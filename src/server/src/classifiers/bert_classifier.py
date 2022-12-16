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

import torch.nn as nn

EPOCH = 3
BATCH_SIZE = 32
LEARNING_RATE = 2e-5
EPSILON = 1e-8
VALIDATION_SPLIT = 0.2

from classifier import Classifier, preprocess_dataset


def flat_accuracy(preds, labels):
    """
    Returns the accuracy of the classifier on the test set.
    :param preds: Predictions from the model.
    :param labels: Actual labels of the test set.
    :return: Accuracy of the model.
    """
    pred_flat = np.argmax(preds, axis=1).flatten()
    labels_flat = labels.flatten()
    return np.sum(pred_flat == labels_flat) / len(labels_flat)


class BertClassifier(Classifier):
    devices = [("cuda", lambda: torch.cuda.is_available()),
               ("mps", lambda: torch.backends.mps.is_available())]

    def __init__(self):
        self.tokenizer = None
        self.classifier = None
        self.device = torch.device(self.get_device())

    def get_device(self):
        for device, available in BertClassifier.devices:
            if available():
                return device
        return "cpu"

    def tokenize(self, input_text):
        """
        Preprocesses the input text to be used by the model.
        :param input_text: The text to preprocess.
        :return: <class transformers.tokenization_utils_base.BatchEncoding> containing lists of token ids, token type ids and attention masks (model will ignore tokens with mask = 0).
        """
        return self.tokenizer.encode_plus(
            input_text,
            add_special_tokens=True,
            max_length=32,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors='pt'
        )

    def preprocess_training_data(self, data):

        token_id, attention_masks = [], []

        # Preprocess training data by tokenizing it, multithreaded for speed
        # start = time.time()
        # pool = ThreadPool(4)
        # encoding_dicts = pool.map(tokenize, train_df['body'])
        # pool.close()
        # pool.join()
        # print("Preprocessing took", time.time() - start, "seconds")
        # token_id, attention_masks = [x['input_ids'] for x in encoding_dicts], [x['attention_mask'] for x in encoding_dicts]

        for index, row in tqdm.tqdm(data.iterrows(), total=len(data)):
            encoding_dict = self.tokenize(row['body'])
            token_id.append(encoding_dict['input_ids'])
            attention_masks.append(encoding_dict['attention_mask'])

        token_id = torch.cat(token_id, dim=0)
        attention_masks = torch.cat(attention_masks, dim=0)
        labels = torch.tensor(data['verdict'].values)

        # Split training dataframe into training and validation sets
        training_dataset, validation_dataset = train_test_split(np.arange(len(labels)), test_size=VALIDATION_SPLIT,
                                                                random_state=40, shuffle=True, stratify=labels)

        # Convert training and validation sets to tensors
        train_set = TensorDataset(token_id[training_dataset], attention_masks[training_dataset],
                                  labels[training_dataset])
        validation_set = TensorDataset(token_id[validation_dataset], attention_masks[validation_dataset],
                                       labels[validation_dataset])

        # Create dataloaders for training and validation sets (efficiently loads data into GPU/CPU memory)
        train_loader = torch.utils.data.DataLoader(train_set, batch_size=BATCH_SIZE, sampler=RandomSampler(train_set))
        validation_loader = torch.utils.data.DataLoader(validation_set, batch_size=BATCH_SIZE,
                                                        sampler=SequentialSampler(validation_set))

        return train_loader, validation_loader

    def train(self, train_data):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
        self.classifier = BertForSequenceClassification. \
            from_pretrained("bert-base-uncased", num_labels=2, output_attentions=False, output_hidden_states=False,
                            attention_probs_dropout_prob=0.5, hidden_dropout_prob=0.5)

        train_loader, validation_loader = self.preprocess_training_data(train_data)

        # Optimizer for the network using AdamW
        optimizer = torch.optim.AdamW(self.classifier.parameters(), lr=LEARNING_RATE, eps=EPSILON)

        # Enable GPU computation if available
        if torch.cuda.is_available():
            self.classifier.cuda()
        if torch.backends.mps.is_available():
            self.classifier.to(self.device)

        # Training loop
        for epoch in range(EPOCH):
            self.classifier.train()

            # ==================================================================================================
            # Training step
            # ==================================================================================================

            total_loss = 0
            for step, batch in enumerate(tqdm.tqdm(train_loader)):
                # Load sentence batch and labels into GPU memory
                batch = tuple(t.to(self.device) for t in batch)
                b_input_ids, b_input_mask, b_labels = batch

                # Clear gradients
                optimizer.zero_grad()

                # Model forward pass, processes sentence batch through BERT and returns logits
                output = self.classifier(b_input_ids, token_type_ids=None, attention_mask=b_input_mask, labels=b_labels)

                # Backpropagation
                output.loss.backward()
                total_loss += output.loss.item()

                # Clip gradients to avoid exploding gradients
                torch.nn.utils.clip_grad_norm_(self.classifier.parameters(), 1.0)

                # Update weights for each layer
                optimizer.step()

            # Calculate average loss over all training batches
            avg_train_loss = total_loss / len(train_loader)
            print("Average training loss: {}".format(avg_train_loss))

            # ==================================================================================================
            # Validation step
            # ==================================================================================================

            # Put model in evaluation mode to evaluate loss between validation data and predictions
            self.classifier.eval()
            total_eval_accuracy = 0
            total_eval_loss = 0
            nb_eval_steps = 0

            for batch in tqdm.tqdm(validation_loader):
                # Load sentence batch and labels into GPU memory
                batch = tuple(t.to(self.device) for t in batch)
                b_input_ids, b_input_mask, b_labels = batch

                # Model forward pass, processes sentence batch through BERT and returns logits
                with torch.no_grad():
                    output = self.classifier(b_input_ids, token_type_ids=None, attention_mask=b_input_mask,
                                             labels=b_labels)
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

    def classify(self, document):
        encoding_dict = self.tokenize(document)

        input_ids, attention_masks = [encoding_dict['input_ids']], [encoding_dict['attention_mask']]

        input_ids = torch.cat(input_ids, dim=0).to(self.device)
        attention_masks = torch.cat(attention_masks, dim=0).to(self.device)

        with torch.no_grad():
            output = self.classifier(input_ids, token_type_ids=None, attention_mask=attention_masks)

        # Return classification result and certainty
        classification = torch.argmax(output.logits, dim=1).item()
        return classification, output.logits[0][classification].item()


if __name__ == '__main__':
    df = pd.read_csv("src/server/dataset/aita_clean.csv")
    training_set, test_set = preprocess_dataset(df)

    classifier = BertClassifier()
    classifier.train(training_set)

    # print(classifier.classify("I was the asshole for not letting my friend borrow my car."))

    classifier.print_metrics(test_set)
