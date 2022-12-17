import pandas as pd
from typing import List, Tuple
import tqdm
import os

from gensim import models
from src.classifiers.classifier import Classifier, preprocess_dataset
from sklearn.linear_model import LogisticRegression

import pickle

EPOCHS = 10

class Doc2VecClassifier(Classifier):
    def __init__(self):
        self.vectorizer = None
        self.classifier = None

    def save_model(self, path: str = "./classifiers/doc2vec"):
        if not os.path.exists(path):
            os.makedirs(path)
        self.vectorizer.save(path + "/vectorizer.model")
        with open(path + "/classifier.pickle", "wb") as f:
            pickle.dump(self.classifier, f)

    def load_model(self, path: str = "./classifiers/doc2vec"):
        self.vectorizer = models.Doc2Vec.load(path + "/vectorizer.model")
        with open(path + "/classifier.pickle", "rb") as f:
            self.classifier = pickle.load(f)

    def train(self, train_data: pd.DataFrame):
        # train_data is pd, train_data['verdict'] is label, train_data['body'] is long string of text
        self.vectorizer = models.Doc2Vec(vector_size=50, min_count=2, workers=4)

        # train_data['body'] is a list of strings, convert to TaggedDocument
        tagged_data = [models.doc2vec.TaggedDocument(words=body.split(), tags=[str(i)]) for i, body in
                       enumerate(train_data['body'])]
        self.vectorizer.build_vocab(tagged_data)

        # self.vectorizer.train(train_data['body'], total_examples=self.vectorizer.corpus_count, epochs=EPOCHS)
        for _ in tqdm.tqdm(range(EPOCHS), desc="Training Doc2Vec"):
            # permuted = train_data.sample(frac=1)
            self.vectorizer.train(tagged_data, total_examples=self.vectorizer.corpus_count, epochs=1)
            self.vectorizer.alpha -= 0.002
            self.vectorizer.min_alpha = self.vectorizer.alpha
        self.classifier = LogisticRegression(C=1e5)
        self.classifier.fit([self.vectorizer.infer_vector(body.split()) for body in train_data['body']],
                            train_data['verdict'])

    def classify(self, document: str) -> Tuple[int, float]:
        vector = self.vectorizer.infer_vector(document.split())
        classification = self.classifier.predict([vector])
        return classification[0], self.classifier.predict_proba([vector])[0][classification][0]


if __name__ == "__main__":
    df = pd.read_csv("../../../dataset/aita_clean.csv")
    training_set, test_set = preprocess_dataset(df, minimize_dataset=False, minimize_training=False, equal_distribution=True)

    classifier = Doc2VecClassifier()
    # classifier.train(training_set)

    # print(classifier.classify("I was the asshole for not letting my friend borrow my car."))

    # classifier.print_metrics(test_set)
    classifier.benchmark_classfier(training_set, test_set)
