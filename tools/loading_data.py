import csv
import os

from tools.common import transform_cost_from_flat_to_dict

def read_data_file(pathh):
    pathh = os.path.normpath(pathh)
    return list(csv.reader(open(pathh), delimiter='\t'))

def load_all(path):
    correct, costs, inputt = \
        [read_data_file(path + s) for s in ['/correct', '/costs', '/input']]
    correct = [x[-2:] for x in correct]
    costs = transform_cost_from_flat_to_dict(costs)
    return correct, costs, inputt



