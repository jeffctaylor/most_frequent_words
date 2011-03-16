#!/usr/bin/env python

###############################################################################
# Imports
###############################################################################
import sgmllib
import getopt
from nltk import FreqDist

###############################################################################
# ReutersParser - an SGML parser
###############################################################################
class ReutersParser(sgmllib.SGMLParser):
    """A class to parse text from Reuters SGML files."""

    def parse(self, s, category):
        """Parse the given string 's', which is an SGML encoded file."""

        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        """Initialize an object, passing 'verbose' to the superclass."""

        sgmllib.SGMLParser.__init__(self, verbose)
        self.in_topics = 0
        """Flag indicating whether or not we're parsing the topic."""

        self.in_title = 0
        """Flag indicating whether or not we're parsing the title."""

        self.in_body = 0
        """Flag indicating whether or not we're parsing the body"""

        self.topics = []
        """Topic of the document"""

        self.title = ""
        """Title of the document"""

        self.reuters_lewis_split = ""
        
        self.reuters_topics = ""

        self.doc_id = 0
        """Document ID"""

        self.body = ""
        """Body of the document"""

    def handle_data(self, data):
        """Print out data in TEXT portions of the document."""

        if self.in_body:
            self.body += data
        elif self.in_title:
            self.title += data
        elif self.in_topics:
            self.topics += [data.lower()]

    ####
    # Handle the Reuters tag
    ####
    def start_reuters(self, attributes):
       """Process Reuters tags, which bracket a document. Create a new
       file for each document encountered.
       """

       for name, value in attributes:
          if name == "topics":
             self.reuters_topics = value
          if name == "lewissplit":
             self.reuters_lewis_split = value
          if name == "newid":
             self.doc_id = value

    def end_reuters(self):
       """Write out the contents to a file and reset all variables."""

       from textwrap import fill
       import re
       import string

       filename = "/dev/null"
       if self.reuters_lewis_split == "TRAIN" and self.reuters_topics == "YES":
          directory = "C:\\Users\\JeffT\\University Work\\phd\\corpora\\reuters-21578\\" + category
          filename = self.doc_id
       elif self.reuters_lewis_split == "TEST" and self.reuters_topics == "YES":
          directory = "C:\\Users\\JeffT\\University Work\\phd\\corpora\\reuters-21578\\" + category
          filename = self.doc_id
       elif self.reuters_lewis_split == "NOT-USED" and (self.reuters_topics == "YES" or self.reuters_topics == "NO" or self.reuters_topics == "BYPASS"):
          filename = "junk"

       if filename != "junk" and filename != "/dev/null":
          if category in self.topics:
             fullfilepath = directory + "\\" + filename
             sys.stdout.write(fullfilepath + "\n") 
             doc_file = open(fullfilepath, "w")
             self.title = self.title.lower()
             self.title = re.sub(r'\'', r'\'', self.title)
             doc_file.write(self.title + " ")
    # Strip out multiple spaces in the body
             self.body = re.sub(r'\s+', r' ', self.body)
   # escape apostrophe characters
             self.body = re.sub(r'\'', r'\'', self.body)
             self.body = self.body.rstrip("\r\n")
          # convert to lower case
             self.body = self.body.lower()
		# remove punctuation
             for c in string.punctuation:
                self.body = self.body.replace(c, " ")
          # remove tokens consisting of nothing but digits
             self.body = re.sub("\d+", "", self.body)
          # make the string into a list and remove stopwords from it
             self.body_split = self.body.split()
             self.body_no_stopwords = remove_stopwords(self.body_split)

             fd = FreqDist(self.body_no_stopwords)

             doc_file.write(" ".join(fd.keys()))
             doc_file.close()
#
           # Reset variables
       self.in_topics = 0
       self.in_title = 0
       self.in_body = 0
       self.reuters_lewis_split = ""
       self.reuters_topics = ""
       self.doc_id = 0
       self.topics = []
       self.title = ""
       self.body = ""

    ####
    # Handle TOPICS tags
    ####
    def start_topics(self, attributes):
       """Indicate that the parser is in the topics portion of the document.
       """

       self.in_topics = 1

    def end_topics(self):
       """Indicate that the parser is no longer in the topics portion of the
       document.
       """

       self.in_topics = 0

    ####
    # Handle TITLE tags
    ####   
    def start_title(self, attributes):
       """Indicate that the parser is in the title portion of the document.
       """

       self.in_title = 1

    def end_title(self):
       """Indicate that the parser is no longer in the title portion of the
       document.
       """

       self.in_title = 0

    ####
    # Handle BODY tags
    ####
    def start_body(self, attributes):
       """Indicate that the parser is in the body portion of the document.
       """

       self.in_body = 1

    def end_body(self):
       """Indicate that the parser is no longer in the body portion of the
       document.
       """

       self.in_body = 0

###
# Create directory if it doesn't already exist
###
def create_directory(dir_name):
   if not os.path.exists(dir_name):
      os.makedirs(dir_name)
      #sys.stdout.write("Created directory " + dir_name + "\n")
      
def remove_stopwords(inwords):
   filteredtext = [t for t in inwords if t.lower() not in stopwords]
   return filteredtext

def main(argv):
    global stopwords_file
    global numwords
    global filenames
    global prepend_arff
    global include_titles
    stopwords_file = "C:\\Users\\JeffT\\Dropbox\\PhD\\aux_files\\english.stop"
    prepend = False
    include_titles = False
    try:
        opts, args = getopt.getopt(argv, "n:s:", ["numwords=", "stoplist=", "titles"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        if opt in ("--titles"):
            # include document titles
            # default is no titles, just body text
            include_titles = True
        if opt in ("-n", "--numwords"):
            numwords = int(arg)
        if opt in ("-s", "--stoplist"):
            stopwords_file = arg

    filenames = args
    #sys.stdout.write("Joined arguments: " + filenames)

###############################################################################
# Main Program
###############################################################################
import sys
import os
import os.path

if __name__ == '__main__':

    categories = ['acq', 'alum', 'austdlr', 'austral', 'barley', 'bfr', 'bop', 'can', 'carcass', 'castor-meal', 'castor-oil', 'castorseed', 'citruspulp', 'cocoa', 'coconut', 'coconut-oil', 'coffee', 'copper', 'copra-cake', 'corn', 'corn-oil', 'cornglutenfeed', 'cotton', 'cotton-meal', 'cotton-oil', 'cottonseed', 'cpi', 'cpu', 'crude', 'cruzado', 'dfl', 'dkr', 'dlr', 'dmk', 'drachma', 'earn', 'escudo', 'f-cattle', 'ffr', 'fishmeal', 'flaxseed', 'fuel', 'gas', 'gnp', 'gold', 'grain', 'groundnut', 'groundnut-meal', 'groundnut-oil', 'heat', 'hk', 'hog', 'housing', 'income', 'instal-debt', 'interest', 'inventories', 'ipi', 'iron-steel', 'jet', 'jobs', 'l-cattle', 'lead', 'lei', 'lin-meal', 'lin-oil', 'linseed', 'lit', 'livestock', 'lumber', 'lupin', 'meal-feed', 'mexpeso', 'money-fx', 'money-supply', 'naphtha', 'nat-gas', 'nickel', 'nkr', 'nzdlr', 'oat', 'oilseed', 'orange', 'palladium', 'palm-meal', 'palm-oil', 'palmkernel', 'peseta', 'pet-chem', 'platinum', 'plywood', 'pork-belly', 'potato', 'propane', 'rand', 'rape-meal', 'rape-oil', 'rapeseed', 'red-bean', 'reserves', 'retail', 'rice', 'ringgit', 'rubber', 'rupiah', 'rye', 'saudriyal', 'sfr', 'ship', 'silk', 'silver', 'singdlr', 'skr', 'sorghum', 'soy-meal', 'soy-oil', 'soybean', 'stg', 'strategic-metal', 'sugar', 'sun-meal', 'sun-oil', 'sunseed', 'tapioca', 'tea', 'tin', 'trade', 'tung', 'tung-oil', 'veg-oil', 'wheat', 'wool', 'wpi', 'yen', 'zinc']
    
    global stopwords
    filenames = ""
    if (len(sys.argv) < 2):
        sys.stdout.write("Files?\n")
	sys.exit(2)
    else:
        main(sys.argv[1:])

    if (filenames == ""):
	sys.stdout.write("Something's wrong.\n")
	sys.exit()

    stopwords = open(stopwords_file, 'r').read().split()

    for category in categories:
        for fname in filenames:
            f = open(fname, "r")
            s = f.read()
            parser = ReutersParser()
            parser.parse(s, category)
