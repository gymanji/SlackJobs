import requests
from bs4 import BeautifulSoup
import re


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
soup = BeautifulSoup(content, 'html.parser')
mydivs = soup.findAll("a", { "class" : "posting-title" })
items = str(mydivs).split(", ")

finalData = []
for i in range(len(items)):
	stripData = re.match('<h4>*?</h4>', items[i])
	finalData.append(stripData)	

print finalData
# finalData = []
# for item in items:
# 	stripData = re.match('<h4>*', item)
# 	finalData.append(stripData)

# print finalData
	

