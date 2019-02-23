from fabric import Connection
from fabric.context_managers import env
import sys


MONGODBURL= "mongodb://{}:{}/ycsb?{}"
EXPECTED_PARAMS = ["mdb_port", "mdb_conn_params",
                   "ycsb_instances", "ycsb_threads_per_instance",
                   "env_servers"]

# MOVE TO OPTIONAL PARAMS
record_count = 20000000
operation_count = 999999999
maxexecutiontime = 600


settings = dict()
servers = list()


def init_settings():
    for item in enumerate(sys.argv):
        p, v = item.split(':')
        settings[p] = v
    for p in EXPECTED_PARAMS:
        if p not in settings:
            print("Error. Missing parameter {}".format(p))
            sys.exit()


def init_remote_env():
    creds = open("/root/alex/creds", "r").readline()
    env.user, env.password = creds.split()


def run_all():
    print("Running YCSB on every client")
    mdb_url = MONGODBURL.format("localhost", settings["mdb_port"], settings["mdb_conn_params"])
    ycsb_cmd = "bin/ycsb run mongodb -P workloads/workloada " \
               "-p exportfile=results.testlog " \
               "-p mongodb.url={} " \
               "-p operationcount={} " \
               "-p recordcount={} " \
               " -threads {} > output.testlog".format(mdb_url,
                                                      operation_count,
                                                      record_count,
                                                      settings["ycsb_threads_per_instance"])
    for server in settings["env_servers"].split(","):
        c = Connection(server)
        for i in range(settings["ycsb_instances"]):
            path = "/tmp/YCSB{}".format(i)
            result = c.run("{}/{}".format(path, ycsb_cmd))
            print(result)


def collect():
    print("Collecting logs")
    for server in settings["env_servers"].split(","):
        c = Connection(server)
        for i in range(settings["ycsb_instances"]):
            rpath = "/tmp/YCSB{}".format(i)
            lpath = "YCSB{}".format(i)
            result = c.get(remote_path="{}{}".format(rpath,"/*testlog"), local_path="{}/{}/".format(server, lpath))
            print(result)


def report_total_throughput():
    print("Reading logs")
    total_thr = 0
    for server in settings["env_servers"].split(","):
        for i in range(settings["ycsb_instances"]):
            lpath = "YCSB{}".format(i)
            file = "{}/{}/results.testlog".format(server, lpath)
            for line in open(file, "r"):
                if "Throughput" in line:
                    val = line.split[2]
                    total_thr += float(val)
                    print("{} instance {}: {}".format(server, lpath, val))
                if "ERROR" in line:
                    print("Errors detected in {}".format(file))
                    break
    print("TOTAL THROUGHPUT: {}".format(total_thr))



init_settings()
init_remote_env()
run_all()
collect()
report_total_throughput()