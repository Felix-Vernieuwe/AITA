import tqdm
import os
from dotenv import load_dotenv
import pandas as pd

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

from src.classifiers.metrics import calculate_metrics, standard_deviation

from src.classifiers.classifier import Classifier, preprocess_dataset

import pickle

class MultinomialBayesClassifier(Classifier):
    def __init__(self):
        self.vectorizer = None
        self.classifier = None

    def save_model(self, path):
        with open(path + "mnb.vectorizer", "wb") as f:
            pickle.dump(self.vectorizer, f)
        with open(path + "mnb.classifier", "wb") as f:
            pickle.dump(self.classifier, f)


    def load_model(self, path):
        with open(path + "mnb.vectorizer", "rb") as f:
            self.vectorizer = pickle.load(f)
        with open(path + "mnb.classifier", "rb") as f:
            self.classifier = pickle.load(f)

    def train(self, train_data):
        self.vectorizer = CountVectorizer()
        self.classifier = MultinomialNB()
        self.classifier.fit(self.vectorizer.fit_transform(train_data["body"]), train_data["verdict"])

    def classify(self, document):
        vector = self.vectorizer.transform([document])
        classification = self.classifier.predict(vector)[0]
        return classification, self.classifier.predict_proba(vector)[0][classification]


if __name__ == "__main__":
    df = pd.read_csv("../../../dataset/aita_clean.csv")
    training_set, test_set = preprocess_dataset(df)

    classifier = MultinomialBayesClassifier()
    classifier.train(training_set)

    # print(classifier.classify("I was the asshole for not letting my friend borrow my car."))

    # classifier.print_metrics(test_set)
    classifier.benchmark_classfier(training_set, test_set)
