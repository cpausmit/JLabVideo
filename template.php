<?php

// File:   lookup.php
// Date:   February 1, 2005
// Author: P. Ragsdale - ragsdale@mit.edu
// Special thanks to I. Chuang <ike@media.mit.edu>
// Revised October 10, 2012 by J.D. Litster for VLC on jlvideo-2
// and again in April 2014 for EyeTV on a Macintosh

$fext = ".ap4"; // default
$fullpath_file= preg_replace("|.php$|","",$_SERVER['PHP_SELF']);
$avi_file = str_replace("/jlvideo/","",$fullpath_file);
if (file_exists($avi_file . ".mp4")) {
    $fext = ".mp4";
} else if (file_exists($avi_file . ".avi")) {
    $fext = ".avi";
} else if (file_exists($avi_file . ".mpg")) {
    $fext = ".mpg";
}

$base_directory = basename(dirname($_SERVER['PHP_SELF']));
$final_file = $avi_file . $fext;

//print "\n" . $final_file+"\n";

$dp = opendir(".");
$pwd = getcwd();
$countpath = ereg_replace("/","_",$pwd);
$countpath = str_replace("/","_",$pwd);
$countpath = "dir$countpath";
echo "<!DOCTYPE html><html><head></head><body bgcolor=\"#CCCCCC\">\n";

echo "<p style=\"font-family: arial;font-size: 28px;font-weight: bold;color:#900000;\">
<img src=\"mit-greywhite-footer3.gif\"> Junior Lab Orals Video</p>\n";

//echo "<p>fullpath_file = " . $fullpath_file;
//echo "<br/>avi_file = " . $avi_file;
//echo "<br/>final_file = " . $final_file;
//echo "<br/>countpath = " . $countpath . "</p>\n";

echo "<p>Videos from this server are in mp4 format with H.264 video and AAC audio.\n";
echo "<br/>They can be played with QuickTime on Macintosh and Windows machines.\n";
echo "<br/>On Linux machines, Mplayer and VLC, among others, should play them.</p>\n";
echo "<p>The files are at the full resolution of the video camera and\n";
echo "<br/>a 15-minute mp4 video is about 250-300 megabytes.</p>\n";
echo "<p>Most browsers will play these videos. To stream the video\n";
echo "<br/>and have your browser play it, just click the link below.\n";
echo "<br/>To download it to your computer first, right-click the link.</p>\n";


$ldash = strrpos($final_file, "-");
$short_name = substr($final_file, 0, $ldash);
echo "<h3>Link: <a href=$final_file>$short_name</a></h3>\n";

echo "</body></html>";
exit();

?>
