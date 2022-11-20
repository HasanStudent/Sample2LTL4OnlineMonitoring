from utils.Traces import ExperimentTraces, Trace

# Get all Records from a Trace and save into new list
def list_of_trace(trace):
    val = []
    for i in trace:
        val.append(i)
    return val

# Encode the Data from Simulator
def encode(item, traces: ExperimentTraces):
    # Start point is the Sample is Empty, so no data has encoded recently
    if traces.acceptedTraces.__len__():
        tmp = [item]
        trace = Trace(tmp)
        traces.acceptedTraces.append(trace)
    else:
        # Get the last edit Trace number
        l = traces.acceptedTraces.__len__()

        # New Record has arrived
        if isinstance(item, list):
            traces.acceptedTraces[l-1].traceVector.append(item)
            traces.acceptedTraces[l - 1].lengthOfTrace = len(traces.acceptedTraces[l-1].traceVector)

        # Classification label has arrived
        else:
            # Create a temporary the last edit Trace
            tmp = list_of_trace(traces.acceptedTraces[l - 1].traceVector)
            trace = Trace(tmp)
            # Case labeled is rejected, save edit Trace into rejected Traces
            if item == "reject":
                traces.rejectedTraces.append(trace)
            # New Empty Trace is append to Traces, for correctness that the Encoder work on the right one.
            trace.traceVector = []
            traces.acceptedTraces.append(trace)

#if __name__ == "__main__":





