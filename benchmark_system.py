from multiprocessing import Process, Pipe
import subprocess
import time
import os, sys
import json 

from Workload import *

ITERS = 10

FNULL = open(os.devnull, 'w')

bench_processes = []
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

runtimes = [0.0] * len(workloads)

# Run through all workloads 100 times, taking down time-to-run.
# Governor should be running in the background here to log thermals and board power.
for i in range(ITERS):
	for idx, wrkld in enumerate(workloads):
        print("starting new workload run:")
        # Launch the benchmark as a subprocess:
        if wrkld.run():
            bench_processes.append(wrkld.get_running_process())
			name = wrkld.name
            print("Launched workload: {}".format(name))
            wrkld.join():
            runtime = wrkld.get_last_runtime()
			runtimes[idx] += runtime
			print("Runtime was {} seconds for {}.".format(runtime, name))
        else:
            print("Failed to launch {}".format(workloads[bm_index].name) )
			sys.exit(1)
		wait_time = 30
		print("Waiting for {} minutes before spawning another process.".format(wait_time/60.0))
		time.sleep(wait_time)

print("*"*40)
print("Workload average runtime summary over {} iterations".format(ITERS))
print("*"*40)
print("Name\tRuntime")
for idx, wrkld in enumerate(workloads):
	name = wrkld.name
	runtime = runtimes[idx] / ITERS
	print("{}\t{}".format(name, runtime)


