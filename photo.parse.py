import urllib.request as urllib
from bs4 import BeautifulSoup, SoupStrainer
import os
import subprocess
import re

####################################### FUNCTIONS ###############################################

def read_html(address):
	# Open the page
	url = urllib.Request(address)#, headers={'User-Agent': 'Mozilla/5.0'})
	# Parse the HTML
	html = urllib.urlopen(url).read()

	return html

def get_account_name(address):
	# Isolate account name
	start = address.find('instagram.com/') + 14
	end = len(address) - 1
	name = address[start:end]

	return name

########################################## LOGIC ###############################################

#address = 'http://www.instagram.com/pretty._landscapes'
#address = 'https://www.instagram.com/laurkendall6/'
#address = 'https://www.instagram.com/puppysphere/'
address = 'https://www.instagram.com/universal.puppies/'

# Open and parse page
html = read_html(address)

# Turn raw html into scrapable 'soup'
soup = BeautifulSoup(html, "html.parser")

text = ''

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

# Get name for folder from account name
folder = get_account_name(address)
file_path = '/Users/annabelle_strong/Documents/Bin/Extracted Images/' + folder + '/'

try:
	os.chdir(file_path)
except FileNotFoundError:
	os.mkdir(file_path)
	os.chdir(file_path)
	
# Cycle through photo urls and dowload the images
for i in range(len(photo_paths)):
	path = photo_paths[i]
	urllib.urlretrieve(path, os.path.basename('Photo_%(num)s.jpg' %{'num': str(i+1)}))

# Print confirmation
print("Image extraction complete.")

# Open folder
subprocess.call(["open", "-R", file_path])
