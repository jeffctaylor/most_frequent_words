#!/usr/bin/env python

###############################################################################
# Program information
###############################################################################
__author__ = "Craig A. Struble"
__date__ = "23 August 2005"
__version__ = "$Revision: 1.1.1.1 $"
__credits__ = """David D. Lewis, the creator of the Reuters collection
Yuen-Hsien Tseng, wrote perl tools to do something similar
"""

###############################################################################
# Imports
###############################################################################
import sgmllib
import getopt

###############################################################################
# ReutersParser - an SGML parser
###############################################################################
class ReutersParser(sgmllib.SGMLParser):
    """A class to parse text from Reuters SGML files."""

    def parse(self, s):
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

       if (True):
          filename = "/dev/null"
          if self.reuters_lewis_split == "TRAIN" and self.reuters_topics == "YES":
              if (split_files):
                 filename = "/work/jtaylo38/arff/modapte_" + category + "_" + str(numwords) + "_train.arff"
              else:
                 filename = "/work/jtaylo38/arff/modapte_" + category + "_" + str(numwords) + ".arff"
          elif self.reuters_lewis_split == "TEST" and self.reuters_topics == "YES":
              if (split_files):
                  filename = "/work/jtaylo38/arff/modapte_" + category + "_" + str(numwords) + "_arff"
              else:
                  filename = "/work/jtaylo38/arff/modapte_" + category + "_" + str(numwords) + ".arff"
          elif self.reuters_lewis_split == "NOT-USED" and (self.reuters_topics == "YES" or self.reuters_topics == "NO" or self.reuters_topics == "BYPASS"):
             filename = "junk"

          if filename != "junk":
             if (prepend_arff and not os.path.exists(filename)):
                 write_arff_header(filename)
             doc_file = open(filename, "a")
             if (include_titles):
                 self.title = self.title.lower()
                 self.title = re.sub(r'\'', r'\'', self.title)
                 doc_file.write("' " + self.title + " ")
        # Strip out multiple spaces in the body
             self.body = re.sub(r'\s+', r' ', self.body)
      # escape apostrophe characters
             self.body = re.sub(r'\'', r'\'', self.body)
             self.body = self.body.rstrip("\r\n")
             # convert to lower case
             self.body = self.body.lower()
             #self.body = re.sub(r' ', r'\n', self.body)
		# remove punctuation
		#self.body_nopunc = self.body.translate(string.maketrans("",""), string.punctuation)
             for c in string.punctuation:
                self.body = self.body.replace(c, " ")
             # remove tokens consisting of nothing but digits
             self.body = re.sub("\d+", "", self.body)
		# make the string into a list and remove stopwords from it
             self.body_split = self.body.split()
             self.body_no_stopwords = remove_stopwords(self.body_split)
             doc_file.write("'")
             if (self.body_no_stopwords):
                for i in range(0, numwords):
                   if (i < len(self.body_no_stopwords)):
                      doc_file.write(self.body_no_stopwords[i] + " ")
#           doc_file.write("'" + str(self.topics) + "/"  + "'\n")
             doc_file.write("',")
             if category in self.topics:
                doc_file.write("true")
             else:
                doc_file.write("false")
             doc_file.write("\n")
             doc_file.close()

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

def usage():
    sys.stdout.write("""
Usage: """ + sys.argv[0] + """ [-h] -c category -n num_words [-s stoplist] [--split] [--prepend] files

Arguments:
-h (or --help): print this usage message and exit
-c (or --category) category: name of a valid Reuters category (e.g. acq) (required argument)
-n (or --numwords) num_words: integer value indicating the number of words to index (required argument)
-s (or --stoplist) stoplist: location of stoplist file (default is ./aux/english.stop) (optional argument)
--split: causes 2 files to be created, for training and testing (default is one file)
--prepend: causes arff header information to be written to the file(s) (default is no arff header information)
files: list of files to convert
""")

# needs support for split training and testing files
def write_arff_header(filename):
    f = open(filename, "w")
    f.write("""@relation '""" + category + """ """ + str(numwords) + """'\n
@attribute Text string
@attribute class {false,true}\n
@data\n""")
    #sys.stdout.write("Writing arff header to new file " + filename + "\n")
    f.close()

def main(argv):
    global stopwords_file
    global split_files
    global category
    global numwords
    global filenames
    global prepend_arff
    global include_titles
    stopwords_file = "C:\\Users\\JeffT\\Dropbox\\PhD\\aux_files\\english.stop"
    split_files = False
    prepend = False
    include_titles = False
    try:
        opts, args = getopt.getopt(argv, "c:n:s:", ["category=", "numwords=", "stoplist=", "split", "prepend", "titles"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        if opt in ("--split"):
            # create separate training and testing files
            # default is one merged file
            split_files = True
        if opt in ("--prepend"):
            # prepend the file with arff header information
            # default is not to prepend
            prepend_arff = True
        if opt in ("--titles"):
            # include document titles
            # default is no titles, just body text
            include_titles = True
        if opt in ("-c", "--category"):
            category = arg
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
    global stopwords
    category = ""
    numwords = ""
    filenames = ""
    if (len(sys.argv) < 2):
        usage()
	sys.exit(2)
    else:
        main(sys.argv[1:])

    if (category == "" or numwords == "" or filenames == ""):
	usage()
	sys.exit()

    stopwords = open(stopwords_file, 'r').read().split()

    for fname in filenames:
        f = open(fname, "r")
        s = f.read()
        parser = ReutersParser()
        parser.parse(s)
