
"""
NAME
    extract_group_messages

SYNOPSIS
    extract_group_messages [input output thresh]

DESCRIPTION
    input       path to html file containing all messages as downloaded from Facebook

    output      path to output html file with only group messages

    thresh      number of members required for a chat to be considered a group chat
"""

import sys

from bs4 import BeautifulSoup as BF

ARG_NUM = 4     # number of arguments expected plus script name

if len(sys.argv) != ARG_NUM:
    sys.exit(127)
inputPath = sys.argv[1]
outputPath = sys.argv[2]
thresh = int(sys.argv[3])

print("Loading input file:", inputPath)
inputFile = open(inputPath)
soup = BF(inputFile, 'html.parser')


# Filters threads based on how many participants
def filter_group(thread):
    text = thread.find(text=True, recursive=False) # participants
    if len(text.split(',')) >= thresh:
        return True


# Filter out group messages
print("Extracting group messages...")
threads = soup.find_all('div', class_='thread')
groups = []
for thread in threads:
    if filter_group(thread):
        groups.append(thread)
print("Found", len(groups), "group messages")

# Write to file
print("Writing to output file:", outputPath)
outsoup = BF('<html></html>', 'html.parser')
for thread in groups:
    outsoup.append(thread)

with open(outputPath, 'wb') as file:
    file.write(outsoup.prettify('UTF-8'))

inputFile.close()
