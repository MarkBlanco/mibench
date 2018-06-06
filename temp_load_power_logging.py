from __future__ import print_function
import serial
import time
import devfreq_utils as cpu_usage
import telnetlib as tel
import atexit
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def getTelnetPower(SP2_tel, last_power):
	# Get the latest data available from the telnet connection 
	# without blocking
	tel_dat = str(SP2_tel.read_very_eager())
	# find latest power measurement in the data
	findex = tel_dat.rfind('\n')
	findex2 = tel_dat[:findex].rfind('\n')
	findex2 = findex2 if findex2 != -1 else 0
	ln = tel_dat[findex2:findex].strip().split(',')
	if len(ln) < 2:
		eprint("ERROR: no power data! Using previous reading.")
		total_power = last_power
	else:
		total_power = float(ln[-1])
	return total_power

# Time to wait between logging a line in ms (target, not guaranteed)
DELAY=0.050
# power used by ethernet and wifiusb when active (assuming they are active)
out_file = None
MAX_SAMPLES = 110000

header = "time watts max_big_temp temp4 temp5 temp6 temp7 temp_gpu freq_little_cluster freq_big_cluster"
header = "\t".join( header.split(' ') )

def usage():
	eprint("USAGE: {} [output filename]".format(sys.argv[0]))
	sys.exit(1)

def cleanup():
	#cpu_usage.unsetUserSpace()	
	if out_file is not None:
	    out_file.close()

if __name__ == "__main__":
	if len(sys.argv) > 2:
		usage()
	if len(sys.argv) == 1:
		out_file = None
		eprint("No logfile given. Outputting to stdout only.")
	else:	
		out_fname = sys.argv[1]#raw_input("Filename for logging: ")
		out_file = open(out_fname, 'w')
		out_file.write(header)
		out_file.write("\n")
		eprint("Outputting to logfile ({}) and to stdout".format(sys.argv[1]))
	atexit.register(cleanup)
	try:
		SP2_tel = tel.Telnet("192.168.4.1")
		eprint("Getting power measure from SP2.")
		connected = True
	except:
		eprint("Can't connect to smartpower for power logging. Skipping.")
		cont = str(input("Continue? (y/n)"))
		while cont != 'y' or cont != 'n':
		    cont = str(input("Enter y/n"))
		if cont != 'y':
		    eprint("Quitting")
		    sys.exit()
		connected = False
	time_stamp = time.time()
	total_power = 0.0
	samples_taken = 0
	while True and samples_taken < MAX_SAMPLES:	
		samples_taken += 1
		last_time = time.time()#time_stamp
		temps = cpu_usage.getTemps()
		F = [0, 0, 0, 0]
		# Get frequency of small cluster, big cluster, GPU, and mem (convert from Khz to hz, except for GPU freq which is already reported by sysfs in hz)
		F[0] = float(cpu_usage.getClusterFreq(0))*1000
		F[1] = float(cpu_usage.getClusterFreq(4))*1000
		if connected:
		    total_power = getTelnetPower(SP2_tel, total_power)
		time_stamp = last_time
		# Data writeout:
		fmt_str = "{}\t"*10
		out_ln = fmt_str.format(\
			time_stamp, total_power,\
			max(temps[0:4]), \
			temps[0], temps[1], temps[2], temps[3], temps[4], \
			F[0], F[1] ) 
		if not out_file is None:
			out_file.write(out_ln)
			out_file.write("\n")
		else:	
		    print(out_ln)
		elapsed = time.time() - last_time
		time.sleep( max(0, DELAY - elapsed ) )	
