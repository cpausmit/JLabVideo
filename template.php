<?php

$debug = 0;
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

// Write the html header

echo "<!DOCTYPE html><html><head></head>";
echo "<style>";
echo "a:link    {color:#000000; background-color:transparent; text-decoration:none}";
echo "a:visited {color:#009000; background-color:transparent; text-decoration:none}";
echo "a:hover   {color:#900000; background-color:transparent; text-decoration:underline}";
echo "a:active  {color:#900000; background-color:transparent; text-decoration:underline}";
echo "body.ex   {margin-top: 0px; margin-bottom: 25px; margin-right: 25px; margin-left: 25px;}";
echo "</style>";
echo "<body class=\"ex\" bgcolor=\"#EEEEEE\">\n";
echo "<p style=\"font-family: arial;font-size: 28px;font-weight: bold;color:#900000;\">
      <img src=\"mit-logo.png\" height=\"40\"> Video of a Junior Lab Oral</p>\n";

// Core text for the file

echo "<p style=\"font-family: arial;font-size: 18px;font-weight: medium;color:#404040;\">\n";
echo "Videos from this server are in formats that can be played with all normal video players.<br>\n";
echo "Most browsers will play these videos. To stream the video and have your browser play it,<br>\n";
echo "left-click the link below or right-click and download it.<br>\n";

// Write the file link

echo "<p style=\"font-family: arial;font-size: 18px;font-weight:medium;color:#009000;\">\n";
echo "<a href=$file>$file</a>\n";

// Debugging output

if ($debug>0) {
  echo "<p style=\"font-family: arial;font-size: 18px;font-weight: medium;color:#007000;\">\n";
  echo "== Debugging ==<br/>";
  echo "<br/>fullFile Trunc = " . $fullFileTrunc;
  echo "<br/>file Trunc     = " . $fileTrunc;
  echo "<br/>file           = " . $file;
}

// Write the html footer

echo "</body></html>";
exit();

?>
