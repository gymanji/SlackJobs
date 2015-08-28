
import requests
from bs4 import BeautifulSoup

#https://slack.com/jobs
#http://blogs.air-watch.com/

url = "https://slack.com/jobs"
data = requests.get(url)

if data.raise_for_status() != None:
	print "Error encountered"
	content = data.raise_for_status()
else:
	content = data.text

soup = BeautifulSoup(content, 'html.parser')

mydivs = soup.findAll("a", { "class" : "posting-title" })
items = str(mydivs).split(", ")

finalData = []
for item in items:
	print item
	





# for i in len(mydivs):
# 	print mydivs[i] + "\n"



# from subprocess import call
#call(["curl", "http://blogs.air-watch.com/ > data2.txt"])
# file = open('data.txt', 'r')
# file.read()