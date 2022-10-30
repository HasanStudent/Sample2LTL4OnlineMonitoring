from smtEncoding.dagSATEncoding import DagSATEncoding
from z3 import *
import sys
import pdb
import traceback
import logging
from collections import deque
import heapq
from random import random
from pytictoc import TicToc
from utils.SimpleTree import Formula, DecisionTreeFormula

def get_dynamic_models(
    traces,
    startDepth=1, maxDepth=float("inf"), step=1,
    optimizeDepth=float("inf"),
    optimize='count', minScore=0,
    encoder=DagSATEncoding,
    maxNumModels=1,
    timeout=float("inf"),
    cl_DagSatEncoding: DagSATEncoding=None,
    last_result=None,
):

    if optimizeDepth < maxDepth and optimize is None:
        logging.warning("Optimize objective not set. Ignoring optimization.")
    tictoc_z3, time_z3 = TicToc(), 0
    tictoc_total = TicToc()
    tictoc_total.tic()

    if cl_DagSatEncoding is not None and last_result is None:
        logging.warning("There is a Error in parameter in the Dynamic Sat Querying!")
        return
    if last_result is not None and cl_DagSatEncoding is None:
        logging.warning("There is a Error in parameter in the Dynamic Sat Querying!")
        return
    results = [] if last_result is None else last_result
    i = startDepth if cl_DagSatEncoding is None else cl_DagSatEncoding.formulaDepth
    if cl_DagSatEncoding is None:
        fg = encoder(i, traces)
    else:
        fg = cl_DagSatEncoding
        fg.traces = traces
    fg.encodeFormula(optimize=(optimize if i >= optimizeDepth else None))

    while len(results) < maxNumModels and i < maxDepth:
        if fg.set_timeout(timeout - tictoc_total.tocvalue()) <= 0: break
        tictoc_z3.tic()
        solverRes = fg.solver.check()
        time_z3 += tictoc_z3.tocvalue()
        acceptFormula = False
        if solverRes == unsat:
            logging.debug(f"not sat for i = {i}")
        elif solverRes != sat:
            logging.debug(f"unknown for i = {i}")
            break
        else:
            acceptFormula = True
            solverModel = fg.solver.model()
            formula = fg.reconstructWholeFormula(solverModel)
            if fg.optimize:
                score = traces.get_score(formula, fg.optimize)
                if score < minScore:
                    acceptFormula = False
                    logging.debug(f"score too low for i = {i} ({fg.optimize}={score})")
        if not acceptFormula:
            i += step
            if cl_DagSatEncoding is None:
                fg = encoder(i, traces)
            else:
                fg = cl_DagSatEncoding
                fg.traces = traces
            fg.encodeFormula(optimize=(optimize if i >= optimizeDepth else None))
        else:
            if fg.optimize:
                logging.info(f"found formula {formula.prettyPrint()} ({fg.optimize}={score})")
            else:
                logging.info(f"found formula {formula.prettyPrint()}")
            # print(f"found formula {formula}")
            formula = Formula.normalize(formula)
            logging.info(f"normalized formula {formula}")
            if formula not in results:
                results.append(formula)

            # prevent current result from being found again
            block = []
            # pdb.set_trace()
            # print(m)
            infVariables = fg.getInformativeVariables()

            logging.debug("informative variables of the model:")
            for v in infVariables:
                logging.debug((v, solverModel[v]))
            logging.debug("===========================")
            for d in solverModel:
                # d is a declaration
                if d.arity() > 0:
                    raise Z3Exception("uninterpreted functions are not supported")
                # create a constant from declaration
                c = d()
                if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                    raise Z3Exception("arrays and uninterpreted sorts are not supported")
                block.append(c != solverModel[d])
            fg.solver.add(Or(block))

        # time_total = tictoc_total.tocvalue()
        # time_z3
        # print(time_z3, time_total)
    return {"result": results, "Encoder": fg}
