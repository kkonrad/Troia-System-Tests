import time


def transform_cost_from_flat_to_dict(cost):
    dictt = {}
    for c1, c2, cost_ in cost:
        el = dictt.get(c1, {})
        el[c2] = cost_
        dictt[c1] = el
    return dictt.items()


def timeit(f, *args, **kwargs):
    start = time.time()
    f(*args, **kwargs)
    return time.time() - start
