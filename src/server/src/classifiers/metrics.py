from typing import List

def standard_deviation(values: List[float]):
    """
    Calculates the standard deviation of a list of values.
    :param values: List of values.
    :return: Standard deviation.
    """
    return (sum([(x - sum(values) / len(values)) ** 2 for x in values]) / len(values)) ** 0.5

def calculate_metrics(observations: List[int], expected_outputs: List[int]) -> List[float]:
    """
    Calculates the accuracy, precision, recall and F1 score of observations
    :param observations: Calculated outputs.
    :param expected_outputs: Expected outputs.
    :return: [accuracy, precision, recall, fscore]
    """

    # precision, recall, fscore, support = score(expected_outputs, observations, average='macro')
    # accuracy = sum([1 if x == y else 0 for x, y in zip(observations, expected_outputs)]) / len(observations)

    true_pos, false_pos, true_neg, false_neg = 0, 0, 0, 0
    for x, y in zip(observations, expected_outputs):
        if x == 1 and y == 1:
            true_pos += 1
        elif x == 1 and y == 0:
            false_pos += 1
        elif x == 0 and y == 0:
            true_neg += 1
        elif x == 0 and y == 1:
            false_neg += 1

    precision = true_pos / (true_pos + false_pos)
    recall = true_pos / (true_pos + false_neg)
    fscore = 2 * precision * recall / (precision + recall)
    accuracy = (true_pos + true_neg) / len(observations)

    return [accuracy, precision, recall, fscore]
