from utils.Simulator_Data import traces2random_list
from utils.Encorder import convert
from solverRuns import *
from utils.Traces import ExperimentTraces, parseExperimentTraces
import logging
import csv;

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

def test_dt(
        traces
        , misclassification
):
    timePassed, numAtoms, numPrimitives = run_dt_solver(
        traces=traces,
        misclassification=misclassification,
    )
    print(f"timePassed: {timePassed}, numAtoms: {numAtoms}, numPrimitives: {numPrimitives}")

def test_recdt(
    traces
    , startDepth=1
    , maxDepth=float("inf")
    , step=1
    , optimizeDepth=float("inf")
    , optimize="count"
    , minScore=0
    , misclassification=0
    , timeout=float("inf")
):
    formula, timePassed = run_rec_dt(
        traces=traces,
        startDepth=startDepth, maxDepth=maxDepth, step=step,
        optimizeDepth=optimizeDepth,
        optimize=optimize, minScore=minScore,
        misclassification=misclassification,
        timeout=timeout,
    )
    trimedFormula = formula.trimPseudoNodes()
    flatFormula = trimedFormula.flattenToFormula()
    logging.debug(f"formula: {formula.prettyPrint()}")
    # logging.debug(f"DT formulas: {flatFormula.prettyPrint()}, timePassed: {timePassed}")
    logging.info(f"timePassed: {timePassed}, completeDT: {trimedFormula is formula}, sizeDT: {trimedFormula.getSize()}, depthDT: {trimedFormula.getDepth()}, misclassification: {traces.get_misclassification(trimedFormula)}")


def simulator(traces: ExperimentTraces):
    data = traces2random_list(traces, 10)
    sample = ExperimentTraces()
    sample.depthOfSolution = traces.depthOfSolution
    tr = None
    for i in data:
        tr = convert(i, sample, tr)
        formulas, timePassed = test_sat(sample)

        append_csv([formulas, str(timePassed)])

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
        tr = convert(i, sample, tr)
        #print(sample)
        #print()
    print(sample)
    formulas, timePassed = test_sat(sample)
    print(f"formulas: {[f.prettyPrint() for f in formulas]}, timePassed: {timePassed}")

def append_csv(l: list()):
    field_names = ['path','formula','time']
    with open('results_experiment_online_system/t.csv', mode='a', newline='') as csv_file:
        ob = csv.writer(csv_file, delimiter=';')
        #tmp = ";".join([str(st) for st in l])
        #csv_file.writelines(tmp + '\n')
        ob.writerow(l)
        #print(tmp)


if __name__ == "__main__":
    test_sample()
    #test_simulation()
    print()
    print("End")
