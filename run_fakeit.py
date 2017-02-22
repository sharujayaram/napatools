import subprocess
from threading import Thread

p = subprocess.Popen('make build', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print line,
retval = p.wait()


def run(batch_size, total_batches, group):
    for i in range(0, total_batches):
        p = subprocess.Popen("../fakeit/bin/fakeit -n {} -d couchbase -s 172.23.100.190 -b bucket-1 -p password --offset {}".format(batch_size,
                                                                                                               batch_size*group*total_batches + i*batch_size),
                              shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print line,
        retval = p.wait()


def run_fakeit(threads, items):
    batch_size = 1000
    total_batches = items / (batch_size*threads)
    print total_batches
    for i in range(0, threads):
        new_thread = Thread(target=run, args=(batch_size, total_batches, i,))
        new_thread.start()


threads = 10
items = 10000

run_fakeit(threads, items)

