from utils.Traces import ExperimentTraces, Trace

def list_of_trace(trace):
    val = []
    for i in trace:
        val.append(i)
    return val

def encode(item, traces: ExperimentTraces):
    if traces.acceptedTraces.__len__():
        tmp = [item]
        trace = Trace(tmp)
        traces.acceptedTraces.append(trace)
    else:
        if isinstance(item, list):
            l = traces.acceptedTraces.__len__()
            traces.acceptedTraces[l-1].traceVector.append(item)
            traces.acceptedTraces[l - 1].lengthOfTrace = traces.acceptedTraces[l-1].traceVector
        else:
            l = traces.acceptedTraces.__len__()
            tmp = list_of_trace(traces.acceptedTraces[l - 1].traceVector)
            trace = Trace(tmp)
            if item == "reject":
                traces.rejectedTraces.append(trace)
            trace.traceVector = []
            traces.acceptedTraces.append(trace)

if __name__ == "__main__":
    trace = Trace([])
    print(trace)