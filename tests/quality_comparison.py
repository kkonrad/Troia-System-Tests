import time
import sys
sys.path.append('.')


from tools.loading_data import load_all
from tools.troia import get_troia_client
from tools.random_data_generation import generate_data
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
    tc.compute_non_blocking(iterations, jid)
#    print "Created computer"
    while 'true' not in tc.is_computed(jid):
        time.sleep(2)
    return tc.majority_votes(jid)["result"]


class QualityComparisionTest(TroiaUser):

    def __init__(self,tc,jid,iterations,iteration_step,dataset):
        self.jid = jid
        self.tc=tc
        self.dataset=dataset
        self.iterations = iterations
        self.iteration_step = iteration_step

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
        self.iterations = self.iterations+self.iteration_step



def main():
    datasets = [load_all(ds) for ds in DATASETS]
    workers, objects, golds, labels, votes, cost_matrix = generate_data(10000)
    fakeDataset = [golds,cost_matrix,votes]
    test = QualityComparisionTest(get_troia_client(),"QualityTest",1,3,fakeDataset)
    test.loop_x_times(5)

if __name__ == "__main__":
    main()
