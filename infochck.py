#!/usr/bin/env python
import subprocess
import os
import socket
from contextlib import closing

def main():
	def ping_test(x):                                                           
		check = os.system('ping ' + x +' -c 3 > /dev/null') #Ping the "ip" three times then send the output to null
		if check == 0:
			return '\033[1;36mAlive \033[0;0m'
		else:
			return '\033[1;31mDown \033[0;0m'

	def snmp_check(x):
		String_Pool = ['mystring','private','public']
		data=[]
		for string in String_Pool:
			check = os.system('snmpwalk -v2c -c ' + string + ' ' + x + ' iso.3.6.1.2.1.1.1.0 > /dev/null 2>&1') #redirect the output to /dev/null. Include both the Standard Error and Standard Out

			if check==0:                                                  
				data.append('\033[1;36mOn \033[0;0m')               
			else:
				data.append('\033[1;31mOff \033[0;0m')
		return data

	def sock_check(x):
		socket_pool = [22,23,80,443]#order of output is 22 23 80 443
		data=[]
		for a_socket in socket_pool:
			with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
				if sock.connect_ex((x, a_socket)) == 0:
					data.append('\033[1;36mOpen \033[0;0m')
				else:
					data.append('\033[1;31mClose \033[0;0m')
		return data

	def model_check(x):
		proc = subprocess.Popen(['snmpwalk','-v2c','-c','mystring',x,'-Ovaq','sysDesc'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		out, err = proc.communicate()
		lo1 = 0
		if err.find('Timeout') == -1: #if we cannot find string 'Timeout' in "err" then continue with string checking loop
			while lo1 != 1:
				emeng = [', Version',', revision',', IronWare'] #where emeng[0] is for Cisco model and emeng[1] is for HP Procurve model and emeng[2] is for Brocade; add string for different switches
				for ff in emeng:
					str_loc = out.find(ff)
					if str_loc == -1:
						lo1 = 0
					else:
						return out[:str_loc] 
						lo1 = 1	
		else:
			return 'N/A'

	def hname_check(x):
		proc = subprocess.Popen(['snmpwalk','-v2c','-c','mystring',x,'-Ovaq','sysName'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		out, err = proc.communicate()
		if err.find('Timeout') == -1:
			return out.strip('\n') #remove new line
		else:
			return 'N/A'

######### Main program starts here #########		
	with open('ip.txt','r') as f:           #Get ips in "host.txt" then save it as a list called "IPs"
	   IPs = [line.strip() for line in f]
	print 'Program Starting.....'
	for ip in IPs:
		ping_stat=ping_test(ip)
		if ping_stat == '\033[1;36mAlive \033[0;0m':
			hname = hname_check(ip)
			model = model_check(ip)
			snmp = snmp_check(ip)
			sock = sock_check(ip)
			print 'IP:'+ip+'  '+'Hostname:'+hname+' '+'Status:'+ping_stat+' '+'Model:'+model+'   '+'SSH:'+sock[0]+' '+'Telnet:'+sock[1]+' '+'HTTP:'+sock[2]+' '+'HTTPS:'+sock[3]+' '+'mystring:'+snmp[0]+' '+'Private:'+snmp[1]+' '+'Public:'+snmp[2]+'\n'
		else:
			print 'IP:'+ip+'  '+'Hostname:N/A'+' '+'Status:'+ping_stat+' '+'Model:N/A'+'   '+'SSH:N/A'+' '+'Telnet:N/A'+' '+'HTTP:N/A'+' '+'HTTPS:N/A'+' '+'mystring:N/A'+' '+'Private:N/A'+' '+'Public:N/A'+'\n'

			
if __name__ == '__main__':
	try:
		main()	
	except IOError:
		print "Can't find ip.txt. Generating one..."
		#Create your script here to automate creation of hosts. Or you can just manually create an "ip.txt" file.
		
		#edt = open('ip.txt','r+')
		#lnes = edt.readlines()
		#edt.seek(0)
		#for i in lnes:
		#	if i.count('.') == 3 and i.find(':') == -1:
		#		edt.write(i)
		#edt.truncate()
		#edt.close()
		#print 'Done!\n'
		#main()
