#!/usr/bin/python
# Processes files from www.webuse.umd.edu:9090/tags to extract usable word tag analyses information

import sys
import re
import os

def main(*args):
  # 2 arguments -- process single file
  if (len(args) == 2):
    print "Processing file: " + args[1]
    process_file(args[1])
  # 1 argument -- process all files in current directory ending with .html
  elif (len(args) == 1):
    print "Processing all html files in current directory..."
    dirlist = os.listdir(os.getcwd())
    for d in dirlist:
      if d.split(".")[1] == "html": # only process html files
        print "Processing file: " + d
        process_file(d)
  else:
    print "Error, incorrect number of arguments (0 or 1 accepted)"
    return 1
    
  return 0
  
  

def process_file(file_name):
  # Determine name for output file
  o_name = file_name.split(".")[0]
  o_name += ".txt" # input name with extension changed to txt 
  
  lines = open(file_name).readlines() # open file for reading, convert to list of strings
  o = open(o_name, 'w')  #str.join(args[1], ".txt"
  
  # Iterate over lines in the input file
  for l in lines:
    elements = l.split(" ") # split into words
    if (len(elements) >= 4) & (elements[0] == "<TR>"): # only proceed if line containing Word
      m = re.search('(?<=>)[A-Z]*-?[A-Z]*', elements[3]) # matches word on line
      n = len(elements) - 2 # to remove the trailing HTML tags at EOL
      
      # Write file
      o.write(m.group(0)) # Word 
      o.write(str.join(" ", elements[6:n]) + '\n') # additional word info
  
  o.close()

if __name__ == "__main__":
    sys.exit(main(*sys.argv))