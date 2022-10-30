import os
import subprocess

from utils.Traces import ExperimentTraces, parseExperimentTraces, Trace
import random

#Class which take a Traces and split into Traces
class RuntimeTraces:

    #If traces is not Empty the class will split the traces into few traces
    def __init__(self, traces=None):
        self.traces = traces
        self.stockTraces = self.copyTraces()
        self.splitTraces = []
        self.add2splitTrace()

    #Copy of the member traces without a references
    def copyTraces(self):
        traces = ExperimentTraces()
        traces.acceptedTraces = self.traces.acceptedTraces
        traces.rejectedTraces = self.traces.rejectedTraces
        traces.operators = self.traces.operators
        traces.numVariables = self.traces.numVariables
        traces.possibleSolution = self.traces.possibleSolution
        traces.depthOfSolution = self.traces.depthOfSolution
        return traces

    #set the member traces with a traces
    def setTraces(self, traces):
        self.traces = traces

    #set the member traces with the source
    def setTraceFromFile(self, source):
        self.traces = parseExperimentTraces(source)

    #Function to have a a subset of the member traces
    def nextTraces(self):
        acceptedTraces = self.stockTraces.acceptedTraces
        rejectedTraces = self.stockTraces.rejectedTraces

        raccept = random.randint(1, 3)
        rreject = random.randint(1, 3)

        if raccept != 0 or rreject != 0:
            acceptedTraces = acceptedTraces[:raccept]
            rejectedTraces = rejectedTraces[:rreject]

            currentTraces = self.copyTraces()
            currentTraces.acceptedTraces = acceptedTraces
            currentTraces.rejectedTraces = rejectedTraces

            self.splitTraces.append(currentTraces)

            self.stockTraces.acceptedTraces = self.stockTraces.acceptedTraces[raccept:]
            self.stockTraces.rejectedTraces = self.stockTraces.rejectedTraces[rreject:]
        else:
            self.nextTraces()

    #Check that they is a trace
    def hasTraces(self):
        if self.stockTraces.acceptedTraces == [] and self.stockTraces.rejectedTraces == []:
            return False
        return True

    #Take all Traces and spilt it into few Traces
    def add2splitTrace(self):
        if self.stockTraces is not None:
            while self.hasTraces():
                self.nextTraces()
        if not self.check():
            print('Split Traces are not correct')
    #Check that the splitTraces is the same as the traces
    def check(self):
        acceptedTraces = []
        rejectedTraces = []
        for traces in self.splitTraces:
            acceptedTraces = acceptedTraces + traces.acceptedTraces
            rejectedTraces = rejectedTraces + traces.rejectedTraces

        if acceptedTraces == self.traces.acceptedTraces and rejectedTraces == self.traces.rejectedTraces:
            return True
        return False

    def writeAllSplitTraces(self, dir):
        a = 1
        for traces in self.splitTraces:
            traces.writeTraces(dir + str(a) + '.trace')
            a += 1

    def runExperiment(self):
        #Path where the Splitet Trace has to find
        path_dir = 'RunTimeTest/BeiPartTest/'
        self.writeAllSplitTraces(path_dir)
        print('Start Experiment')
        a = 1
        for _ in self.splitTraces:
            print('Start ' + str(a) + '. split Trace')
            subprocess.call('python experiment.py -f ' + path_dir + str(a) + '.trace', shell=True)
            print('End ' + str(a))
            a += 1


#Test: All traces is equal to main traces
if __name__ == "__main__":
    test: ExperimentTraces
    test = parseExperimentTraces("../traces/finite/5pc_misclass/disjunctionOfExistence/0003.trace")

    a = RuntimeTraces(test)
    #a.runExperiment()
    '''
    for i in range(len(a.splitTraces)):
        print('This is {} Traces Data'.format(i))
        print(a.splitTraces[i])

    print('This is your trace')
    print(a.traces)
    '''





