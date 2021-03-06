from itertools import combinations_with_replacement
from random import choice

from tools.common import transform_cost_from_flat_to_dict


def _generate_elements(start_number,n, prefix):
    return [prefix + str(i) for i in xrange(start_number,start_number+n)]


def generate_workers(start_number,n_workers, prefix="worker_"):
    return _generate_elements(start_number,n_workers, prefix)


def generate_objects(start_number,n_objects, prefix="object_labels_quite_long_"):
    return _generate_elements(start_number,n_objects, prefix)


def generate_golds(start_number,n_golds, labels, prefix='gold_object_labels_quite_long_'):
    return [(gold, choice(labels)) for gold in _generate_elements(start_number,n_golds, prefix)]


def generate_labels(start_number,n_labels, prefix='label_'):
    return _generate_elements(start_number,n_labels, prefix)


def generate_core_items(start_number,n_workers, n_objects, n_labels):
    return generate_workers(start_number,n_workers), generate_objects(start_number,n_objects), \
         generate_labels(start_number,n_labels)


def generate_votes(n_votes, workers, objects, golds, labels):
    objects = objects + [x[0] for x in golds]
    return [(choice(workers), choice(objects), choice(labels))
        for _ in xrange(n_votes)]


def generate_cost_matrix(labels):
    return [(l1, l2, int(l1 != l2))
        for l1, l2 in combinations_with_replacement(labels, 2)]


def generate_data(n_votes, n_labels=2, n_objects=None,
        n_workers=None, n_golds=None):
    n_objects = n_objects or n_votes / 5
    n_workers = n_workers or n_votes / 50
    n_golds = n_objects or n_objects / 20

    workers, objects, labels = generate_core_items(0,n_workers,
        n_objects, n_labels)
    golds = generate_golds(0,n_golds,labels)
    votes = generate_votes(n_votes, workers, objects, golds, labels)

    cost_matrix = generate_cost_matrix(labels)
    cost_matrix = transform_cost_from_flat_to_dict(cost_matrix)
    return workers, objects, golds, labels, votes, cost_matrix
