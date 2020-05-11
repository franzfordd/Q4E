#!/usr/bin/env python2.7
import netmiko
import sys
import subprocess
import os
from netmiko import ConnectHandler
import getpass

def main():
	with open('ip.txt','r')as f:
		IPs = [line.strip() for line in f]

	with open('commands.txt','r') as j:
		commands = [line.strip() for line in j]

	selct = raw_input('So what do you want to do today?\n1 ---> Execute Show Commands\n2 ---> Execute Config Commands\n3 ---> Test ByPi\nSelect an Option: ')

	if selct == '1': #Executing Show Commands
		lo0 = ''
		uname = raw_input('Username: ')
		pwd = getpass.getpass()
		mod = raw_input('\nOption:\n1 ---> cisco_ios\n2 ---> hp_procurve\nPlease select a switch model: ')#cisco_ios,hp_procurve
		if mod == '1':
			model = 'cisco_ios'
		elif mod == '2':
			model = 'hp_procurve'
		else:
			print 'Invalid option!\n'
			exit()

		for ip in IPs:
			hp_procurve = {
							'device_type':model,
							'ip':ip,
							'username':uname,
							'password':pwd,
							'secret':pwd,
							}

			print '\n>>>> \033[0;33mChecking ip: '+ip+' \033[0;0m<<<<<'
			try:
				net_connect=ConnectHandler(**hp_procurve)
				for a_command in commands:
					output = net_connect.send_command(a_command)
					print output
				net_connect.disconnect()
			except netmiko.NetMikoTimeoutException:
				print 'Connection Failed For Unknown Reason: '+ip
			except netmiko.ssh_exception.NetMikoAuthenticationException:
				print 'SSH authentication took too long to finish, please check credentials.'
				
	elif selct == '2': #Executing Config Commands
		
		uname = raw_input('Username: ')
		pwd = getpass.getpass()
		mod = raw_input('\nOption:\n1 ---> cisco_ios\n2 ---> hp_procurve\nPlease select a switch model: ')#cisco_ios,hp_procurve
		if mod == '1':
			model = 'cisco_ios'
		elif mod == '2':
			model = 'hp_procurve'
		else:
			print 'Invalid option!\n'
			exit()
		for ip in IPs:
			hp_procurve = {
							'device_type':model,
							'ip':ip,
							'username':uname,
							'password':pwd,
							'secret':pwd,
							}

			print '\n>>>> \033[0;33mChecking ip: '+ip+' \033[0;0m<<<<<'
			try:
				net_connect=ConnectHandler(**hp_procurve)
				output = net_connect.send_config_set(commands)
				print output
				net_connect.disconnect()
			except netmiko.NetMikoTimeoutException:
				print 'Connection Failed For Unknown Reason: '+ip
			except netmiko.ssh_exception.NetMikoAuthenticationException:
				print 'SSH authentication took too long to finish, please check credentials.'

	elif selct == '3':#Checking ByPi
		lo2 = ''
		uname = raw_input('ByPi Username: ')
		pwd = getpass.getpass()
		mod = raw_input('\nOption:\n1 ---> cisco_ios\n2 ---> hp_procurve\nPlease select a switch model: ')#cisco_ios,hp_procurve
		if mod == '1':
			model = 'cisco_ios'
		elif mod == '2':
			model = 'hp_procurve'
		else:
			print 'Invalid option!\n'
			exit()
		for ip in IPs:
			hp_procurve = {
							'device_type':model,
							'ip':ip,
							'username':uname,
							'password':pwd,
							'secret':pwd,
							}

			print '\n>>>> \033[0;33mChecking ip: '+ip+' \033[0;0m<<<<<'
			try:
				net_connect=ConnectHandler(**hp_procurve)
				prompt = net_connect.find_prompt()
				net_connect.disconnect()
				if prompt.find('>') != -1:
					print 'Radius: '+'\033[1;36mON \033[0;0m'
			except netmiko.NetMikoTimeoutException:
				print 'Connection Failed For Unknown Reason: '+ip
			except netmiko.ssh_exception.NetMikoAuthenticationException:
				print '\033[1;31mCheck Radius Config \033[0;0m'
	
	else:
		print 'Invalid Option!'

if __name__ == '__main__':
	try:
		main()	
	except IOError:
		print '\033[1;33mPlease check if ip.txt and commands.txt is present in current directory\033[0;0m'
	except KeyboardInterrupt:
		print 'Exiting...'
