import requests
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser


url = "https://slack.com/jobs"
data = requests.get(url)
content = ""

#Download page data
if data.raise_for_status() != None:
	print "Error encountered"
	content = data.raise_for_status()
else:
	content = data.text

#Parse out relevant content

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
for i in range(len(myH4s)):
	print strip_tags(myH4s[i])

	

