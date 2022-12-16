import tqdm
import os
from dotenv import load_dotenv
import pandas as pd

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

from src.classifiers.metrics import calculate_metrics, standard_deviation

from src.classifiers.classifier import Classifier, preprocess_dataset


class MultinomialBayesClassifier(Classifier):
    def __init__(self):
        self.vectorizer = None
        self.classifier = None

    def save_model(self, path):
        import pickle
        with open(path, 'wb') as file:
            pickle.dump(self.classifier, file)
            pickle.dump(self.vectorizer, file)

    def load_model(self, path):
        import pickle
        with open(path, 'rb') as file:
            self.classifier = pickle.load(file)
            self.vectorizer = pickle.load(file)

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
