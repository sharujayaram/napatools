import subprocess
from threading import Thread
import sys
import requests
import time


USER = "Administrator"
PWD = "password"
BUCKET = "bucket-1"


INDEX_1 = "CREATE PRIMARY INDEX ON `" + BUCKET + "`"
INDEX_2 = "CREATE INDEX ix1 ON `" + BUCKET + "`(address.country)"
INDEX_3 = "CREATE index ix2 ON `" + BUCKET + "`(address.country, age_group, DATE_PART_STR(dob,'year'))"
INDEX_4 = "CREATE INDEX ix3 ON `" + BUCKET + "`(address.prev_address.country)"
INDEX_5 = "CREATE INDEX ix4 ON `" + BUCKET + "`(DISTINCT devices)"
INDEX_6 = "CREATE INDEX ix5 ON `" + BUCKET + "`(DISTINCT ARRAY (DISTINCT ARRAY " \
                "(v.country || \".\" || c) FOR c IN v.activities END) FOR v IN visited_places END);"
INDEX_7 = "CREATE INDEX ix6 ON `" + BUCKET + "`(address.country, order_list)"
INDEX_8 = "CREATE INDEX ix7 ON `" + BUCKET + "`(address.country, month, order_list, sale_price)"



INDEXING_MAP = {
    "workloadsa": (INDEX_1,),
    "workloadsb": (INDEX_1,),
    "workloadsc": (INDEX_1,),
    "workloadsd": (INDEX_1,),
    "workloadse": (INDEX_1,),
    "workloadsf": (INDEX_1,),
    "workloadsg": (INDEX_2,),
    "workloadsh": (INDEX_3,),
    "workloadsi": (INDEX_4,),
    "workloadsj": (INDEX_5,),
    "workloadsk": (INDEX_6,),
    "workloadsl1": (INDEX_7,),
    "workloadsl2": (INDEX_8,),
    "workloadsmix": (INDEX_1, INDEX_2, INDEX_3, INDEX_4, INDEX_5, INDEX_6, INDEX_7, INDEX_8),

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
        for indexdef in INDEXING_MAP[workload]:
            api = 'http://{}:8093/query/service'.format(host)
            data = {'statement': indexdef}
            response = requests.post(url=api, data=data, auth=(USER, PWD))
            print response


def action_load():
    total = ""
    cached = ""
    host = ""
    workload = ""
    insertstart = ""
    for i, item in enumerate(sys.argv):
        if item == "-total_items":
            total = sys.argv[i+1]
        elif item == "-cache_items":
            cached = sys.argv[i+1]
        elif item == "-master_host":
            host = sys.argv[i+1]
        elif item == "-workload":
            workload = sys.argv[i+1]
        elif item == "-insertstart":
            insertstart = sys.argv[i+1]

    cmd = "./bin/ycsb load couchbase2 -P workloads/soe/{} " \
          "-p couchbase.host={} -p couchbase.bucket={} -p couchbase.password={} " \
          "-p operationcount=1 -p recordcount={} -p totalrecordcount={} -threads 20 -p insertstart={}".\
        format(workload, host, BUCKET, PWD, cached, total, insertstart)
    print "Executing command: {}".format(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd="../YCSB")
    for line in p.stdout.readlines():
        print line,
    retval = p.wait()


def run_thread(workload, host, t, kv, log, i, insertstart):
    cmd = get_ycsb_run_cmd(workload, host, t, kv, "{}_i{}".format(log, i), insertstart)
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
        elif item == "-maxexecutiontime":
            maxexecutiontime = sys.argv[i+1]
        elif item == "-test_duration":
            totalrecords = sys.argv[i + 1]

    if threads > 35:
        for i in (1,2,3,4):
            time.sleep(10)
            if i != 4:
                t = int(threads/4)
            else:
                t = threads - int(threads/4) *3
            new_thread = Thread(target=run_thread, args=(workload, host, t, kv, log, i, insertstart))
            new_thread.start()

    else:
        cmd = get_ycsb_run_cmd(workload, host, threads, kv, log, insertstart)
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

    for i, item in enumerate(sys.argv):
        if item == "-workload":
            workload = sys.argv[i+1]
        elif item == "-path":
            path = sys.argv[i+1]

    file1 = "{}_i1".format(path)
    file2 = "{}_i1".format(path)
    file3 = "{}_i1".format(path)
    file4 = "{}_i1".format(path)

    SOE_INSERT = "SOE_INSERT"
    SOE_UPDATE = "SOE_UPDATE"
    SOE_SCAN = "SOE_SCAN"
    SOE_PAGE = "SOE_PAGE"
    SOE_SEARCH = "SOE_SEARCH"
    SOE_NESTSCAN = "SOE_NESTSCAN"
    SOE_ARRAYSCAN = "SOE_ARRAYSCAN"
    SOE_ARRAYDEEPSCAN = "SOE_ARRAYDEEPSCAN"
    SOE_REPORT = "SOE_REPORT"
    SOE_REPORT2 = "SOE_REPORT2"

    METRIC_95P = "95thPercentileLatency(us)"
    METRIC_THR = "Throughput(ops/sec)"

    FAILED = "FAILED"
    OVERALL = "OVERALL"

    METRIC_MAP = {
        "workloadse": (SOE_INSERT, SOE_SCAN),
        "workloadsg": (SOE_INSERT, SOE_UPDATE, SOE_PAGE),
        "workloadsh": (SOE_INSERT, SOE_UPDATE, SOE_SEARCH),
        "workloadsi": (SOE_INSERT, SOE_UPDATE, SOE_NESTSCAN),
        "workloadsj": (SOE_INSERT, SOE_UPDATE, SOE_ARRAYSCAN),
        "workloadsk": (SOE_INSERT, SOE_UPDATE, SOE_ARRAYDEEPSCAN),
        "workloadsl1": (SOE_REPORT,),
        "workloadsl2": (SOE_REPORT2,),
        "workloadsmix": (SOE_PAGE, SOE_SEARCH, SOE_NESTSCAN, SOE_ARRAYSCAN, SOE_ARRAYDEEPSCAN, SOE_REPORT),
    }

    results_container = dict()
    results_container[OVERALL] = 0
    if workload in METRIC_MAP:
        for metric in METRIC_MAP[workload]:
            results_container[metric] = 0
            results_container["{}_{}".format(metric, FAILED)] = 0

    for file in (file1, file2, file3, file4):
        with open(file) as f:
            content = f.readlines()
            for metric in results_container.iterkeys():
                failed_metric = "{}_{}".format(metric, FAILED)
                if metric == OVERALL:
                    if OVERALL in content and METRIC_THR in content:
                        results_container[metric] += float(content.split(",")[2])
                elif metric in content and   METRIC_95P in content:
                    results_container[metric] += float(content.split(",")[2])
                elif failed_metric in content:
                    results_container[failed_metric] +=1

        for metric in results_container.iterkeys():
            if metric == OVERALL:
                print "Throughput: {}".format(results_container[metric])
            elif FAILED not in metric:
                print "{}, 95 percentile latency, ms: {}".format(metric / 4 / 1000)
            else:
                print "{}, total requests: {}"

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

