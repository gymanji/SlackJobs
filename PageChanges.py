import requests
import subprocess
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import datetime
import os


# Download page data
url = "https://slack.com/jobs"
data = requests.get(url)
content = ""

if data.raise_for_status() != None:
	print "Error encountered"
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
os.chdir(resultPath)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
oldest = files[0]

def write_file(myH4s):
	timeStamp = datetime.datetime.now().strftime("%H%M%S")
	f = open(resultPath + 'result-' + timeStamp + '.txt', 'w')
	for i in range(len(myH4s)):
		f.write(strip_tags(myH4s[i] + "\n"))
	f.close()

# Check file count in Results Directory
ps = subprocess.Popen(('ls', resultPath), stdout=subprocess.PIPE)
fileCount = subprocess.check_output(('wc', '-l'), stdin=ps.stdout)
ps.wait()	

# Write new file or delete oldest and create new
if int(fileCount) < 2:
	write_file(myH4s)
else:
	print "file count over 2"
	os.remove(resultPath + oldest)
	write_file(myH4s)
	print "wrote new file"
# Check diff between two job files
files = []
# print subprocess.call(['ls', resultPath])







