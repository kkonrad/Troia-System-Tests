import csv
import os

from tools.common import transform_cost_from_flat_to_dict


def load_all(path):
    def tmp(pathh):
        pathh = os.path.normpath(pathh)
        return list(csv.reader(open(pathh), delimiter='\t'))

    correct, costs, inputt = \
        [tmp(path + s) for s in ['/correct', '/costs', '/input']]
    correct = [x[-2:] for x in correct]
    costs = transform_cost_from_flat_to_dict(costs)
    return correct, costs, inputt
