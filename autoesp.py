import subprocess
import re
import os
from tqdm import tqdm

esptool = "esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 1000000 write_flash -z 0x1000"
firmware_file = "firmware-5-2-18-22-39.bin"
cmd = "{} {}".format(esptool, firmware_file)
devnull = open(os.devnull, 'w')

pbar = tqdm(total=100)

def main():
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=devnull)	
	
	s = ""
	append=""
	pos = 0
	progress = 0
	prev_progress = 0

	while True:
		output = process.stdout.read(10)
		append = output.decode('ascii')
		s = s + append
		
		m=re.search('\([0-9]+ \%\)', s[pos:])
		
		if m: 
			pos = pos + m.end()
			progress = int(m.group()[1:-2].strip())
			pbar.update(progress - prev_progress)
			prev_progress = progress

		if process.poll() is not None and len(output) != 0:
			#print(process.poll())
			break
		if output:
			pass


	retval = process.poll()

if __name__ == "__main__":	
	# execute only if run as a script
	main()

