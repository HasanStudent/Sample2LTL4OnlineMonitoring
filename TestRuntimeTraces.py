import logging

from pytictoc import TicToc
from formulaBuilder.satQuerying import DagSATEncoding
from solverRuns import run_solver
from utils.RuntimeTraces import RuntimeTraces
from utils.Traces import ExperimentTraces, parseExperimentTraces
from formulaBuilder.DynamicSatQuerying import get_dynamic_models, Test_dynamic_models
from smtEncoding.dagSATEncoding import DagSATEncoding
from z3 import *

def test_1(dynTraces: RuntimeTraces):
    results = None
    Encoder: DagSATEncoding = None
    for i, traces in enumerate(dynTraces.splitTraces):
        t = TicToc()
        t.tic()
        results, Encoder = get_dynamic_models(
            traces=traces,
            cl_DagSatEncoding=Encoder,
            last_result=results,
        )
        time_passed = t.tocvalue()
        print(f"On {i} Trace Data:")
        print(f"formulas: {[f.prettyPrint() for f in results]}, timePassed: {time_passed}")

def test_2(dynTrace: RuntimeTraces):
    t = TicToc()
    t.tic()
    results, fg = Test_dynamic_models(
        Splittraces=dynTrace,
    )
    time_passed = t.tocvalue()
    print("Test start")
    print(f"formulas: {[f.prettyPrint() for f in results]}, timePassed: {time_passed}")

def test_3(dynTrace: RuntimeTraces):
    acc_trace = []
    rej_trace = []
    tmpTraces = dynTrace.copyTraces()
    for i, traces in enumerate(dynTrace.splitTraces):
        acc_trace = acc_trace + traces.acceptedTraces
        rej_trace = rej_trace + traces.rejectedTraces

        tmpTraces.acceptedTraces = acc_trace
        tmpTraces.rejectedTraces = rej_trace
        formulas, timePassed = run_solver(traces=tmpTraces,
                                          startDepth=1, maxDepth=float("inf"), step=1,
                                          optimizeDepth=float("inf"),
                                          optimize="count", minScore=0,
                                          maxNumModels=1,
                                          timeout=float("inf"),
                                          )
        print(f"This is {i+1} Trace:")
        print(f"formulas: {[f.prettyPrint() for f in formulas]}, timePassed: {timePassed}")
    print("\n")
    print("This is the normal Trace:")
    formulas, timePassed = run_solver(traces=dynTrace.traces,
                                      startDepth=1, maxDepth=float("inf"), step=1,
                                      optimizeDepth=float("inf"),
                                      optimize="count", minScore=0,
                                      maxNumModels=1,
                                      timeout=float("inf"),
                                      )
    print(f"formulas: {[f.prettyPrint() for f in formulas]}, timePassed: {timePassed}")

#Test: All traces is equal to main traces
if __name__ == "__main__":
    test: ExperimentTraces
    test = parseExperimentTraces("traces/finite/5pc_misclass/disjunctionOfExistence/0003.trace")

    a = RuntimeTraces(test)


    test_2(a)
    '''
    mfg = DagSATEncoding(1, test)
    print("\n\n\n\n")
    print("All SAT")
    mfg.encodeFormula('count')
    print(mfg.solver)
    '''
    #test_3(a)