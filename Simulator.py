from utils.Simulator_Data import traces2random_list
from utils.Encorder import encode
from solverRuns import *
from utils.Traces import ExperimentTraces, parseExperimentTraces


def test_sat(
    traces
    , startDepth=1
    , maxDepth=float("inf")
    , step=1
    , optimizeDepth=float("inf")
    , optimize="count"
    , minScore=0
    , maxNumModels=1
    , timeout=float("inf")
):
    formulas, timePassed = run_solver(
        traces=traces,
        startDepth=startDepth,
        maxDepth=maxDepth,
        step=step,
        optimizeDepth=optimizeDepth,
        optimize=optimize,
        minScore=minScore,
        maxNumModels=maxNumModels,
        timeout=timeout,
    )
    return [formulas, timePassed]

def simulator(traces: ExperimentTraces):
    data = traces2random_list(traces, 10)
    sample = ExperimentTraces()
    sample.depthOfSolution = traces.depthOfSolution
    tr = None
    for i in data:
        tr = encode(i, sample, tr)
        formulas, timePassed = test_sat(sample)
        print(f"formulas: {[f.prettyPrint() for f in formulas]}, timePassed: {timePassed}")

def test_sample():
    path = "traces/finite/5pc_misclass/disjunctionOfExistence/0003.trace"
    traces: ExperimentTraces = parseExperimentTraces(path)

    print(f'Path: {path}')
    print(f'Posible Solution {traces.possibleSolution}')
    print('Start Test')
    print()
    simulator(traces)

def test_simulation():
    path = "traces/finite/5pc_misclass/disjunctionOfExistence/0003.trace"
    traces: ExperimentTraces = parseExperimentTraces(path)
    tr = None
    #formulas, timePassed = test_sat(traces)
    #print(f"formulas: {[f.prettyPrint() for f in formulas]}, timePassed: {timePassed}")

    data = traces2random_list(traces, 10)
    sample = ExperimentTraces()
    #sample.depthOfSolution = traces.depthOfSolution
    #sample.operators = traces.operators

    #print(f'Traces depthOfSolution {traces.depthOfSolution}')

    for i in data[:20]:
        tr = encode(i, sample, tr)
        #print(sample)
        #print()
    print(sample)
    formulas, timePassed = test_sat(sample)
    print(f"formulas: {[f.prettyPrint() for f in formulas]}, timePassed: {timePassed}")


if __name__ == "__main__":
    test_sample()
    #test_simulation()
    print()
    print("End")
