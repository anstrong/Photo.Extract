import urllib.request as urllib
from bs4 import BeautifulSoup, SoupStrainer
import os
import subprocess
import re

####################################### FUNCTIONS ###############################################

def read_html(address):
	# Open the page
	url = urllib.Request(address, headers={'User-Agent': 'Mozilla/5.0'})
	# Parse the HTML
	html = urllib.urlopen(url).read()

	return html

########################################## LOGIC ###############################################

#address = 'http://www.instagram.com/pretty._landscapes'
#address = 'https://www.instagram.com/laurkendall6/'
address = 'https://www.instagram.com/puppysphere/'

# Open and parse page
html = read_html(url)

# Turn raw html into scrapable 'soup'
soup = BeautifulSoup(html, "html.parser")

# Extract all text with 'script' tag
for script in soup(["script"]):
    text += script.get_text()

# Search for beginning of image urls in extracted text
indicator = '''"config_width": 640, "config_height": 640}], "is_video": false,''' # "code":"BNPjw9JAyuy", "date": 1480098330, "display_src":
photos = text.split(indicator)

# Create empty array to store photo urls
photo_paths = []

# Cycle through photo code and strip the urls out
for x in range(len(photos)):
	if x != 0: 							# The first chunk is all the text before the first photo
		text = photos[x]

		start = text.find('https://')	# Isolate url
		end = text.find('jpg') + 3
		photo_path = text[start:end]

		photo_paths.append(photo_path)	# Add url to photo path array

# Cycle through photo urls and dowload the images
for i in range(len(photo_paths)):
	path = photo_paths[i]
	urllib.urlretrieve(path, os.path.basename("Photo_" + str(i+1)))

# Print confirmation
print("Script extraction complete.")

# Open folder
subprocess.call(["open", "-R", "Photo_1"]])
