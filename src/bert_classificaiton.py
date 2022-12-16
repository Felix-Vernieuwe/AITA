import tqdm
import time

from multiprocessing.dummy import Pool as ThreadPool

import pandas as pd
import numpy as np

from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.model_selection import train_test_split

import torch as torch
from torch.utils.data import TensorDataset
from torch.utils.data import RandomSampler, SequentialSampler

from JudgeBERT import JudgeBERT





EPOCH = 3
BATCH_SIZE = 32
LEARNING_RATE = 2e-5
EPSILON = 1e-8
VALIDATION_SPLIT = 0.2



df = pd.read_csv("dataset/aita_clean.csv").fillna("0")

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

binary_verdicts = {
    "asshole": 0,
    "not the asshole": 1,
    "no assholes here": 1,
    "everyone sucks": 0,
    "info": 1,
}

df['verdict'] = df['verdict'].map(binary_verdicts)

train_df, test_df = train_test_split(df, test_size=0.3, random_state=40)

# Minimise dataset
train_df = train_df.sample(frac=0.5, random_state=40)

# Ensure equal distribution of verdict 0 and 1
# train_df = train_df.groupby('verdict').apply(lambda x: x.sample(train_df['verdict'].value_counts().min(), random_state=40)).reset_index(drop=True)

print("=" * 100)
print(f"Training on {len(train_df)} samples")
print(f"\tAmount of YTA vs NTA samples: {list(train_df['verdict'].value_counts())}")
print(f"\tAverage length of posts: {train_df['body'].apply(lambda x: len(x.split())).mean()}")
print(f"Testing on {len(test_df)} samples")
print(f"\tAmount of YTA vs NTA samples: {list(test_df['verdict'].value_counts())}")
print(f"\tAverage length of posts: {test_df['body'].apply(lambda x: len(x.split())).mean()}")
print("*" * 100)

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

token_id = []
attention_masks = []


def preprocessing(input_text):
    """
    Preprocesses the input text to be used by the model.
    :param input_text: The text to preprocess.
    :return: <class transformers.tokenization_utils_base.BatchEncoding> containing lists of token ids, token type ids and attention masks (model will ignore tokens with mask = 0).
    """
    return tokenizer.encode_plus(
        input_text,
        add_special_tokens=True,
        max_length=32,
        pad_to_max_length=True,
        return_attention_mask=True,
        return_tensors='pt'
    )


# Preprocess training data by tokenizing it, multithreaded for speed
start = time.time()
pool = ThreadPool(4)
encoding_dicts = pool.map(preprocessing, train_df['body'])
pool.close()
pool.join()
print("Preprocessing took", time.time() - start, "seconds")

token_id, attention_masks = [x['input_ids'] for x in encoding_dicts], [x['attention_mask'] for x in encoding_dicts]

token_id = torch.cat(token_id, dim=0)
attention_masks = torch.cat(attention_masks, dim=0)
labels = torch.tensor(train_df['verdict'].values)

# Split training dataframe into training and validation sets
training_dataset, validation_dataset = train_test_split(np.arange(len(labels)), test_size=VALIDATION_SPLIT, random_state=40, shuffle=True, stratify=labels)

# Convert training and validation sets to tensors
train_set = TensorDataset(token_id[training_dataset], attention_masks[training_dataset], labels[training_dataset])
validation_set = TensorDataset(token_id[validation_dataset], attention_masks[validation_dataset], labels[validation_dataset])

# Create dataloaders for training and validation sets (efficiently loads data into GPU/CPU memory)
train_loader = torch.utils.data.DataLoader(train_set, batch_size=BATCH_SIZE, sampler=RandomSampler(train_set))
validation_loader = torch.utils.data.DataLoader(validation_set, batch_size=BATCH_SIZE, sampler=SequentialSampler(validation_set))

# Load pre-trained BERT model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2, output_attentions=False, output_hidden_states=False, attention_probs_dropout_prob=0.5, hidden_dropout_prob=0.5)

# Optimizer for the network using AdamW
optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE, eps=EPSILON)


# Enable GPU computation if available
if torch.cuda.is_available():
    model.cuda()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Calculates accuracy of validation set predictions
def flat_accuracy(preds, labels):
    pred_flat = np.argmax(preds, axis=1).flatten()
    labels_flat = labels.flatten()
    return np.sum(pred_flat == labels_flat) / len(labels_flat)


# Training loop
for epoch in range(EPOCH):
    model.train()

    # ==================================================================================================
    # Training step
    # ==================================================================================================

    total_loss = 0
    for step, batch in enumerate(tqdm.tqdm(train_loader)):
        # Load sentence batch and labels into GPU memory
        batch = tuple(t.to(device) for t in batch)
        b_input_ids, b_input_mask, b_labels = batch

        # Clear gradients
        optimizer.zero_grad()

        # Model forward pass, processes sentence batch through BERT and returns logits
        output = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask, labels=b_labels)

        # Backpropagation
        output.loss.backward()
        total_loss += output.loss.item()

        # Clip gradients to avoid exploding gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

        # Update weights for each layer
        optimizer.step()

    # Calculate average loss over all training batches
    avg_train_loss = total_loss / len(train_loader)
    print("Average training loss: {}".format(avg_train_loss))

    # ==================================================================================================
    # Validation step
    # ==================================================================================================

    # Put model in evaluation mode to evaluate loss between validation data and predictions
    model.eval()
    total_eval_accuracy = 0
    total_eval_loss = 0
    nb_eval_steps = 0

    for batch in tqdm.tqdm(validation_loader):
        # Load sentence batch and labels into GPU memory
        batch = tuple(t.to(device) for t in batch)
        b_input_ids, b_input_mask, b_labels = batch

        # Model forward pass, processes sentence batch through BERT and returns logits
        with torch.no_grad():
            output = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask, labels=b_labels)
        total_eval_loss += output.loss.item()

        # Move logits and labels to CPU and convert to numpy arrays
        logits = output.logits.detach().cpu().numpy()
        label_ids = b_labels.to('cpu').numpy()

        # Calculate accuracy for this batch of test sentences
        total_eval_accuracy += flat_accuracy(logits, label_ids)
    avg_val_accuracy = total_eval_accuracy / len(validation_loader)
    print("Validation Accuracy: {}".format(avg_val_accuracy))
    avg_val_loss = total_eval_loss / len(validation_loader)
    print("Validation Loss: {}".format(avg_val_loss))
    print("Finished epoch {}".format(epoch))


def save_model(model_path):
    """
    Saves the model to the specified path.
    """
    print("Saving model to {}".format(model_path))
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)


def classify_post(post):
    """
    Classifies a post as either "true" or "false" using the trained model.
    :param post: the post to classify
    :return: Tensor containing the classification result
    """
    encoding_dict = preprocessing(post)

    input_ids = [encoding_dict['input_ids']]
    attention_masks = [encoding_dict['attention_mask']]

    input_ids = torch.cat(input_ids, dim=0).to(device)
    attention_masks = torch.cat(attention_masks, dim=0).to(device)

    with torch.no_grad():
        output = model(input_ids, token_type_ids=None, attention_mask=attention_masks)

    # Return certainty of classification and classification result
    return torch.softmax(output.logits, dim=1), torch.argmax(output.logits, dim=1)

def classifier_accuracy(test_set: pd.DataFrame):
    """
    Returns the accuracy of the classifier on the test set.
    :param test_set: Subset of data to test the classifier on.
    :return: Accuracy of the classifier on the test set.
    """
    correct, average_certainty = 0, 0.0
    for index, row in test_set.iterrows():
        certainty, classification = classify_post(row['body'])
        if classification == row['verdict']:
            correct += 1
        average_certainty += certainty[0][classification]
    return correct / len(test_set), float(average_certainty) / len(test_set)


test_set = test_df.sample(frac=0.05)
print("Accuracy on test set: {} with average certainty of {}".format(*classifier_accuracy(test_set)))
