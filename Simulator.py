import random

from utils.Traces import ExperimentTraces,parseExperimentTraces

def copy_traces(traces: ExperimentTraces):
    result = ExperimentTraces()
    result.acceptedTraces = traces.acceptedTraces
    result.rejectedTraces = traces.rejectedTraces
    return result

def traces2finite(traces: ExperimentTraces):
    for trace in traces.acceptedTraces:
        if trace.lassoStart is not None:
            tmp = trace.traceVector[trace.lassoStart:]
            for i in range(10):
                trace.traceVector += tmp
            trace.lassoStart = None

def traces2random_list(
        traces:ExperimentTraces
):
    #Format the traces to a finite set
    traces2finite(traces)

    #data with all traces
    data = copy_traces(traces)

    num = 0

    a_num = None
    r_num = None

    result = ["Start Sample"]

    while len(traces.acceptedTraces) > 0 or len(traces.rejectedTraces) > 0:

        rand_i = random.randint(0, 1)

        if rand_i == 0:
            if a_num is None:
                a_num = num
                num += 1
            tmp_str = str(data.acceptedTraces[0].traceVector[0])

            result.append(str(a_num) + "::" + tmp_str[1:len(tmp_str)-1])
            data.acceptedTraces[0].traceVector.pop(0)
            if len(traces.acceptedTraces[0].traceVector) == 0:
                traces.acceptedTraces.pop(0)
                result.append(str(a_num) + "::accepted")
                a_num = num
                num += 1
        else:
            if r_num is None:
                r_num = num
                num += 1
            tmp_str = str(data.rejectedTraces[0].traceVector[0])
            result.append(str(r_num) + "::" + tmp_str[1:len(tmp_str)-1])
            data.rejectedTraces[0].traceVector.pop(0)
            if len(traces.rejectedTraces[0].traceVector) == 0:
                traces.rejectedTraces.pop(0)
                result.append(str(r_num) + "::rejected")
                r_num = num
                num += 1

if __name__ == "__main__":
    traces = parseExperimentTraces("traces/finite/5pc_misclass/disjunctionOfExistence/0003.trace")
    #traces = parseExperimentTraces("traces/generated/5to10OneThree/0002.trace")

    p = "hallo;" + str(traces.acceptedTraces[0].traceVector[0])[1:len(str(traces.acceptedTraces[0].traceVector[0]))-1]
    print(p)

    print(traces.acceptedTraces[0].traceVector)

    traces.acceptedTraces[0].traceVector.pop(0)

    print(traces.acceptedTraces[0].traceVector)
