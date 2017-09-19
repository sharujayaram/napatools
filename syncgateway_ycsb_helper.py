
import subprocess
from threading import Thread
import sys


INSTANCES = 10
HEAD = "./bin/ycsb run syncgateway -s "
LOG = open('runafew.log', 'w')
YCSB_HOME = ".."

threads = list()


def log(msg):
    LOG.write(msg + '\n')


def run_thread(cmd, i):
    homedir = "{}/YCSB_{}".format(YCSB_HOME,i)
    log("Running command {} from {}".format(cmd, homedir))
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         cwd=homedir)
    for line in p.stdout.readlines():
        log(line),
    retval = p.wait()


def run_instance(params, i):
    instance_log = "{}.log".format(i)
    cmd = HEAD
    for param in params:
        if param == "workload":
            cmd = "{} -P {} ".format(cmd, params["workload"])
        else:
            cmd = "{} -p {}={}".format(cmd, param, params[param])
    cmd = "{} -p exportfile={}".format(cmd, instance_log)

    new_thread = Thread(target=run_thread, args=(cmd, i))
    threads.append(new_thread)
    new_thread.start()


def consolidate():
    allresults = {}
    for i in range(0, INSTANCES):
       filename = "{}/YCSB_{}/{}.log".format(YCSB_HOME, i, i)
       lines = [line.rstrip('\n') for line in open(filename)]
       for line in lines:
           line = line.strip('\n')
           n,d,v = line.split(",")
           v = v.strip(' ')
           key = "{},{}".format(n,d)
           if key in allresults:
               allresults[key] = "{}-{}".format(allresults[key], v)
           else:
               allresults[key] = v

    aggregated_results = {}
    for item in allresults:
        total = 0
        counter = 0
        for value in allresults[item].split("-"):
            counter+=1
            total += float(value)
        avg = long(total/counter)
        allresults[item] = " sum({}) avg({}) count({})".format(total, avg, counter)

    sortedkeys = aggregated_results.keys()
    sortedkeys.sort()
    for key in sortedkeys:
        print "{}, {}".format(key, allresults[key])


allparams={}
for i, item in enumerate(sys.argv):
    if item == "-P":
        allparams["workload"] = sys.argv[i+1]

    if item == "-p":
        name,value = sys.argv[i+1].split("=")
        allparams[name] = value

insertstart = 0
threadcount = 0
if "insertstart" in allparams:
    insertstart = int(allparams["insertstart"])
if "threadcount" in allparams:
    threadcount = int(allparams["threadcount"])


for i in range(0, INSTANCES):
    sub_insertstart = int (insertstart / INSTANCES)
    sub_insertstart = sub_insertstart * i + insertstart
    if threadcount > INSTANCES:
        sub_threadcount = int(threadcount / INSTANCES)
    else:
        sub_threadcount = 1

    instace_params = allparams.copy()
    instace_params["insertstart"] = sub_insertstart
    instace_params["threadcount"] = sub_threadcount

    run_instance(instace_params, i)

for x in threads:
    x.join()

consolidate()