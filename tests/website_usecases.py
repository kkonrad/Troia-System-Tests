import sys
sys.path.append('.')

from itertools import repeat

from concurrent.futures import ProcessPoolExecutor

from tools.loading_data import load_all
from tools.troia import get_troia_client
from tests.tests_core import TroiaWebDemoUser

WORKERS = 10
ITERATIONS = 10
DATASETS = ['datasets/' + s for s in ('AdultContent', 'BarzanMozafari')]


def exec_fun(worker, *args, **kwargs):
    worker.loop_x_times(*args, **kwargs)


def run_simulation(datasets, workers_num):
    workers = [TroiaWebDemoUser(get_troia_client(),
        "TES_TROJ_JID_" + str(i)) for i in xrange(workers_num)]
    for worker in workers:
        worker.set_datasets(datasets)
    executor = ProcessPoolExecutor(workers_num)
    # maap = map
    maap = lambda *args, **kwargs: list(executor.map(*args, **kwargs))
    maap(exec_fun, workers, repeat(ITERATIONS, workers_num))


def main():
    datastes = [load_all(ds) for ds in DATASETS]
    run_simulation(datastes, WORKERS)


if __name__ == '__main__':
    main()
