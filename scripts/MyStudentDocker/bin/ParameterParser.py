#!/usr/bin/env python

# ParameterParser.py
# Description: * Read parameter.config
#              * Parse stdin and stdout files based on parameter.config
#              * Create a json file

import json
import glob
import md5
import os
import random
import sys

UBUNTUHOME = "/home/ubuntu/"
randreplacelist = {}
hashcreatelist = {}
hashreplacelist = {}
paramlist = {}

def CheckRandReplaceEntry(lab_instance_seed, param_id, each_value):

    # RAND_REPLACE : <filename> : <token> : <LowerBound> : <UpperBound>
    #print "Checking RAND_REPLACE entry"
    entryline = each_value.split(':')
    #print entryline
    numentry = len(entryline)
    if numentry != 4:
        sys.stderr.write("ERROR: RAND_REPLACE (%s) improper format\n" % each_value)
        sys.stderr.write("ERROR: RAND_REPLACE : <filename> : <token> : <LowerBound> : <UpperBound>\n")
        sys.exit(1)
    myfilename = entryline[0].strip()
    token = entryline[1].strip()
    #print "filename is (%s)" % myfilename
    #print "token is (%s)" % token

    # Converts lowerbound and upperbound as integer - and pass to
    # random.randint(a,b)
    # Starts with assuming will use integer (instead of hexadecimal)
    use_integer = True
    lowerboundstr = entryline[2].strip()
    if lowerboundstr.startswith('0x'):
        use_integer = False
        lowerbound_int = int(lowerboundstr, 16)
    else:
        lowerbound_int = int(lowerboundstr, 10)
    upperboundstr = entryline[3].strip()
    if upperboundstr.startswith('0x'):
        if use_integer == True:
            # Inconsistent format of lowerbound (integer format)
            # vs upperbound (hexadecimal format)
            sys.stderr.write("ERROR: RAND_REPLACE (%s) inconsistent lowerbound/upperbound format\n" % each_value)
            sys.stderr.write("ERROR: RAND_REPLACE : <filename> : <token> : <LowerBound> : <UpperBound>\n")
            sys.exit(1)
        use_integer = False
        upperbound_int = int(upperboundstr, 16)
    else:
        upperbound_int = int(upperboundstr, 10)
    #print "lowerbound is (%d)" % lowerbound_int
    #print "upperbound is (%d)" % upperbound_int
    if lowerbound_int > upperbound_int:
        sys.stderr.write("ERROR: RAND_REPLACE (%s) inconsistent lowerbound/upperbound format\n" % each_value)
        sys.stderr.write("ERROR: RAND_REPLACE : <filename> : <token> : <LowerBound> : <UpperBound>\n")
        sys.exit(1)
    random_int = random.randint(lowerbound_int, upperbound_int)
    #print "random value is (%d)" % random_int
    if use_integer:
        random_str = '%s' % int(random_int)
    else:
        random_str = '%s' % hex(random_int)
    if myfilename in randreplacelist:
        randreplacelist[myfilename].append('%s:%s' % (token, random_str))
    else:
        randreplacelist[myfilename] = []
        randreplacelist[myfilename].append('%s:%s' % (token, random_str))
    paramlist[param_id] = random_str


def CheckHashCreateEntry(lab_instance_seed, param_id, each_value):
    # HASH_CREATE : <filename> : <string>
    #print "Checking HASH_CREATE entry"
    entryline = each_value.split(':')
    #print entryline
    numentry = len(entryline)
    if numentry != 2:
        sys.stderr.write("ERROR: RAND_CREATE (%s) improper format\n" % each_value)
        sys.stderr.write("ERROR: HASH_CREATE : <filename> : <string>\n")
    myfilename = entryline[0].strip()
    the_string = entryline[1].strip()
    # Create hash per the_string
    string_to_be_hashed = '%s:%s' % (lab_instance_seed, the_string)
    mymd5 = md5.new()
    mymd5.update(string_to_be_hashed)
    mymd5_hex_string = mymd5.hexdigest()
    #print mymd5_hex_string
    #print "filename is (%s)" % myfilename
    #print "the_string is (%s)" % the_string
    #print "mymd5_hex_string is (%s)" % mymd5_hex_string
    # If file does not exist, create an empty file
    if not os.path.exists(myfilename):
        outfile = open(myfilename, 'w')
        outfile.write('')
        outfile.close()
    if myfilename in hashcreatelist:
        hashcreatelist[myfilename].append('%s' % mymd5_hex_string)
    else:
        hashcreatelist[myfilename] = []
        hashcreatelist[myfilename].append('%s' % mymd5_hex_string)
    paramlist[param_id] = mymd5_hex_string

def CheckHashReplaceEntry(lab_instance_seed, param_id, each_value):
    # HASH_REPLACE : <filename> : <token> : <string>
    #print "Checking HASH_REPLACE entry"
    entryline = each_value.split(':')
    #print entryline
    numentry = len(entryline)
    if numentry != 3:
        sys.stderr.write("ERROR: RAND_REPLACE (%s) improper format\n" % each_value)
        sys.stderr.write("ERROR: HASH_REPLACE : <filename> : <token> : <string>\n")
    myfilename = entryline[0].strip()
    token = entryline[1].strip()
    the_string = entryline[2].strip()
    # Create hash per the_string
    string_to_be_hashed = '%s:%s' % (lab_instance_seed, the_string)
    mymd5 = md5.new()
    mymd5.update(string_to_be_hashed)
    mymd5_hex_string = mymd5.hexdigest()
    #print "filename is (%s)" % myfilename
    #print "token is (%s)" % token
    #print "the_string is (%s)" % the_string
    if myfilename in hashreplacelist:
        hashreplacelist[myfilename].append('%s:%s' % (token, mymd5_hex_string))
    else:
        hashreplacelist[myfilename] = []
        hashreplacelist[myfilename].append('%s:%s' % (token, mymd5_hex_string))
    paramlist[param_id] = mymd5_hex_string


def ValidateParameterConfig(lab_instance_seed, param_id, each_key, each_value):
    if each_key == "RAND_REPLACE":
        #print "RAND_REPLACE"
        CheckRandReplaceEntry(lab_instance_seed, param_id, each_value)
    elif each_key == "HASH_CREATE":
        #print "HASH_CREATE"
        CheckHashCreateEntry(lab_instance_seed, param_id, each_value)
    elif each_key == "HASH_REPLACE":
        #print "HASH_REPLACE"
        CheckHashReplaceEntry(lab_instance_seed, param_id, each_value)
    else:
        sys.stderr.write("ERROR: Invalid operator %s\n" % each_key)
        sys.exit(1)
    return 0

# Perform RAND_REPLACE
def Perform_RAND_REPLACE(lab_instance_seed):
    # At this point randreplacelist should have been populated
    # and files have been confirmed to exist

    #print "Perform_RAND_REPLACE"
    for (filename, replacelist) in randreplacelist.items():
        #print "Current Filename is %s" % filename
        if not os.path.exists(filename):
            sys.stderr.write("ERROR: Perform_RAND_REPLACE: File %s does not exist\n" % filename)
            sys.exit(1)
        #else:
        #    print "File (%s) exist\n" % filename
        #print "Replace list is "
        #print replacelist
        filelines = []
        # First open the file - read
        with open(filename, 'r') as infile:
            for line in infile:
                # Replace token
                for replaceitem in replacelist:
                    (oldtoken, newtoken) = replaceitem.split(':')
                    line = line.replace(oldtoken, newtoken)
                filelines.append(line)
        infile.close()
        # Re-open file with write
        with open(filename, 'w') as outfile:
            for line in filelines:
                outfile.write(line)
        outfile.close()

# Perform HASH_CREATE
def Perform_HASH_CREATE(lab_instance_seed):
    # At this point hashcreatelist should have been populated
    # and files have been confirmed to exist or created

    #print "Perform_HASH_CREATE"
    for (filename, createlist) in hashcreatelist.items():
        #print "Current Filename is %s" % filename
        #print "Hash Create list is "
        #print createlist
        # open the file - write
        outfile = open(filename, 'w')
        for the_string in createlist:
            outfile.write('%s\n' % the_string)
        outfile.close()

# Perform HASH_REPLACE
def Perform_HASH_REPLACE(lab_instance_seed):
    # At this point hashreplacelist should have been populated
    # and files have been confirmed to exist

    #print "Perform_HASH_REPLACE"
    for (filename, replacelist) in hashreplacelist.items():
        #print "Current Filename is %s" % filename
        if not os.path.exists(filename):
            sys.stderr.write("ERROR: Perform_HASH_REPLACE: File %s does not exist\n" % filename)
            sys.exit(1)
        #else:
        #    print "File (%s) exist\n" % filename
        #print "Replace list is "
        #print replacelist
        filelines = []
        with open(filename, 'r') as infile:
            for line in infile:
                # Replace token
                for replaceitem in replacelist:
                    (oldtoken, newtoken) = replaceitem.split(':')
                    line = line.replace(oldtoken, newtoken)
                filelines.append(line)
        infile.close()
        # Re-open file with write
        with open(filename, 'w') as outfile:
            for line in filelines:
                outfile.write(line)
        outfile.close()

def DoReplace(lab_instance_seed):
    # Perform RAND_REPLACE
    Perform_RAND_REPLACE(lab_instance_seed)
    # Perform HASH_CREATE
    Perform_HASH_CREATE(lab_instance_seed)
    # Perform HASH_REPLACE
    Perform_HASH_REPLACE(lab_instance_seed)

def ParseParameterConfig(lab_instance_seed, configfilename):
    # Seed random with lab seed
    random.seed(lab_instance_seed)
    configfile = open(configfilename)
    configfilelines = configfile.readlines()
    configfile.close()
  
    for line in configfilelines:
        linestrip = line.rstrip()
        if linestrip:
            if not linestrip.startswith('#'):
                #print "Current linestrip is (%s)" % linestrip
                (param_id, each_key, each_value) = linestrip.split(':', 2)
                each_key = each_key.strip()
                param_id = param_id.strip()
                ValidateParameterConfig(lab_instance_seed, param_id, each_key, each_value)
        #else:
        #    print "Skipping empty linestrip is (%s)" % linestrip
    return paramlist



# Usage: ParameterParser.py <lab_instance_seed> [<config_file>]
# Arguments:
#     <lab_instance_seed> - laboratory instance seed
#     [<config_file>] - optional configuration file
#                       if <config_file> not specified, it defaults to
#                       /home/ubuntu/.local/config/parameter.config
def main():
    #print "Running ParameterParser.py"
    numargs = len(sys.argv)
    if not (numargs == 2 or numargs == 3):
        sys.stderr.write("Usage: ParameterParser.py <lab_instance_seed> [<config_file>]\n")
        sys.exit(1)

    lab_instance_seed = sys.argv[1]
    if numargs == 3:
        configfilename = sys.argv[2]
    else:
        configfilename = '%s/.local/config/%s' % (UBUNTUHOME, "parameter.config")
    ParseParameterConfig(lab_instance_seed, configfilename)
    DoReplace(lab_instance_seed)
    return 0

if __name__ == '__main__':
    sys.exit(main())

