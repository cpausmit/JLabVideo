#!/usr/bin/python
#====================================================================================================
#
# Archive all oral presentations recorded for junior lab on this computer.
#
# Requirements:
#
# - put your public key (usually $HOME/.ssh/id_rsa.pub) into the home server file
#   (serverUser@serverHost:.ssh/authorized_keys to avoid having to type the password.
#
#                                                                         Ch. Paus (V0, Nov 25, 2019)
#====================================================================================================
import os,sys,getopt,re
import ConfigParser

#====================================================================================================
# H E L P E R S 
#====================================================================================================
def archive(archiveDir,archiveServer,archiveRemoteDir):
    # archive all valuable files created
    
    cmd = "rsync -Cavz %s %s:%s"%(archiveDir,archiveServer,archiveRemoteDir)
    #cmd = "rm -f cmd.sh; mkdir -p %s; mv %s.* %s"%(archiveDir,fileTrunc,archiveDir)
    print ' Archive: ' + cmd
    os.system(cmd)

#===================================================================================================
# M A I N
#===================================================================================================
# command line options and their defaults
debug = False
test = False

# Read the configuration file
config = ConfigParser.RawConfigParser()
config.read('jlabvideo.cfg')

print ""
archiveDir = config.get('Archive','dir')
archiveServer = config.get('Archive','server')
archiveRemoteDir = config.get('Archive','remote_dir')
print " Archive:   %s"%(archiveDir)
print " Server:    %s"%(archiveServer)
print " RemoteDir: %s"%(archiveRemoteDir)

# done with options
print ""

# Define string to explain usage of the script
usage  = "\nUsage: archive.py \n"

valid = ['debug','help']
try:
    opts, args = getopt.getopt(sys.argv[1:], "", valid)
except getopt.GetoptError, ex:
    print usage
    print str(ex)
    sys.exit(1)

# read all command line options
for opt, arg in opts:
    if opt == "--help":
        print usage
        sys.exit(0)
    if opt == "--debug":
        debug = True

# this needs to be archived
archive(archiveDir,archiveServer,archiveRemoteDir)

# and exit!
sys.exit(0)
