import time
import sys
sys.path.append('..')


from tools.loading_data import load_all
from tools.troia import get_troia_client


DATASETS = ['datasets/' + s for s in ('AdultContent', 'BarzanMozafari')]

def executeDawidSkene(jid, tc, iterations, incremental, golds, cost_matrix, assigns):
    tc.ping()
    if tc.exists(jid):
        tc.reset(jid)
    tc.load_categories(cost_matrix, jid)
    tc.load_worker_assigned_labels(assigns, jid)
    tc.load_gold_labels(golds, jid)
    time.sleep(4)
    tc.compute_non_blocking(iterations, jid)
    while 'true' not in tc.is_computed(jid):
        time.sleep(2)
    return tc.majority_votes(jid)


class QualityComparisionTest():

    def init(self,tc,jid,iterations,dataset):
        self.jid = jid
        self.tc=tc
        self.dataset=dataset
        self.iterations = iterations


    def run(self):
        print "Begining quality comparition test"
        incrementalResults = executeDawidSkene(self.jid,self.tc,self.iterations,True,*dataset)
        batchResults = executeDawidSkene(self.jid,self.tc,self.iterations,False,*dataset)
        labelCount = 0
        differingMajorityVoteCount = 0
        for index in  range(len(incrementalResults)):
            if incrementalResults != batchResults :
                differingMajorityVoteCount = differingMajorityVoteCount + 1
        print "Differing labels = " + differingMajorityVoteCount

def main():
    datastes = [load_all(ds) for ds in DATASETS]
