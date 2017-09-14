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
            new_thread = Thread(target=run_thread, args=(workload, t, log, i, insertstart,  maxexecutiontime,
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

action_run()