import random

from utils.Traces import ExperimentTraces, parseExperimentTraces, Trace

# Copy a the positiv and negativ Traces to new Traces
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

# Convert a not finite Trace into a finite Trace
def traces2finite(traces: ExperimentTraces, n):
    for trace in traces.acceptedTraces:
        if trace.lassoStart is not None:
            tmp = trace.traceVector[trace.lassoStart:]
            for i in range(n):
                trace.traceVector += tmp
            trace.lassoStart = None

# Result list is getting all Records
def append_records(trace: list, result: list):
    for r in trace:
        result.append(r)

# Result list is getting the trace and his classification label
def trace_from_data(traces: ExperimentTraces, result: list, label):
    if label == "reject":
        append_records(traces.rejectedTraces[0].traceVector, result)
        result.append(label)
        traces.rejectedTraces.pop(0)
    else:
        append_records(traces.acceptedTraces[0].traceVector, result)
        result.append(label)
        traces.acceptedTraces.pop(0)

# Create a random list from Traces
def traces2random_list(traces: ExperimentTraces, n):

    # Format the traces to a finite set
    traces2finite(traces, n)

    # data with all traces
    data = copy_traces(traces)

    # list of sending records or classification
    result = []

    # Go to all Traces
    while len(data.acceptedTraces) > 0 or len(data.rejectedTraces) > 0:
        # Random number to choose a Trace
        rand_i = random.randint(0, 1)

        # negative labeled Traces has chosen
        if rand_i == 0:
            if len(data.rejectedTraces) > 0:
                trace_from_data(data, result, "reject")
        # positive labeled Trace has chosen
        else:
            if len(data.acceptedTraces) > 0:
                trace_from_data(data, result, "accept")

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

if __name__ == "__main__":
    test_all_traces_in_List()
