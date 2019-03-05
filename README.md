## Junior Lab Video Recording Package

Record a oral presentation in MIT junior lab 8.13, create the web access file, copy both to the server and sent e-mail to te student and the instructors.

## Example

./record.py --name Paus --video /dev/video0


## Requirements

### Packages

Install vlc and the relevant packages for ACC (mp4) codec support

### Authentication

Put your public key (usually $HOME/.ssh/id_rsa.pub) into the server file (serverUser@serverHost:.ssh/authorized_keys) to avoid having to type the password

## Configuration

The configuration file is jlabvideo.cfg. Contents

### [Archive]
Describes the archive where for backup purposes all recorded files get stored.
* dir - directory on your local computer where recorded videos get stored as a backup is all fails

### [Server]
Describes all relevant parameters for the server where the video recordings get stored and published.
* user - is the user under which you will login
* host - the host name of the web server
* webdir - directory that is used to hold videos

### [ClassFiles]
All lists to describe the class
* instructors - csv file with instructors (email,lastName,firstName)
* students - csv file with students (email,lastName,firstName)

### [Video]
Parameters used to configure the video
* device - which device is used: /dev/video0, etc.
* cheese - if 'True' cheese is used as a video recording tool (less integrated but more reliable)
