#!/usr/bin/python
#====================================================================================================
#
# Record a oral presentation in MIT junior lab 8.13, create the web access file, copy both to the
# server and sent e-mail to te student and the instructors.
#
# Requirements:
#
# - install vlc and the relevant packages for ACC (mp4) codec support
#
# - put your public key (usually $HOME/.ssh/id_rsa.pub) into
#       the server file (serverUser@serverHost:.ssh/authorized_keys)
#       to avoid having to type the password            
#
#                                                                         Ch. Paus (V0, Oct 09, 2014)
#====================================================================================================
import os,sys,getopt,re
import ConfigParser

#====================================================================================================
# H E L P E R S 
#====================================================================================================
def getInstructors(classFilesInstructors):
    # get the full string of instructor e-mails

    instructorEmails = ''
    inputFile = open(classFilesInstructors,'r')
    for line in inputFile.xreadlines():
        line = line[0:-1]
        items = line.split(',')
        email = items[0]
        lastName = items[1]
        firstName = items[2]
        # skip the initial line
        if email == 'EMAIL':
            continue
        if instructorEmails == '':
            instructorEmails = email
        else:
            instructorEmails += "," + email
    inputFile.close()
    
    print ' Instructors:  %s'%(instructorEmails)
    return instructorEmails

def getStudent(classFilesStudents,debug):
    # get the students and select requested student

    inputFile = open(classFilesStudents,'r')
    for line in inputFile.xreadlines():
        line = line[0:-1]
        items = line.split(',')
        email = items[0]
        lastName = items[1]
        firstName = items[2]
        if email != 'EMAIL':
            if debug:
                print ' Student:  %-15s %-15s %s'%(firstName,lastName,email)

            if lastName == name:
                print ' Selected:  %-15s %-15s %s'%(firstName,lastName,email)
                break
            else:
                email = ''
                lastName = ''
                firstName = ''
    inputFile.close()

    return (email,lastName,firstName)

def mute():
    # before recording please mute (otherwise beeeeeeeeppppp)

    cmd =  "amixer set Master mute  >& /dev/null"
    print ' Mute speakers first: ' + cmd
    os.system(cmd)
    
def unMute():
    # after recording unmute se we can hear

    cmd =  "amixer set Master unmute >& /dev/null"
    print ' Mute speakers first: ' + cmd
    os.system(cmd)

def record(video,fileTrunc):    
    # here is the recording using vlc (nice tool)

    cmd = "vlc v4l2://%s :v4l2-standard=NTSC :input-slave=alsa://"%(video) + " :live-caching=300" + \
          " --sout '#transcode{vcodec=mp4v,acodec=mpga,vb=800,ab=128}" + \
          ":duplicate{dst=display,dst=std{access=file,dst=%s.mp4}}' >& /dev/null"%(fileTrunc)
    print ' Recording: ' + cmd
    print '  --> PLEASE exit the vlc player and let the script complete.\n'
    os.system(cmd)

def showVideo(fileTrunc):    
    cmd = "vlc %s.mp4 >& /dev/null"%(fileTrunc)
    print ' Showing: ' + cmd
    print '  --> PLEASE exit the vlc player and let the script complete.\n'
    os.system(cmd)

def cleanup(fileTrunc):    
    # cleanup the files created

    cmd = "rm -f cmd.sh %s.*"%(fileTrunc)
    print ' Cleanup: ' + cmd
    os.system(cmd)

def archive(archiveDir,fileTrunc):    
    # archive all valuable files created

    cmd = "rm -f cmd.sh; mkdir -p %s; mv %s.* %s"%(archiveDir,fileTrunc,archiveDir)
    print ' Archive: ' + cmd
    os.system(cmd)

#===================================================================================================
# M A I N
#===================================================================================================

# Read the configuration file
config = ConfigParser.RawConfigParser()
config.read('jlabvideo.cfg')

print ""
archiveDir = config.get('Archive','dir')
print " Archive: %s"%(archiveDir)

serverHost = config.get('Server','host')
serverUser = config.get('Server','user')
serverDir = config.get('Server','webDir')
print " Server: %s@%s => %s"%(serverUser,serverHost,serverDir)

classFilesInstructors = config.get('ClassFiles','instructors')
classFilesStudents = config.get('ClassFiles','students')
print " Class Files: %s, %s"%(classFilesInstructors,classFilesStudents)
print ""

# make sure to record date and time when we start
cmd = 'date "+%y%m%d-%H%M%S"'
for line in os.popen(cmd).readlines():  # run command
    line = line[:-1]
    dateTime = line
print ' Date/Time: ' + dateTime

# Define string to explain usage of the script
usage  = "\nUsage: record.py --name=<name>\n"

valid = ['name=','video=','test','debug','help']
try:
    opts, args = getopt.getopt(sys.argv[1:], "", valid)
except getopt.GetoptError, ex:
    print usage
    print str(ex)
    sys.exit(1)

# read command line options
debug = False
test = False
video = '/dev/video1'
name = ''

for opt, arg in opts:
    if opt == "--help":
        print usage
        sys.exit(0)
    if opt == "--debug":
        debug = True
    if opt == "--test":
        test = True
    if opt == "--name":
        name = arg
    if opt == "--video":
        video = arg

# basic sanity tests
if name == '':
   print ' ERROR - no students name given.'

# get the instructors
instructorEmails = getInstructors(classFilesInstructors)

# get student to be recorded
(email,lastName,firstName) =  getStudent(classFilesStudents,debug)

# make sure we have a valid student
if lastName == '':
    print '\n ERROR - name not found in the list!\n'
    print usage
    sys.exit(1)

# prepare file name

fileTrunc = '%s-%s-%s'%(lastName,firstName,dateTime)
print " File trunc: %s"%(fileTrunc)
print ""

# mute/record/unmute
mute()
record(video,fileTrunc)
unMute()

# for test we stop here
if test:
    showVideo(fileTrunc)
    cleanup(fileTrunc)
    sys.exit(0)

# make php template
cmd = "cp template.php %s.php"%(fileTrunc)
os.system(cmd)

# copy the files to our server
cmd = "scp %s.* %s@%s:%s"%(fileTrunc,serverUser,serverHost,serverDir)
os.system(cmd)
url = 'http://%s/jlvideo/%s.php'%(serverHost,fileTrunc)
print ' Web page: ' + url

# send the email
cmd = 'echo " Your URL: %s" > url.tmp;cat template.eml url.tmp > %s.eml;rm url.tmp'%(url,fileTrunc)
os.system(cmd)
cmd  = "echo \"#!/bin/bash\n"
cmd += "mail -s 'Your Video is ready %s %s' -c %s %s < %s.eml\" > cmd.sh; chmod 750 cmd.sh"%\
       (firstName,lastName,instructorEmails,email,fileTrunc)
os.system(cmd)
cmd = "scp cmd.sh %s.eml %s@%s:"%(fileTrunc,serverUser,serverHost)
os.system(cmd)
cmd = "ssh %s@%s ./cmd.sh"%(serverUser,serverHost)
os.system(cmd)
cmd = "ssh %s@%s rm cmd.sh %s.eml "%(serverUser,serverHost,fileTrunc)
os.system(cmd)

# this needs to be archived
archive(archiveDir,fileTrunc)

# and exit!
sys.exit(0)
