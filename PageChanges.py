import requests
import subprocess
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import datetime
import os

url = "https://slack.com/jobs"
data = requests.get(url)
content = ""

# Download page data
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

timeStamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
soup = BeautifulSoup(content, 'html.parser')
myH4s = str(soup.findAll('h4')).split(", ")

# Check file count in Results Directory
ps = subprocess.Popen(('ls', 'Results/'), stdout=subprocess.PIPE)
fileCount = subprocess.check_output(('wc', '-l'), stdin=ps.stdout)
ps.wait()

path = "/Users/Zach/Development/GitHub\ Repos/SlackJobs"
# files = sorted(os.listdir(path), key=os.path.getctime)
min = min(os.listdir(path), key=os.path.getctime)
print min
# print files

def write_file():
	f = open('Results/results_' + timeStamp + '.txt', 'w+')
	for i in range(len(myH4s)):
		f.write(strip_tags(myH4s[i] + "\n"))
	f.close()

if int(fileCount) < 2:
	write_file()
else:
	print "too bad bro"
	# files = []
	# os.listdir()
















