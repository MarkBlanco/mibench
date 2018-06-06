from multiprocessing import Process, Pipe
import subprocess
import time
import os, sys
import json 

from Workload import *

ITERS = 10

workloads = []
path = os.getcwd()

# Read in all workloads:
workloads_fname = "workload_collections.json"
with open(workloads_fname, 'r') as wf:
    json_data = json.load(wf)

for workload_spec in json_data['workloads']:
    if "microbenchmarks" in workload_spec:
        workloads.append(Workload(workload_spec, path))
        print("Added workload: {}".format(workloads[-1].name))

print(workloads)

runtimes = [[]] * len(workloads)

# Run through all workloads ITERS times, taking down time-to-run.
# Governor should be running in the background here to log thermals and board power.
print("name\tstartts\tendts\truntime(s)\titeration")
for i in range(ITERS):
    for idx, wrkld in enumerate(workloads):
        # Launch the benchmark as a subprocess:
        start = time.time()
        if wrkld.run(affinity=15):
            name = wrkld.name
            #print("Launched workload: {}".format(name))
            wrkld.join()
            runtime = wrkld.get_last_runtime()
            runtimes[idx].append(runtime)
            #print("Runtime was {} seconds for {}.".format(runtime, name))
        else:
            print("Failed to launch {}".format(name) )
            sys.exit(1)
        end = time.time()
        print("{}\t{}\t{}\t{}\t{}".format(name, start, end, runtime, i))
        wait_time = 30
        #print("Waiting for {} minutes before spawning another process.".format(wait_time/60.0))
        time.sleep(wait_time)

print("*"*40)
print("Workload geometric average runtime summary over {} iterations".format(ITERS))
print("*"*40)
print("Name\tRuntimeAvg\tGeomAvg")
for idx, wrkld in enumerate(workloads):
    name = wrkld.name
    runtime = 0.0
    geom_runtime = 0.0
    for i in ITERS:
        runtime += runtimes[idx][i]
        geom_runtime *= runtimes[idx][i]
    runtime /= ITERS
    geom_runtime = geom_runtime**(1/float(ITERS))
    print("{}\t{}\t{}".format(name, runtime, geom_runtime))
