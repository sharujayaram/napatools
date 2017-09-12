import subprocess
from threading import Thread
import sys
import requests
import time


USER = "Administrator"
PWD = "password"
BUCKET = "bucket-1"


INDEXDEFS = dict()

INDEXDEFS["INDEX1"] = "CREATE PRIMARY INDEX INDEX1 ON `" + BUCKET + "`"
INDEXDEFS["INDEX2"] = "CREATE INDEX INDEX2 ON `" + BUCKET + "`(address.country)"
INDEXDEFS["INDEX3"] = "CREATE index INDEX3 ON `" + BUCKET + "`(address.country, age_group, DATE_PART_STR(dob,'year'))"
INDEXDEFS["INDEX4"] = "CREATE INDEX INDEX4 ON `" + BUCKET + "`(address.prev_address.country)"
INDEXDEFS["INDEX5"] = "CREATE INDEX INDEX5 ON `" + BUCKET + "`(DISTINCT devices)"
INDEXDEFS["INDEX6"] = "CREATE INDEX INDEX6 ON `" + BUCKET + "`(DISTINCT ARRAY (DISTINCT ARRAY " \
                "(v.country || \".\" || c) FOR c IN v.activities END) FOR v IN visited_places END);"
INDEXDEFS["INDEX7"] = "CREATE INDEX INDEX7 ON `" + BUCKET + "`(address.country, order_list)"
INDEXDEFS["INDEX8"] = "CREATE INDEX INDEX8 ON `" + BUCKET + "`(address.country, month, order_list, sale_price)"


INDEXING_MAP = {
    "workloadsa": ("INDEX1"),
    "workloadsb": ("INDEX1",),
    "workloadsc": ("INDEX1",),
    "workloadsd": ("INDEX1",),
    "workloadse": ("INDEX1",),
    "workloadsf": ("INDEX1",),
    "workloadsg": ("INDEX2",),
    "workloadsh": ("INDEX3",),
    "workloadsi": ("INDEX4",),
    "workloadsj": ("INDEX5",),
    "workloadsk": ("INDEX6",),
    "workloadsl1": ("INDEX7",),
    "workloadsl2": ("INDEX8",),
    "workloadsmix": ("INDEX1", "INDEX2", "INDEX3", "INDEX4", "INDEX5", "INDEX6", "INDEX7", "INDEX8"),
}


def action_createindex():
    workload = ""
    host = ""
    for i, item in enumerate(sys.argv):
        if item == "-workload":
            workload = sys.argv[i+1]
        elif item == "-master_host":
            host = sys.argv[i+1]

    if INDEXING_MAP[workload] != None:
        for index in INDEXING_MAP[workload]:
            indexdef = INDEXDEFS[index]
            if "mix" in workload:
                api = 'http://{}:8093/query/service'.format(host)
                data = {'statement': indexdef}
                response = requests.post(url=api, data=data, auth=(USER, PWD))
                print response
            else:
                for suff in ("_1", "_2", "_3", "_4"):
                    nodedef = indexdef.replace(index, "{}{}".format(index, suff))
                    api = 'http://{}:8093/query/service'.format(host)
                    data = {'statement': nodedef}
                    response = requests.post(url=api, data=data, auth=(USER, PWD))


def run_thread(workload, host, t, kv, log, i, insertstart, maxexecutiontime, totalrecordst):
    cmd = get_ycsb_run_cmd(workload, host, t, kv, "{}_i{}".format(log, i), insertstart, maxexecutiontime, totalrecordst)
    print "Executing command: {}".format(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         cwd="../clones/YCSB_{}".format(i))
    for line in p.stdout.readlines():
        print line,
    retval = p.wait()


def action_run():
    workload = ""
    host = ""
    threads = 0
    kv = ""
    log = ""
    insertstart = ""
    maxexecutiontime = ""
    totalrecords = ""

    for i, item in enumerate(sys.argv):
        if item == "-workload":
            workload = sys.argv[i+1]
        elif item == "-master_host":
            host = sys.argv[i+1]
        elif item == "-threads":
            threads = int(sys.argv[i+1])
        elif item == "-kv":
            kv = sys.argv[i+1]
        elif item == "-log":
            log = sys.argv[i+1]
        elif item == "-insertstart":
            insertstart = sys.argv[i+1]
        elif item == "-test_duration":
            maxexecutiontime = sys.argv[i+1]
        elif item == "-total_items":
            totalrecords = sys.argv[i + 1]

    if threads > 35:
        for i in (1,2,3,4):
            time.sleep(10)
            if i != 4:
                t = int(threads/4)
            else:
                t = threads - int(threads/4) *3
            sub_offset = insertstart + ((int(totalrecords) / 10) * (i-1))
            new_thread = Thread(target=run_thread, args=(workload, host, t, kv, log, i, sub_offset,
                                                         maxexecutiontime, totalrecords))
            new_thread.start()

    else:
        cmd = get_ycsb_run_cmd(workload, host, threads, kv, log, insertstart, maxexecutiontime, totalrecords)
        print "Executing command: {}".format(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd="../YCSB")
        for line in p.stdout.readlines():
            print line,
        retval = p.wait()


def get_ycsb_run_cmd(workload, host, threads, kv, log, insertstart, maxexecutiontime, totalrecords):
    return "./bin/ycsb run couchbase2 -P workloads/soe/{} " \
           "-p couchbase.host={} -p couchbase.bucket={} -p couchbase.password={} " \
           "-p operationcount=900000000 -p maxexecutiontime={} -threads {} " \
           "-p couchbase.kv={} -p exportfile=../{}.log -p insertstart={} -p recordcount={}" .format(workload,
                                                                                                    host,
                                                                                                    BUCKET,
                                                                                                    PWD,
                                                                                                    maxexecutiontime,
                                                                                                    threads,
                                                                                                    kv,
                                                                                                    log,
                                                                                                    insertstart,
                                                                                                    totalrecords)


def consolidate():

    path = ""

    for i, item in enumerate(sys.argv):
        if item == "-path":
            path = sys.argv[i+1]

    file1 = "{}_i1.log".format(path)
    file2 = "{}_i1.log".format(path)
    file3 = "{}_i1.log".format(path)
    file4 = "{}_i1.log".format(path)

    METRICS = ("SOE_INSERT", "SOE_UPDATE", "SOE_SCAN", "SOE_PAGE", "SOE_SEARCH", "SOE_NESTSCAN",
               "SOE_ARRAYSCAN", "SOE_ARRAYDEEPSCAN", "SOE_REPORT", "SOE_REPORT2")

    FAILED = "FAILED"
    OVERALL = "OVERALL"

    METRICSTAT_95P = "95thPercentileLatency(us)"
    METRICSTAT_THR = "Throughput(ops/sec)"

    results_container = dict()
    for metric in METRICS:
        results_container[metric] = 0
        results_container["{}-{}".format(metric, FAILED)] = 0
    results_container[OVERALL] = 0

    for file in (file1, file2, file3, file4):
        with open(file) as f:
            for content in f:
                for metric in results_container.iterkeys():
                    report_key = "[{}]".format(metric)
                    if report_key in content:
                        if FAILED in content:
                            results_container[metric] +=1
                        elif METRICSTAT_95P in content or METRICSTAT_THR in content:
                            results_container[metric] += float(content.split(",")[2])

    for metric in results_container.iterkeys():
        if results_container[metric] != 0:
            if metric == OVERALL:
                print "Throughput: {}".format(results_container[metric])
            elif FAILED not in metric:
                print "{}, 95 percentile latency, ms: {}".format(metric, results_container[metric] / 4 / 1000)
            else:
                print "{}, total requests: {}".format(metric, results_container[metric])

for i,item in enumerate(sys.argv):
    if item == "-action":
        if sys.argv[i+1] == "createindex":
            action_createindex()
        elif sys.argv[i+1] == "load":
            action_load()
        elif sys.argv[i+1] == "run":
            action_run()
        elif sys.argv[i+1] == "consolidate":
            consolidate()

