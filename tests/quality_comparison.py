import time
import sys
sys.path.append('.')


from tools.loading_data import load_all
from tools.troia import get_troia_client
from tests.tests_core import TroiaUser

DATASETS = ['datasets/' + s for s in ('AdultContent','BarzanMozafari')]

def executeDawidSkene(jid, tc, iterations, incremental, golds, cost_matrix, assigns):
#    print "Executing DS"
    tc.ping()
#    print "Ping succesfull"
    if tc.exists(jid):
        tc.reset(jid)
#        print "DS model reset"
#    else:
#        print "No need for DS reset"
#   print cost_matrix
    if incremental :
        tc.load_categories(cost_matrix, jid,"incremental")
    else:
        tc.load_categories(cost_matrix, jid)
#    print "DS model created"
    tc.load_worker_assigned_labels(assigns, jid)
#    print "Labels loaded"
    tc.load_gold_labels(golds, jid)
#    print "Gold labels loaded"
    time.sleep(4)
    tc.compute_non_blocking(iterations, jid)
#    print "Created computer"
    while 'true' not in tc.is_computed(jid):
        time.sleep(2)
    return tc.majority_votes(jid)["result"]


class QualityComparisionTest(TroiaUser):

    def __init__(self,tc,jid,iterations,dataset):
        self.jid = jid
        self.tc=tc
        self.dataset=dataset
        self.iterations = iterations


    def loop(self):
        print "Begining quality comparition test"
        dataset = self.dataset
        startTime = time.clock()
        incrementalResults = executeDawidSkene(self.jid,self.tc,self.iterations,True,*dataset)
        endTime = time.clock()
        incrementalTime = endTime-startTime
        startTime = time.clock()
        batchResults = executeDawidSkene(self.jid,self.tc,self.iterations,False,*dataset)
        endTime = time.clock()
        batchTime = endTime-startTime
        timeDifference = incrementalTime-batchTime
        labelCount = 0
        differingMajorityVoteCount = 0
        objects = incrementalResults.keys()
        for index in  range(len(objects)):
            if incrementalResults[objects[index]] != batchResults[objects[index]] :
                differingMajorityVoteCount = differingMajorityVoteCount + 1
        print "Objects = "+str(len(objects))+" Iterations = "+ str(self.iterations)+" Differing labels = "\
            + str(differingMajorityVoteCount) + " Incremental time adv =" + str(timeDifference)

def main():
    datasets = [load_all(ds) for ds in DATASETS]

    test = QualityComparisionTest(get_troia_client(),"QualityTest",3,datasets[0])
    test.loop()
    test = QualityComparisionTest(get_troia_client(),"QualityTest",10,datasets[0])
    test.loop()
    test = QualityComparisionTest(get_troia_client(),"QualityTest",15,datasets[0])
    test.loop()
    test = QualityComparisionTest(get_troia_client(),"QualityTest",30,datasets[0])
    test.loop()

    test = QualityComparisionTest(get_troia_client(),"QualityTest",1,datasets[1])
    test.loop()
    test = QualityComparisionTest(get_troia_client(),"QualityTest",3,datasets[1])
    test.loop()
    test = QualityComparisionTest(get_troia_client(),"QualityTest",10,datasets[1])
    test.loop()
    test = QualityComparisionTest(get_troia_client(),"QualityTest",15,datasets[1])
    test.loop()
    test = QualityComparisionTest(get_troia_client(),"QualityTest",30,datasets[1])
    test.loop()

if __name__ == "__main__":
    main()
