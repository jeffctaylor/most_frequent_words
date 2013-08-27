###############################################################################
# Imports
###############################################################################
import getopt
import sys
import os
import os.path
import re
import string
import glob
from nltk import FreqDist

###
# Parse the file and create the output
###

def parse(filename):
    outfilename = filename + ".freq"
    entry_string = open(filename, 'r').read()
 
    # convert to lower case 
    entry_string = entry_string.lower() 

    # remove punctuation 
    for c in string.punctuation: 
            entry_string = entry_string.replace(c, " ") 

    # remove everything except letters and spaces
    entry_string = re.sub("[^a-z ]", " ", entry_string) 

    # strip out multiple spaces 
    entry_string = re.sub(r'\s+', r' ', entry_string) 

    # make the string into a list and remove stopwords from it 
    entry_string_split = entry_string.split() 
    entry_string_no_stopwords = remove_stopwords(entry_string_split) 

    fd = FreqDist(entry_string_no_stopwords)

    fout = open(outfilename, "w")
    sys.stdout.write(outfilename + "\n")
    fout.write(" ".join(fd.keys()))
    fout.close() 

def remove_stopwords(inwords):
   filteredtext = [t for t in inwords if t.lower() not in stopwords]
   return filteredtext

def usage():
    sys.stdout.write("""
Usage: """ + sys.argv[0] + """ [-h] [-s stoplist] [-o filename] [-r relation_prefix] [--debug]

Arguments:
-h (or --help): print this usage message and exit -s (or --stoplist) stoplist: location of stoplist file (default: ./aux/english.stop) (optional argument)
-o (or --outfile) filename: name of the file to which output will be written (default: blogdata.arff) (optional argument)
-r (or --relation) relation_prefix: name of the relation as it will appear in the output file (default: "blog data") (optional argument)
--debug: display values of all command line parameters, with no processing performed. Useful for double checking that everything is set up properly.
""")

def process_files():
    for split in ['training', 'test']:
        for classname in ['C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23']:
            #filenames = base_directory + "\\" + classname + "\\" + "cv" + str(fold_number) + str(number).zfill(2) + "*.txt"
            filenames = base_directory + "\\" + split + "\\" + classname + "\\" + "*"
            for file in glob.glob(filenames):
                parse(file)

def main(argv):
    global stopwords_file
    global outfileprefix
    global debug
    global base_directory
    global fold_numberG
    stopwords_file = "C:\\Users\\JeffT\\Dropbox\\PhD\\aux_files\\english.stop"
    outfileprefix = "ohsumed"
    base_directory = "C:\\Users\\JeffT\\University Work\\phd\\corpora\\ohsumed\\ohsumed-first-20000-docs"
    fold_numberG = ""
    debug = False

    try:
	    opts, args = getopt.getopt(argv, "s:o:r:f:", ["stoplist=", "outfile=", "relation=", "fold=", "debug"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        if opt in ("-s", "--stoplist"):
            stopwords_file = arg
        if opt in ("-o", "--outfile"):
            outfileprefix = arg
        if opt in ("-f", "--fold"):
            fold_numberG = arg
        if opt in ("--debug"):
            debug = True

###############################################################################
# Main Program
###############################################################################

if __name__ == '__main__':
    global stopwords
    main(sys.argv[1:])

    if (debug):
        sys.stdout.write("Debug mode.\n")
        sys.stdout.write("stopwords_file: " + stopwords_file + "\n")
        sys.stdout.write("outfileprefix: " + outfileprefix + "\n")
        sys.stdout.write("fold_numberG: " + fold_numberG + "\n")
        sys.exit()

    stopwords = open(stopwords_file, "r").read().split()

    process_files()
