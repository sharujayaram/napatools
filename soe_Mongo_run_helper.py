import subprocess
from threading import Thread
import sys
import requests
import time

MONGODBURL= "mongodb://localhost:27021/ycsb?w=1"

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
        elif item == "-workload":
            workload = sys.argv[i+1]
        elif item == "-insertstart":
            insertstart = sys.argv[i+1]

    cmd = "./bin/ycsb load mongodb -P workloads/soe/{} -p mongodb.url={} -p operationcount=1 -p recordcount={} " \
          "-p totalrecordcount={} -threads 20 -p insertstart={}".format(workload, MONGODBURL, cached,
                                                                        total, insertstart)
    print "Executing command: {}".format(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd="../YCSB")
    for line in p.stdout.readlines():
        print line,
    retval = p.wait()


def run_thread(workload, t, log, i, insertstart):
    cmd = get_ycsb_run_cmd(workload, t, "{}_i{}".format(log, i), insertstart)
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
        elif item == "-threads":
            threads = int(sys.argv[i+1])
        elif item == "-log":
            log = sys.argv[i+1]
        elif item == "-insertstart":
            insertstart = sys.argv[i+1]

    if threads > 35:
        for i in (1,2,3,4):
            time.sleep(10)
            if i != 4:
                t = int(threads/4)
            else:
                t = threads - int(threads/4) *3
            new_thread = Thread(target=run_thread, args=(workload, t, log, i, insertstart))
            new_thread.start()
    else:
        cmd = get_ycsb_run_cmd(workload, threads, log, insertstart)
        print "Executing command: {}".format(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd="../YCSB")
        for line in p.stdout.readlines():
            print line,
        retval = p.wait()


def get_ycsb_run_cmd(workload, threads, log, insertstart):
    return "./bin/ycsb run mongodb -P workloads/soe/{} -p mongodb.url={} -p operationcount=900000000 " \
           "-p maxexecutiontime=600 -threads {} -p exportfile=../{}.log -p insertstart={}".format(workload,
                                                                                                  MONGODBURL,
                                                                                                  threads,
                                                                                                  log,
                                                                                                  insertstart)
for i,item in enumerate(sys.argv):
    if item == "-action":
        if sys.argv[i+1] == "load":
            action_load()
        elif sys.argv[i+1] == "run":
            action_run()