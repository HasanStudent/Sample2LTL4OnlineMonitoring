import random

from utils.Traces import ExperimentTraces, parseExperimentTraces, Trace


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

    result = []

    while len(data.acceptedTraces) > 0 or len(data.rejectedTraces) > 0:

        rand_i = random.randint(0, 1)

        if rand_i == 0:
            if a_num is None:
                a_num = num
                num += 1
            if len(data.acceptedTraces) > 0:
                if len(data.acceptedTraces[0].traceVector) > 0:
                    tmp_str = str(data.acceptedTraces[0].traceVector[0])
                    result.append(str(a_num) + "::" + tmp_str[1:len(tmp_str)-1])
                    data.acceptedTraces[0].traceVector.pop(0)
                if len(data.acceptedTraces[0].traceVector) == 0:
                    data.acceptedTraces.pop(0)
                    result.append(str(a_num) + "::accepted")
                    a_num = num
                    num += 1
        else:
            if r_num is None:
                r_num = num
                num += 1
            if len(data.rejectedTraces) > 0:
                if len(data.rejectedTraces[0].traceVector) > 0:
                    tmp_str = str(data.rejectedTraces[0].traceVector[0])
                    result.append(str(r_num) + "::" + tmp_str[1:len(tmp_str)-1])
                    data.rejectedTraces[0].traceVector.pop(0)
                if len(data.rejectedTraces[0].traceVector) == 0:
                    data.rejectedTraces.pop(0)
                    result.append(str(r_num) + "::rejected")
                    r_num = num
                    num += 1
    return result

def test_encoder(data):
    traces = ExperimentTraces()
    num_list = []
    tmp_data = {}
    accepted = {}
    rejected = {}
    accepted_tmp = []
    rejected_tmp = []
    for t in data:
        tmp = t.split("::")
        if len(tmp) == 2:
            if tmp[1] == "accepted":
                accepted[int(tmp[0])] = tmp_data[int(tmp[0])]
                accepted_tmp.append(int(tmp[0]))
                #print(tmp_data[int(tmp[0])])
                continue
            if tmp[1] == "rejected":
                rejected[int(tmp[0])] = tmp_data[int(tmp[0])]
                rejected_tmp.append(int(tmp[0]))
                continue

            record = tmp[1].split(", ")
            try:
                tmp_data[int(tmp[0])].append([eval(v) for v in record])
            except:
                tmp_data[int(tmp[0])] = [[eval(v) for v in record]]

    accepted_tmp.sort()
    rejected_tmp.sort()
    for i in accepted_tmp:
        trace = Trace(traceVector=accepted[i])
        trace.intendedEvaluation = True
        traces.acceptedTraces.append(trace)

    for i in rejected_tmp:
        trace = Trace(traceVector=rejected[i])
        trace.intendedEvaluation = True
        traces.rejectedTraces.append(trace)

    #print(traces.acceptedTraces)

    return traces.acceptedTraces

if __name__ == "__main__":
    traces = parseExperimentTraces("traces/finite/5pc_misclass/disjunctionOfExistence/0003.trace")
    #traces = parseExperimentTraces("traces/generated/5to10OneThree/0002.trace")
    #print(traces.acceptedTraces)
    #print(traces.acceptedTraces[0].traceVector[0])
    data = traces2random_list(traces)
    test = test_encoder(data)
    val = True
    for i, trace in enumerate(traces.acceptedTraces):
        if test[i].traceVector != trace.traceVector:
            val = False

    print(val)

    '''
    p = "hallo;" + str(traces.acceptedTraces[0].traceVector[0])[1:len(str(traces.acceptedTraces[0].traceVector[0]))-1]
    print(p)

    print(traces.acceptedTraces[0].traceVector)

    traces.acceptedTraces[0].traceVector.pop(0)

    print(traces.acceptedTraces[0].traceVector)
    '''

