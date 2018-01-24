import urllib.request as urllib
from bs4 import BeautifulSoup, SoupStrainer
import os
import subprocess
import re

####################################### FUNCTIONS ###############################################
def read_html(address):
	# Open and parse the page
	url = urllib.Request(address, headers={'User-Agent': 'Mozilla/5.0'})
	html = urllib.urlopen(url).read()

	return html

########################################## LOGIC ###############################################
#address = 'http://www.instagram.com/pretty._landscapes'
#address = 'https://www.instagram.com/laurkendall6/'
address = 'https://www.instagram.com/puppysphere/'

# Parse page
html = read_html(url)

soup = BeautifulSoup(html, "html.parser")

text = 'Script: '

for script in soup(["script"]):
    text += script.get_text()

indicator = '''"config_width": 640, "config_height": 640}], "is_video": false,''' # "code":"BNPjw9JAyuy", "date": 1480098330, "display_src":

photos = text.split(indicator)

photo_paths = []

for x in range(len(photos)):
	if x != 0:
		text = photos[x]

		start = text.find('https://')
		end = text.find('jpg') + 3
		photo_path = text[start:end]

		photo_paths.append(photo_path)

for i in range(len(photo_paths)):
	path = photo_paths[i]
	urllib.urlretrieve(path, os.path.basename("Photo_" + str(i+1)))


# Print confirmation
print("Script extraction complete.")
