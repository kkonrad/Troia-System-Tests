import time
import sys
from optparse import OptionParser

sys.path.append('.')


from tools.loading_data import load_all
from tools.troia import get_troia_client
from tools.random_data_generation import generate_data
from tools.random_data_generation import generate_objects
from tools.random_data_generation import generate_votes
from tests.tests_core import TroiaUser




def initializeDawidSkene(jid,tc,workers, golds, labels, cost_matrix,incremental):

    tc.ping()
    if tc.exists(jid):
        tc.reset(jid)
    if incremental :
        tc.load_categories(cost_matrix, jid,"incremental")
    else:
        tc.load_categories(cost_matrix, jid)
    tc.load_gold_labels(golds, jid)


def executeDawidSkene(jid, tc, iterations, objects, votes):
    tc.load_worker_assigned_labels(votes, jid)
    tc.compute_non_blocking(iterations, jid)
    while 'true' not in tc.is_computed(jid):
        time.sleep(2)
    return tc.majority_votes(jid)["result"]



class QualityComparisionTest(TroiaUser):

    def __init__(self,tc,jid,iterations,iteration_step,steps,label_count):
        self.jid = jid
        self.tc=tc
        self.iterations = iterations
        self.iteration_step = iteration_step
        self.steps = steps
        self.label_count = label_count

    def basicTest(self):
        workers, objects, golds, labels, votes, cost_matrix = generate_data(self.label_count)
        for i in range(self.steps):
            startTime = time.time()
            initializeDawidSkene(self.jid,self.tc,workers, golds, labels, cost_matrix,False)
            batchResults=executeDawidSkene(self.jid, self.tc, self.iterations, objects, votes)
            endTime = time.time()
            batchTime = endTime-startTime
            startTime = time.time()
            initializeDawidSkene(self.jid,self.tc,workers, golds, labels, cost_matrix,True)
            incrementalResults=executeDawidSkene(self.jid, self.tc, self.iterations, objects, votes)
            endTime = time.time()
            incrementalTime  = endTime-startTime
            timeDifference = batchTime-incrementalTime
            labelCount = 0
            differingMajorityVoteCount = 0
            objects = incrementalResults.keys()
            for index in  range(len(objects)):
                if incrementalResults[objects[index]] != batchResults[objects[index]] :
                    differingMajorityVoteCount = differingMajorityVoteCount + 1
            print "Objects = "+str(len(objects))+" Iterations = "+ str(self.iterations)+" Differing labels = "\
                   + str(float(differingMajorityVoteCount)/float(len(objects))*100.0) + "% Incremental time adv =" + str(timeDifference)
            self.iterations = self.iterations+self.iteration_step

    def additionTest(self,addition):
        workers, objects, golds, labels, votes, cost_matrix = generate_data(self.label_count)
        initializeDawidSkene(self.jid+"_batch",self.tc,workers, golds, labels, cost_matrix,False)
        initializeDawidSkene(self.jid+"_incremental",self.tc,workers, golds, labels, cost_matrix,True)
        offset = 0
        for i in range(self.steps):
            next_offset = offset + addition
            objects = generate_objects(offset,next_offset)
            votes = generate_votes(addition*5,workers,objects,golds,labels)
            startTime = time.time()
            batchResults=executeDawidSkene(self.jid+"_batch", self.tc, self.iterations, objects, votes)
            endTime = time.time()
            batchTime = endTime-startTime
            startTime = time.time()
            incrementalResults=executeDawidSkene(self.jid+"_incremental", self.tc, self.iterations, objects, votes)
            endTime = time.time()
            incrementalTime = endTime-startTime
            print "Incremental is faster by :" + str(batchTime-incrementalTime)
            labelCount = 0
            differingMajorityVoteCount = 0
            objects = incrementalResults.keys()
        for index in  range(len(objects)):
            if incrementalResults[objects[index]] != batchResults[objects[index]] :
                differingMajorityVoteCount = differingMajorityVoteCount + 1
        print "Objects = "+str(len(objects))+" Iterations = "+ str(self.iterations)+" Differing labels = "\
               + str(float(differingMajorityVoteCount)/float(len(objects))*100.0) + "%" 


    def loop(self):
        print "Begining quality comparition test"
        self.additionTest(500)




def main():
    parser = OptionParser()
    parser.add_option("-l", "--label_count", dest="label_count", default=10000,
                      type='int',help="Number of worker assigned labels in test")
    parser.add_option("-i", "--initial_iterations", dest="initial_iterations", default=1,
                      type='int',help="Number of iteration during first test execution")
    parser.add_option("-s", "--iteration_step", dest="iteration_step", default=5,
                      type='int',help="Difference between iteration count in proceeding test execution")

    (options, args) = parser.parse_args()
    test = QualityComparisionTest(get_troia_client(),"QualityTest",options.initial_iterations,options.iteration_step,20,options.label_count)
    test.loop()

if __name__ == "__main__":
    main()

