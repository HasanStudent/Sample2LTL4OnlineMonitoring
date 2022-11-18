import random

from utils.Traces import ExperimentTraces, parseExperimentTraces, Trace

def copy_traces(traces: ExperimentTraces):
    val = ExperimentTraces()
    val.acceptedTraces = []
    val.rejectedTraces = []
    for i in traces.acceptedTraces:
        val.acceptedTraces.append(i)

    for i in traces.rejectedTraces:
        val.rejectedTraces.append(i)
    val.numVariables = traces.numVariables
    return val

def traces2finite(traces: ExperimentTraces, n):
    for trace in traces.acceptedTraces:
        if trace.lassoStart is not None:
            tmp = trace.traceVector[trace.lassoStart:]
            for i in range(n):
                trace.traceVector += tmp
            trace.lassoStart = None

def append_records(trace: list, result: list):
    for r in trace:
        result.append(r)

def traces2random_list(traces: ExperimentTraces, n):

    # Format the traces to a finite set
    traces2finite(traces, n)

    # data with all traces
    data = copy_traces(traces)

    # list of sending records or classification
    result = []

    #Go to all Traces
    while len(data.acceptedTraces) > 0 or len(data.rejectedTraces) > 0:
        rand_i = random.randint(0, 1)

        if rand_i == 0:
            if len(data.rejectedTraces) > 0:
                append_records(data.rejectedTraces[0].traceVector, result)
                result.append("reject")
                data.rejectedTraces.pop(0)
        else:
            if len(data.acceptedTraces) > 0:
                append_records(data.acceptedTraces[0].traceVector, result)
                result.append("accept")
                data.acceptedTraces.pop(0)

    return result
# Test: if all traces of the sample is in the random list (by count the both size of traces)
def test_all_traces_in_List():
    # Read traces
    traces = parseExperimentTraces("../traces/finite/5pc_misclass/disjunctionOfExistence/0003.trace")

    # Number of Traces of the sample
    s = len(traces.acceptedTraces) + len(traces.rejectedTraces)
    # Sending values of the Simulator
    tmp = traces2random_list(traces, 10)
    # Number of Traces of the Simulator values
    c = 0
    for i in tmp:
        if i == "accept" or i == "reject":
            c += 1
    # Test result
    print(c == s)

#if __name__ == "__main__":
    #test_all_traces_in_List()
