import requests
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
from datetime import datetime
import os
from os.path import isfile, join
import difflib


# Download page data
url = 'https://slack.com/jobs'
data = requests.get(url)
content = ''

if data.raise_for_status() != None:
	print 'Error encountered'
	content = data.raise_for_status()
else:
	content = data.text

# Parse out relevant content & write to file
class ZHTMLStrip(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
    s = ZHTMLStrip()
    s.feed(html)
    return s.get_data() 

soup = BeautifulSoup(content, 'html.parser')
myH4s = str(soup.findAll('h4')).split(", ")
# Determine oldest file in Results Directory
resultPath = '/Users/zreed/SlackJobs/Results/'
files = [ f for f in os.listdir(resultPath) if isfile(join(resultPath,f)) ]
oldest = files[0]
fileCount = int(len(files))

def write_file(myH4s):
	timeStamp = datetime.now().strftime("%H%M%S")
	f = open(resultPath + 'result-' + timeStamp + '.txt', 'w')
	for i in range(len(myH4s)):
		f.write(strip_tags(myH4s[i] + "\n"))
	f.close()

# Write new file or delete oldest and create new
if fileCount < 3:
	write_file(myH4s)
else:
	os.remove(resultPath + oldest)
	write_file(myH4s)

# Check diff between two files
files = [ f for f in os.listdir(resultPath) if isfile(join(resultPath,f)) ]
fileContents = ['','']

# print open(resultPath + files[0]).readlines()

# for i in range(2):
# 	with open(resultPath + str(files[i])) as f:
# 		for line in f:
# 			fileContents[i] += line
a = open(resultPath + files[0]).readlines()
b = open(resultPath + files[1]).readlines()

# for line in difflib.unified_diff(a, b, n=0):
#     print line
    # for prefix in ('---', '+++', '@@'):
    #     if line.startswith(prefix):
    #         break
    # else:
    #     print line

# print changes

# Send any changes via email

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
fromaddr = ''
toaddr = ''
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'Python Email'
 
body = 'and here is the data!'
msg.attach(MIMEText(body, 'plain'))
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, '')
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()



