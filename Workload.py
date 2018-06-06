from multiprocessing import Process, Pipe
import os, sys
import subprocess
import time, random

FNULL = open(os.devnull, 'w')

def rand_affinity(baffinity=None, threads=None):
    affinity_l = 0#random.randint(0, 15)
    if baffinity is None:
        affinity_b = random.randint(1, 1) #15)
    else:
        affinity_b = baffinity
    affinity = affinity_l | (affinity_b << 4)
    affinity_string = hex(affinity)
    if threads is None:
        num_threads = bin(affinity).count("1")#random.randint(1, bin(affinity).count("1"))
    else:
        num_threads = threads
    return affinity_string, num_threads


# This function is meant to run as a separate process that runs each microbenchmark
# of a workload in sequence:
def run_workload(affinity_string, num_threads, paths, executables, name, stats_pipe):
    cmd = 'taskset --all-tasks ' + '{} {}'
    bwd = os.getcwd()
    t1 = time.time()
    for i in range(10):
		for e, p in zip(executables, paths):
			os.chdir(p)
			#print(os.getcwd())
			P = subprocess.Popen( [ 'taskset', '--all-tasks', affinity_string, e ], stdout=FNULL )
			P.wait()
			os.chdir(bwd)
    t2 = time.time()
    stats_pipe.send(t2-t1)


class Workload:
    def __init__(self, json_spec, base_path):
        self.name = json_spec["title"]
        self.path = base_path
        self.microbenchmarks = json_spec["microbenchmarks"]
        self.parent_pipe = None
        self.child_pipe = None
        self.process = None
        self.runtime = -1

    # NOTE: Currently will run on just one thread anyways!
    # Threads isn't actually implemented anywhere...
    def run(self, affinity=4, threads=None):
        if threads is not None:
            raise Exception("Number of threads is fixed to affinity or workload limit. Cannot be selected.")
        try:
            executables = ["./runme_{}.sh".format(s) for b, s in self.microbenchmarks.items()]
            paths = [self.path + "/" + b + "/" for b, s in self.microbenchmarks.items()] 
            # Open as a separate, persistent process:
            affinity_string, num_threads = rand_affinity(baffinity=affinity, threads=threads)
            self.parent_pipe, self.child_pipe = Pipe()
            self.process = Process(target=run_workload,
                        args=(affinity_string, num_threads, paths, executables, self.name, self.child_pipe) )
            self.process.start()
            self.runtime = -1
            return True
        except:
            print("Error:", sys.exc_info()[0])
            return False

    # Join the current process (if exists) and return the runtime.
    def join(self):
        if self.process is None:
            return False
        else:
            self.process.join()
            self.runtime = self.parent_pipe.recv()
            self.parent_pipe.close()
            self.child_pipe.close() 
            self.parent_pipe = None
            self.child_pipe = None
            self.process = None
            return True

    def get_last_runtime(self):
        return self.runtime

    def get_running_process(self):
        return self.process

    def is_running(self):
        if self.process is None:
            return False
        else:
            return self.process.is_alive()
   
    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.name
