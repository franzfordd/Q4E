#!/usr/bin/env python3
import netmiko
import sys
import subprocess
import os
import getpass


def main():
#	def check_dir():
#		proc1 = subprocess.Popen(['ls'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#		out,err = proc1.communicate()
#		if out.find('Config_backup') == -1:
#			os.system('mkdir /home/fhemeng/Config_backup')
#		else:
#			print ('Config_backup directory found')


	with open('ip.txt','r')as f:
		IPs = [line.strip() for line in f]

	#check_dir()
	uname = input('Username: ')
	pwd = getpass.getpass()
	for ip in IPs:
		cisco_ios = {
						'device_type':'cisco_ios',
						'ip':ip,
						'username':uname,
						'password':pwd,
						'secret':pwd,
						}

		print ('\n>>>> \033[0;33mChecking ip: '+ip+' \033[0;0m<<<<<')
		try:
			os.system('touch /home/fhemeng/'+ip+'-config')
			net_connect=netmiko.ConnectHandler(**cisco_ios)
			output = net_connect.send_command('show config')
			net_connect.disconnect()
			file = open("/home/fhemeng/"+ip+"-config","a")
			file.write(output)
			#print ('\033[1;33mDone! File is located in /root/Config_backup dir.\033[0;0m')

		except netmiko.NetMikoTimeoutException:
			print ('Connection Failed For Unknown Reason: '+ip)
		except netmiko.ssh_exception.NetMikoAuthenticationException:
			print ('SSH authentication took too long to finish, please check credentials.')

if __name__ == '__main__':
	try:
		main()	
	except IOError:
		print ("Can't find ip.txt. Generating one...")
		#os.system('/opt/PIPlatform/sbin/fi_psql_shell.sh "select management_ip from pidb_networkdevice;" > ip.txt') #Gets list of IP from FI's SQL db
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
