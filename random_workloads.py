from multiprocessing import Process, Pipe
import subprocess
import random
import time
import os, sys
import json 

from Workload import *

FNULL = open(os.devnull, 'w')

bench_prob = 0.4
period_max = 30 
bench_processes = []
workloads = []
path = os.getcwd()
workloads_fname = "workload_collections.json"
with open(workloads_fname, 'r') as wf:
    json_data = json.load(wf)

for workload_spec in json_data['workloads']:
    if "microbenchmarks" in workload_spec:
        workloads.append(Workload(workload_spec, path))
        print("Added workload: {}".format(workloads[-1].name))

print(workloads)

random.seed()
while True:
    #for i in range(len(bench_processes)-1, -1, -1):
    #if bench_processes[i].poll() is not None:
    #    del bench_processes[i]
    # Roll a die:
    d = random.random()
    if d <= bench_prob: # and len(bench_processes) == 0:
        print("starting new workload run:")
        # launch a new benchmark
        bm_index = random.randint(0,len(workloads)-1)
        # Launch the benchmark as a subprocess:
        if workloads[bm_index].run():
            bench_processes.append(workloads[bm_index].get_running_process())
            print("Launched workload: {}".format(workloads[bm_index].name))
            if not workloads[bm_index].join():
                raise Exception("Subprocess failed to join!")
            else:
                runtime = workloads[bm_index].get_last_runtime()
                name = workloads[bm_index].name
                print("Runtime was {} seconds for {}.".format(runtime, name))
        else:
            print("Failed to launch {}".format(workloads[bm_index].name) )
    else:
        continue
#   if len(bench_processes) > 0:
        # Kill the process and go idle:
        #bench_processes[0].kill()
    wait_time = random.randint(0, period_max)
    print("Waiting for {} minutes before spawning another process.".format(wait_time/60.0))
    time.sleep(wait_time)

