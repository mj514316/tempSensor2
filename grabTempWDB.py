import os
import glob
import time
import MySQLdb

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
print device_file
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
db = MySQLdb.connect("localhost", "monitor", "password", "temps")
	
for x in range(0,1):
	temp_c, temp_f = read_temp()
	curs=db.cursor()
	executeString = "INSERT INTO tempdat values(CURRENT_DATE(),NOW(),'Basement',%s)" % (temp_f)
	print "%s of 180" %(x)
	print executeString
	with db:
		curs.execute(executeString)
	time.sleep(120)
db.close()
	


