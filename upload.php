<?php
# https://www.w3schools.com/php/php_file_upload.asp

$target_dir = "uploads/";
// $target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploaded_file = $_FILES["fileToUpload"]["tmp_name"];
$fileType = "pdf";
$target_file = $target_dir . time() .".".$fileType;
$uploadOk = true;

// Check if the file is a pdf
if(isset($_POST["submit"])) {

    $finfo = finfo_open(FILEINFO_MIME_TYPE);
    
    if(finfo_file($finfo, $uploaded_file) === 'application/pdf') {
        echo "'{$uploaded_file}' is a PDF" . PHP_EOL;
        $uploadOk = true;
    } else {
        echo "'{$uploaded_file}' is not a PDF" . PHP_EOL;
        $uploadOk = false;
    }
    finfo_close($finfo);
}

// Check if file already exists
if (file_exists($target_file)) {
    echo "Sorry, file already exists.";
    $uploadOk = false;
}
// Check file size
if ($_FILES["fileToUpload"]["size"] > 25000000) {
    echo "Sorry, your file is too large.";
    $uploadOk = false;
}
// Allow certain file formats
if($fileType != "pdf" ) {
    echo "Sorry, only PDF files are allowed.";
    $uploadOk = false;
}
// Check if $uploadOk is set to 0 by an error
if (!$uploadOk) {
    echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.";
        # https://stackoverflow.com/questions/166944/calling-python-in-php
        // Call the ButlletinsSplitter
        
        echo '<pre>';

        // Outputs all the result of shellcommand "ls", and returns
        // the last output line into $last_line. Stores the return value
        // of the shell command in $retval.
        //print_r('python3 ButlletinsSplitter1.1.py '.$target_file);
        //$last_line = system('python3 ButlletinsSplitter1.1.py '.$target_file, $retval);

        /* Add redirection so we can get stderr. */
        $handle = popen('python3 ButlletinsSplitter1.1.py '.$target_file.' 2>&1', 'r');
        echo "'$handle'; " . gettype($handle) . "\n";
        $read = fread($handle, 2096);
        echo $read;
        pclose($handle);

        // Printing additional info
        echo '
        </pre>
        <hr />Last line of the output: ' . $last_line . '
        <hr />Return value: ' . $retval;


    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}

