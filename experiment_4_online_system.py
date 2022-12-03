from utils.Simulator_Data import traces2random_list
from utils.Encorder import convert
from solverRuns import *
from utils.Traces import ExperimentTraces, parseExperimentTraces
import sys
import os
import logging

def sat(
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
        , misclassification=0
):
    timePassed, numAtoms, numPrimitives = run_dt_solver(
        traces=traces,
        misclassification=misclassification,
    )
    return [timePassed, numAtoms, numPrimitives]

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

    return [formula, timePassed]

def experiment_with_traces(traces: ExperimentTraces):
    break_num = [10, 100, 1000, 10000]
    threshold = [0.9, 0.95]
    misclassification = [0.05]
    min_score = [0.9, 0.8, 0.7, 0.6]

if __name__ == "__main__":
    tracesFolderName = "all_traces/misclass-5"
    subDirs = ['abscence', 'disjunctionOfExistence', 'existence', 'universality']
    flieTracesFileList = []
    file_list = list()

    for root, dirs, files in os.walk("all_traces/"):
        if len(dirs) > 0:
            file_list.append([root, dirs])
        for file in files:
            if file.endswith('.trace'):
                tmp = root.split('\\')
                hlp = ""
                for t in tmp:
                    hlp += t + '/'
                file_list.append([hlp, 'trace'])
                break

    traceFolders = [f[0] for f in file_list if f[1] == 'trace']
    print(traceFolders)

    writePath = "results_experiment_online_system"

    for f in traceFolders[:1]:
        for root, dirs, files in os.walk(f):
            for file in files:
                if file.endswith('.trace'):
                    path = f + '/' + file
                    traces: ExperimentTraces = parseExperimentTraces(path)
                    result, time = test_recdt(traces)
                    print(f'formula: {result} has solved with time: {time}')
                    break

    '''
    for root, dirs, files in os.walk(tracesFolderName):
        print(f'Root: {root}')
        print(f'Dir: {dirs}')
        for file in files:
            if file.endswith('.trace'):
                flie_file_name = str(os.path.join(root, file))
                flieTracesFileList.append(flie_file_name)
    if tracesFolderName.endswith('.trace'):
        flieTracesFileList.append(tracesFolderName)

    print(flieTracesFileList)
    '''