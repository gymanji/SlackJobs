import requests
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
from datetime import datetime
import os
from os.path import isfile, join


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
resultPath = '/Users/Zach/Development/GitHub Repos/SlackJobs/Results/'
files = [ f for f in os.listdir(resultPath) if isfile(join(resultPath,f)) ]
oldest = files[0]
fileCount = int(len(files))

def write_file(myH4s):
	timeStamp = datetime.now().strftime("%H%M%S")
	f = open(resultPath + 'result-' + timeStamp + '.txt', 'w')
	for i in range(len(myH4s)):
		f.write(strip_tags(myH4s[i] + '\n'))
	f.close()

# Write new file or delete oldest and create new
if fileCount < 3:
	write_file(myH4s)
else:
	os.remove(resultPath + oldest)
	write_file(myH4s)

# Send any changes via email
def send_email(toaddr, data):
	import smtplib
	from email.MIMEMultipart import MIMEMultipart
	from email.MIMEText import MIMEText
	 
	fromaddr = 'add_here'
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = 'Slack Page Changes'
	body = 'Page additions:\n\n' + data
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, 'add_here')
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

# Check diff between two files
files = [ f for f in os.listdir(resultPath) if isfile(join(resultPath,f)) ]
a = set(open(resultPath + files[0]).readlines())
b = set(open(resultPath + files[1]).readlines())
c = set(open(resultPath + files[2]).readlines())

oldestDiff = b - a
newestDiff = c - b
if oldestDiff == newestDiff:
	print 'no changes'
else:
	mailData = ''
	for i in newestDiff:
		mailData += i
	print 'sending mail...'
	send_email('add_here', mailData)





