<?php

$extension = ".ap4"; // unimportant default

$fullFileTrunc = preg_replace("|.php$|","",$_SERVER['PHP_SELF']);
$fileTrunc = str_replace("/jlvideo/","",$fullFileTrunc);

// Find out which type of video file was produced and determine the file name

if (file_exists($fileTrunc . ".webm")) {
    $extension = ".webm";
} else if (file_exists($fileTrunc . ".mp4")) {
    $extension = ".mp4";
} else if (file_exists($fileTrunc . ".avi")) {
    $extension = ".avi";
} else if (file_exists($fileTrunc . ".mpg")) {
    $extension = ".mpg";
}
$file = $fileTrunc . $extension;

// Get the base directory on our server

//$dir = basename(dirname($_SERVER['PHP_SELF']));
$dp = opendir(".");
$pwd = getcwd();
$countpath = ereg_replace("/","_",$pwd);
$countpath = str_replace("/","_",$pwd);
$countpath = "dir$countpath";

// Write the html header

echo "<!DOCTYPE html><html><head></head><body bgcolor=\"#CCCCCC\">\n";
echo "<p style=\"font-family: arial;font-size: 28px;font-weight: bold;color:#900000;\">
      <img src=\"mit-greywhite-footer3.gif\"> Junior Lab Orals Video</p>\n";

// Debugging output
//
//echo "<p>fullFile Trunc = " . $fullFileTrunc;
//echo "<br/>file Trunc   = " . $fileTrunc;
//echo "<br/>file         = " . $file;
//echo "<br/>countpath    = " . $countpath . "</p>\n";

// Core text for the file

echo "<p>\n"
echo "Videos from this server are in formats that can be played with all normal video players.<br>\n";
echo "Most browsers will play these videos. To stream the video and have your browser play it,<br>\n";
echo "left-click the link below or right-click and download it.<br>\n";

// Write the file link

$ldash = strrpos($file,"-");
$name = substr($file, 0, $ldash);
echo "<h3>Link: <a href=$file>$name</a></h3>\n";

// Write the html footer

echo "</body></html>";
exit();

?>
