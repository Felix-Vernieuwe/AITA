import pandas as pd
from typing import List, Tuple
from tabulate import tabulate
import tqdm

from src.classifiers.metrics import calculate_metrics, standard_deviation

from sklearn.model_selection import train_test_split
from sklearn import model_selection

import warnings

from multiprocessing.dummy import Pool

def preprocess_dataset(df: pd.DataFrame, equal_distribution=False, minimize_training=False,
                       minimize_dataset=False, test_split=0.3) -> (pd.DataFrame, pd.DataFrame):
    df = df.fillna("0")

    binary_verdicts = {
        "asshole": 0,
        "not the asshole": 1,
        "no assholes here": 1,
        "everyone sucks": 0,
        "info": 1,
    }

    df['verdict'] = df['verdict'].map(binary_verdicts)

    if minimize_dataset:
        # Decrease the size of the dataset
        df = df.sample(frac=0.2, random_state=1)

    # Split the dataset into training and test sets
    training_set, test_set = train_test_split(df, test_size=test_split, random_state=40)

    if minimize_training:
        # Decrease the size of the training set to make training faster
        training_set = training_set.sample(frac=0.02, random_state=1)

    if equal_distribution:
        # Ensure equal distribution of verdict 0 and 1
        training_set = training_set.groupby('verdict').apply(
            lambda x: x.sample(training_set['verdict'].value_counts().min(), random_state=40)).reset_index(drop=True)

    print("=" * 100)
    print(f"Training on {len(training_set)} samples")
    print(f"\tAmount of NTA vs YTA samples: {list(training_set['verdict'].value_counts())}")
    print(f"\t{round(training_set['verdict'].value_counts()[1] / len(training_set) * 100, 2)}% of samples are NTA")
    print(f"\tAverage length of posts: {training_set['body'].apply(lambda x: len(x.split())).mean()}")
    print(f"Testing on {len(test_set)} samples")
    print(f"\tAmount of NTA vs YTA samples: {list(test_set['verdict'].value_counts())}")
    print(f"\t{round(test_set['verdict'].value_counts()[1] / len(test_set) * 100, 2)}% of samples are NTA")
    print(f"\tAverage length of posts: {test_set['body'].apply(lambda x: len(x.split())).mean()}")
    print("=" * 100)

    return training_set, test_set


class Classifier:
    def __init__(self):
        pass

    def save_model(self, path: str):
        """
        Saves the model to a file.
        :param path: Path to the file.
        """
        raise NotImplementedError()

    def load_model(self, path: str):
        """
        Loads the model from a file.
        :param path: Path to the file.
        """
        raise NotImplementedError()

    def train(self, train_data: pd.DataFrame):
        raise NotImplementedError()

    def classify(self, document: str) -> Tuple[int, float]:
        """
        Get the classification and certainty value for a document.
        :param document: Document to classify.
        :return: (classification, certainty)
        """
        raise NotImplementedError()

    def metrics(self, test_set: pd.DataFrame) -> List[float]:
        """
        Calculates the average certainty, accuracy, precision, recall and F1 score on the test data and their respective standard deviations.
        :param test_set: Test data.
        :return: [avg certainty, accuracy, precision, recall, fscore]
        """

        observations, expected_outputs, certainties = [], [], []

        for index, row in tqdm.tqdm(test_set.iterrows(), total=len(test_set), desc="Calculating metrics"):
            classification, certainty = self.classify(row['body'])
            observations.append(classification)
            expected_outputs.append(row['verdict'])
            certainties.append(certainty)

        obs_occurence = observations.count(0)
        yta_rate = obs_occurence / len(observations)
        if yta_rate > 0.9 or yta_rate < 0.1:
            warnings.warn(
                f"Observations are skewed towards class {1 if obs_occurence / len(observations) > 0.9 else 0}, {obs_occurence} out of {len(observations)} are the same class.")

        return [sum(certainties) / len(certainties)] + calculate_metrics(observations, expected_outputs) + [1 - yta_rate]

    def print_metrics(self, test_set: pd.DataFrame):
        """
        Prints the metrics in a table.
        :param test_set: Test data.
        """
        metrics = self.metrics(test_set)

        stringified_metrics = [str(round(x * 100, 2)) for x in metrics]
        # Transpose the table
        # stringified_metrics = list(map(list, zip(*stringified_metrics)))

        # Tabulate the metrics
        print(tabulate(
            [["Avg. certainty", "Accuracy", "Precision", "Recall", "F1 score", "NTA rate"], stringified_metrics],
            headers="firstrow", tablefmt="fancy_grid"))

    def benchmark_classfier(self, training_set, test_set, folds=5):
        """
        Benchmarks the classifier by calculating the average metrics over a number of folds.
        :param training_set: Training data.
        :param test_set: Test data.
        :param folds: Number of folds.
        :return: [(avg certainty, std certainty), (avg accuracy, std accuracy), (avg precision, std precision), (avg recall, std recall), (avg fscore, std fscore)]
        """
        kf = model_selection.KFold(n_splits=folds, shuffle=True, random_state=40)

        metrics = []
        for train_index, test_index in kf.split(training_set):
            # Split the training set into training and validation sets
            train, val = training_set.iloc[train_index], training_set.iloc[test_index]

            # Train the classifier
            self.train(train)

            # Calculate the metrics
            metrics.append(self.metrics(test_set))

        # Calculate the average metrics and their standard deviations
        avg_metrics = [sum(x) / len(x) for x in zip(*metrics)]
        std_metrics = [standard_deviation(x) for x in zip(*metrics)]

        metrics = list(zip(avg_metrics, std_metrics))
        stringified_metrics = [[str(round(x[0] * 100, 2)) + " ± " + str(round(x[1] * 100, 2)) for x in metrics]]

        print(tabulate([["Avg. certainty", "Accuracy", "Precision", "Recall", "F1 score", "NTA rate"], *stringified_metrics],
                       headers="firstrow", tablefmt="fancy_grid"))
