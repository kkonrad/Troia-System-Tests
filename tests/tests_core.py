import time
import math
import random


class TroiaUser(object):

    def __init__(self, tc, jid=None):
        self.tc = tc
        self.jid = jid

    def init(self, *args, **kwargs):
        """ Allows you to prepare TroiaClient """
        self.tc.reset(self.jid)

    def loop(self):
        """ Abstract to redefine """
        raise NotImplementedError

    def loop_forever(self):
        self.init()
        while True:
            self.loop()

    def loop_for_time(self, seconds):
        self.init()
        deadline = time.time() + seconds
        while deadline > time.time():
            self.loop()

    def loop_x_times(self, iterations):
        self.init()
        for _ in xrange(iterations):
            self.loop()


def web_demo_scenario(jid, tc, iterations, golds, cost_matrix, assigns):
    N = 500
    tc.ping()
    tc.exists(jid)
    tc.reset(jid)

    tc.load_categories(cost_matrix, jid)
    num_packs = int(math.ceil(len(assigns) / float(N)))
    for package in (assigns[i * N:(i + 1) * N] for i in xrange(num_packs)):
        tc.load_worker_assigned_labels(package, jid)
    tc.load_gold_labels(golds, jid)
    time.sleep(4)
    for _ in xrange(iterations):
        tc.compute_non_blocking(1, jid)
        while 'true' not in tc.is_computed(jid):
            time.sleep(2)

        tc.print_worker_summary(False, jid)
        tc.majority_votes(jid)
        time.sleep(2)


class TroiaWebDemoUser(TroiaUser):

    def init(self):
        self.current_jid_num = 0

    def set_datasets(self, datasets):
        self.datasets = datasets

    def loop(self):
        print "Begining loop"
        self.current_jid_num += 1
        jid = self.jid + str(self.current_jid_num)
        dataset = random.choice(self.datasets)
        iterations = random.choice((5, 10, 20))
        web_demo_scenario(jid, self.tc, iterations, *dataset)
