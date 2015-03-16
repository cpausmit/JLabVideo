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

if (file_exists($avi_file . ".webm")) {
    $fext = ".webm";
} else if (file_exists($avi_file . ".mp4")) {
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

echo "<p>Videos from this server are in formats that can be played with all normal video players.<br>\n";
echo "Most browsers will play these videos. To stream the video and have your browser play it,<br>\n";
echo "just left click the link below or right click and download it.<br>\n";

$ldash = strrpos($final_file, "-");
$short_name = substr($final_file, 0, $ldash);
echo "<h3>Link: <a href=$final_file>$short_name</a></h3>\n";

echo "</body></html>";
exit();

?>
