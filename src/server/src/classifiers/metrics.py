def standard_deviation(values):
    """
    Calculates the standard deviation of a list of values.
    :param values: List of values.
    :return: Standard deviation.
    """
    return (sum([(x - sum(values) / len(values)) ** 2 for x in values]) / len(values)) ** 0.5

def calculate_metrics(observations, expected_outputs):
    """
    Calculates the accuracy, precision, recall and F1 score of observations and their respective standard deviations.
    :param observations: Calculated outputs.
    :param expected_outputs: Expected outputs.
    :return: [(accuracy, standard deviation), (precision, standard deviation), (recall, standard deviation), (F1 score, standard deviation)]
    """

    accuracy, precision, recall, f1_score = [], [], [], []

    for i in range(len(observations)):
        accuracy.append(1 if observations[i] == expected_outputs[i] else 0)
        precision.append(1 if observations[i] == 1 and expected_outputs[i] == 1 else 0)
        recall.append(1 if observations[i] == 1 and expected_outputs[i] == 1 else 0)
        if precision[-1] == 1 and recall[-1] == 1:
            f1_score.append(2 * precision[-1] * recall[-1] / (precision[-1] + recall[-1]) )
        else:
            f1_score.append(0)

    return [(sum(accuracy) / len(accuracy), standard_deviation(accuracy)),
            (sum(precision) / len(precision), standard_deviation(precision)),
            (sum(recall) / len(recall), standard_deviation(recall)),
            (sum(f1_score) / len(f1_score), standard_deviation(f1_score))]
