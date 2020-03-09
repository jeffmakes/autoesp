#!/usr/bin/env python3
import subprocess
import re
import os
from tqdm import tqdm
import sys
 
#esptool = "esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 1000000 write_flash -z 0x1000"
devnull = open(os.devnull, 'w')

esptool="esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 2000000 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size detect" 

bin_init = "0xd000 ../tr20-badge-fw/firmware/build/ota_data_initial.bin"
bin_bl = "0x1000 ../tr20-badge-fw/firmware/build/bootloader/bootloader.bin"
bin_fw = "0x10000 ../tr20-badge-fw/firmware/build/firmware.bin"


def flash():
        input('Plug in badge and press return: ')
        
        print("Flashing initial data...")
        process = subprocess.Popen("{} {}".format(esptool, bin_init), shell=True, stdout=subprocess.PIPE, stderr=devnull)        
        process.wait()
        print("Flashing bootloader...")
        process = subprocess.Popen("{} {}".format(esptool, bin_bl), shell=True, stdout=subprocess.PIPE, stderr=devnull)         
        process.wait()
        
        print("Flashing application firmware...")
        process = subprocess.Popen("{} {}".format(esptool, bin_fw), shell=True, stdout=subprocess.PIPE, stderr=devnull)        

        pbar = tqdm(total=100)
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

                if process.poll() is not None:
                        #print(process.poll())
                        break
                if output:
                        pass

        #pbar.clear()
        pbar.close()
        retval = process.poll()
        if (retval):
                print ("Flashing FAILED - please retry")
        else:
                print ("Flashed OK!")

def main():     
        while True:
                flash()

if __name__ == "__main__":      
        # execute only if run as a script
        main()

