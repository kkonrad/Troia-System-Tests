import time
import sys
sys.path.append('.')


from tools.loading_data import load_all
from tools.troia import get_troia_client


DATASETS = ['datasets/' + s for s in ('AdultContent',)]

def executeDawidSkene(jid, tc, iterations, incremental, golds, cost_matrix, assigns):
    print "Executing DS"
    tc.ping()
    print "Ping succesfull"
    if tc.exists(jid):
        tc.reset(jid)
        print "DS model reset"
    else:
        print "No need for DS reset"
    print cost_matrix
    tc.load_categories(cost_matrix, jid)
    print "DS model created"
    tc.load_worker_assigned_labels(assigns, jid)
    print "Labels loaded"
    tc.load_gold_labels(golds, jid)
    print "Gold labels loaded"
    time.sleep(4)
    tc.compute_non_blocking(iterations, jid)
    print "Created computer"
    while 'true' not in tc.is_computed(jid):
        time.sleep(2)
    return tc.majority_votes(jid)


class QualityComparisionTest():

    def __init__(self,tc,jid,iterations,datasets):
        self.jid = jid
        self.tc=tc
        self.datasets=datasets
        self.iterations = iterations


    def run(self):
        print "Begining quality comparition test"
        dataset = self.datasets[0]
        incrementalResults = executeDawidSkene(self.jid,self.tc,self.iterations,True,*dataset)
        batchResults = executeDawidSkene(self.jid,self.tc,self.iterations,False,*dataset)
        labelCount = 0
        differingMajorityVoteCount = 0
        for index in  range(len(incrementalResults)):
            if incrementalResults != batchResults :
                differingMajorityVoteCount = differingMajorityVoteCount + 1
        print "Differing labels = " + differingMajorityVoteCount

def main():
    datasets = [load_all(ds) for ds in DATASETS]
    test = QualityComparisionTest(get_troia_client(),"QualityTest",10,datasets)
    test.run()

if __name__ == "__main__":
    main()
