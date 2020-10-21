#!/usr/bin/python
#====================================================================================================
#
# Record a oral presentation in MIT junior lab 8.13, create the web access file, copy both to the
# server and sent e-mail to the student and the instructors.
#
# Requirements:
#
# - install vlc, cheese and the relevant packages for ACC (mp4) codec support
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

def getZoomList(fileName,debug):
    # get the zoom files per student
    
    fileList = {}
    inputFile = open(fileName,'r')
    for line in inputFile.xreadlines():
        if len(line) == 0 or line[0] == '#':
            continue
        line = line[0:-1]
        items = line.split(',')
        email = items[0]
        zoomFile = "/home/paus/Documents/Zoom/%s"%(items[1])
        if debug:
            print ' Zoomfile(%s): %s'%(email,zoomFile)
        fileList[email] = zoomFile
            
    inputFile.close()

    return fileList
    
def mute():
    # before recording please mute (otherwise beeeeeeeeppppp)

    cmd =  "amixer set Master mute  >& /dev/null"
    print ' Mute speakers first: ' + cmd
    os.system(cmd)
    
def unMute():
    # after recording unmute so we can hear

    cmd =  "amixer set Master unmute >& /dev/null"
    print ' Mute speakers first: ' + cmd
    os.system(cmd)

def record(device,cheese,fileTrunc):    
    # here is the recording using vlc (nice tool) or the minimalistic cheese program

    # I do not really understand set of options available, this one seems to work (it is not HD 16:9)

    if cheese:
        cmd = 'cheese'
    else:
        cmd = "vlc v4l2://%s :input-slave=alsa://"%(device) + " :live-caching=600" + \
              " --sout '#transcode{vcodec=mp4v,acodec=mpga,ab=128}" + \
              ":duplicate{dst=display,dst=std{access=file,dst=%s.mp4}}' >& /dev/null"%(fileTrunc)
    

    print ' Recording: ' + cmd
    print '  --> PLEASE exit the vlc player and let the script complete.\n'
    os.system(cmd)

    # For cheese we need to find the file that was recorded and copy it to the right place
    if cheese:
        cmd = "ls -1rt $HOME/Videos/Webcam/*.webm | tail -1"
        for line in os.popen(cmd).readlines():  # run command
            line = line[:-1]
            file = line
        print " Copy: %s to ./%s.webm"%(file,fileTrunc)
        cmd = "cp %s ./%s.webm"%(file,fileTrunc)
        print "       %s"%(cmd)
        os.system(cmd)
    
def showVideo(fileTrunc):    
    cmd = "vlc %s.* >& /dev/null"%(fileTrunc)
    print ' Showing: ' + cmd
    print '  --> PLEASE exit the vlc player and let the script complete.\n'
    os.system(cmd)

def copyToServer(fileTrunc,serverUser,serverHost,serverDir):    
    # make php template
    cmd = "cp template.php %s.php"%(fileTrunc)
    os.system(cmd)
    # list them
    print ""
    cmd = "ls -lhrt %s.*"%(fileTrunc)
    os.system(cmd)
    print ""
    # copy the files to our server
    cmd = "scp %s.* %s@%s:%s"%(fileTrunc,serverUser,serverHost,serverDir)
    os.system(cmd)
    url = 'http://%s/jlvideo/%s.php'%(serverHost,fileTrunc)
    print ' Web page: ' + url
    return url

def makeEmail(fileTrunc,url,firstName,lastName,email,instructorEmails):
    cmd = 'echo " Your URL: %s" > url.tmp;cat template.eml url.tmp > %s.eml;rm url.tmp'%\
          (url,fileTrunc)
    os.system(cmd)
    cmd  = "echo \"#!/bin/bash\n"
    cmd += "mail -s 'Your Video is ready %s %s' -c %s %s < %s.eml\" > cmd.sh; chmod 750 cmd.sh"%\
           (firstName,lastName,instructorEmails,email,fileTrunc)
    #print "CMD: %s"%(cmd)
    os.system(cmd)
    
def sendEmail(fileTrunc,localEmail,mailUser,mailHost):
    # local email sent?
    if localEmail:
        #os.system('cat ./cmd.sh');
        os.system('./cmd.sh');
    # send it from remote
    else:
        cmd = "scp cmd.sh %s.eml %s@%s:"%(fileTrunc,mailUser,mailHost)
        os.system(cmd)
        cmd = "ssh %s@%s ./cmd.sh"%(mailUser,mailHost)
        os.system(cmd)
        # cleanup
        cmd = "ssh %s@%s rm cmd.sh %s.eml "%(mailUser,mailHost,fileTrunc)
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
# command line options and their defaults
debug = False
cheese = False
localEmail = True
test = False
name = ''
recover = ''
zoom = ''
extension = 'mp4'
device = '/dev/video0'

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

cheese = config.getboolean('Video','cheese')
device = config.get('Video','device')
if cheese:
    extension = 'webm'
print " Video options: cheese=%s, device=%s (file extension: %s)"%(cheese,device,extension)

mailHost = config.get('Mail','host')
mailUser = config.get('Mail','user')
print " Mail: %s@%s"%(mailUser,mailHost)

# done with options
print ""

# make sure to record date and time when we start
cmd = 'date "+%y%m%d-%H%M%S"'
for line in os.popen(cmd).readlines():  # run command
    line = line[:-1]
    dateTime = line
print ' Date/Time: ' + dateTime

# Define string to explain usage of the script
usage  = "\nUsage: record.py --name=<name> [ --zoom <FileList> ] || [ --recover <date>(=191008-153433) ]\n"

valid = ['name=','device=','recover=','zoom=','debug','cheese','localEmail','test','help']
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
    if opt == "--localEmail":
        localEmail = True
    if opt == "--cheese":
        cheese = True
    if opt == "--test":
        test = True
    if opt == "--name":
        name = arg
    if opt == "--recover":
        recover = arg
    if opt == "--zoom":
        zoom = arg
    if opt == "--device":
        device = arg

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

if recover != '':
    dateTime = recover
    print ' RECOVER MODE -- use date: %s'%(dateTime)

if zoom != '':
    print ' ZOOM MODE -- use date: %s'%(dateTime)
    zoomList = getZoomList(zoom,debug)
    print ' Zoom recording(%s): %s'%(email,zoomList[email])
    rc = os.system("cp %s %s/%s-%s-%s.mp4"%(zoomList[email],archiveDir,lastName,firstName,dateTime))
    print(" RC: %d"%(rc))
    if rc != 0:
        print(" ERROR - recording does not exist: %s"%(zoomList[email]))
        sys.exit(1)
    # go automatically to recover mode
    recover = 'zoom'
    
# prepare file name

fileTrunc = '%s-%s-%s'%(lastName,firstName,dateTime)
print " File trunc: %s"%(fileTrunc)
print ""

if recover != '':
    print ' RECOVER MODE -- no new recording'
    print '                 archive: %s'%(archiveDir)
    print '                 file is: %s'%(fileTrunc)
    videoFile = archiveDir +'/'+fileTrunc+'.'+extension
    if os.path.isfile(videoFile):
        print ' Found file -> recover.'
        os.system('mv '+videoFile+' ./')
        
else:
    # mute/record/unmute
    mute()
    record(device,cheese,fileTrunc)
    unMute()

# for test we stop here
if test:
    showVideo(fileTrunc)
    cleanup(fileTrunc)
    sys.exit(0)

# complete files and copy them to server
url = copyToServer(fileTrunc,serverUser,serverHost,serverDir)

# make and send the email
makeEmail(fileTrunc,url,firstName,lastName,email,instructorEmails)
sendEmail(fileTrunc,localEmail,mailUser,mailHost)

# this needs to be archived
archive(archiveDir,fileTrunc)

# and exit!
sys.exit(0)
