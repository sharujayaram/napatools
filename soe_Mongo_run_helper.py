import subprocess
from threading import Thread
import sys
import requests
import time

MONGODBURL= "mongodb://localhost:27021/ycsb?w=1"


def run_thread(workload, t, log, i, insertstart,  maxexecutiontime, totalrecords):
    cmd = get_ycsb_run_cmd(workload, t, "{}_i{}".format(log, i), insertstart,  maxexecutiontime, totalrecords)
    print "Executing command: {}".format(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         cwd="../clones/YCSB_{}".format(i))
    for line in p.stdout.readlines():
        print line,
    retval = p.wait()


def action_run():
    workload = ""
    maxexecutiontime = ""
    threads = 0
    totalrecords = ""
    log = ""
    insertstart = ""
    for i, item in enumerate(sys.argv):
        if item == "-workload":
            workload = sys.argv[i+1]
        elif item == "-threads":
            threads = int(sys.argv[i+1])
        elif item == "-log":
            log = sys.argv[i+1]
        elif item == "-insertstart":
            insertstart = sys.argv[i+1]
        elif item == "-test_duration":
            maxexecutiontime = sys.argv[i + 1]
        elif item == "-total_items":
            totalrecords = sys.argv[i + 1]

    if threads > 3:
        for i in (1,2,3,4):
            time.sleep(10)
            if i != 4:
                t = int(threads/4)
            else:
                t = threads - int(threads/4) *3
            sub_offset = int(insertstart) + ((int(totalrecords) / 10) * (i - 1))
            new_thread = Thread(target=run_thread, args=(workload, t, log, i, sub_offset,  maxexecutiontime,
                                                         totalrecords))
            new_thread.start()
    else:
        cmd = get_ycsb_run_cmd(workload, threads, log, insertstart, maxexecutiontime, totalrecords)
        print "Executing command: {}".format(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd="../YCSB")
        for line in p.stdout.readlines():
            print line,
        retval = p.wait()

def get_ycsb_run_cmd(workload, threads, log, insertstart, maxexecutiontime, totalrecords):
    return "./bin/ycsb run mongodb -P workloads/soe/{} -p mongodb.url={} " \
           "-p operationcount=900000000 -p maxexecutiontime={} -threads {} " \
           "-p exportfile=../{}.log -p insertstart={} -p recordcount={}".format(workload,
                                                                                MONGODBURL,
                                                                                maxexecutiontime,
                                                                                threads,
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
        if sys.argv[i+1] == "run":
            action_run()
        elif sys.argv[i+1] == "consolidate":
            consolidate()
