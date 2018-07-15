<?php
define("PYTHON_SCRIPT", "ButlletinsSplitter.py");
define("PYTHON_SCRIPT_DIR", "../batch/");
define("RESULT_ZIP_FILE", "butlletins.zip");
define("RESULT_ZIP_FILE_DIR", "../batch/tmp/");
define("UPLOAD_DIR", "../uploads/");

$uploaded_file = $_FILES["fileToUpload"]["tmp_name"];
$fileType = "pdf";
$target_file = UPLOAD_DIR.time().".".$fileType;
$uploadOk = true;
// Check PDF file type
if(isset($_POST["submit"])) {
    $finfo = finfo_open(FILEINFO_MIME_TYPE);
    
    if(finfo_file($finfo, $uploaded_file) === 'application/pdf') {
        $uploadOk = true;
    } else {
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

// Check file is not empty
if ($_FILES["fileToUpload"]["size"] == 0) {
    echo "Sorry, your file is empty.";
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

        // Call the ButlletinsSplitter        
        $ret_val = exec("python ".PYTHON_SCRIPT_DIR.PYTHON_SCRIPT." ".$target_file, $ret_val);
      
        // Download zip file
        $file = RESULT_ZIP_FILE_DIR.RESULT_ZIP_FILE;

        if (headers_sent()) {
            echo 'HTTP header already sent';
        } else {
            if (!is_file($file)) {
                header($_SERVER['SERVER_PROTOCOL']." 404 Not Found");
                echo "File not found";
            } else if (!is_readable($file)) {
                header($_SERVER['SERVER_PROTOCOL']." 403 Forbidden");
                echo "File not readable";
            } else {
                header($_SERVER['SERVER_PROTOCOL']." 200 OK");
                header("Content-type: application/zip"); 
                header("Content-Transfer-Encoding: Binary");
                header("Content-Length: ".filesize($file));
                header("Content-Disposition: attachment; filename=\"".basename($file)."\"");

                // Disable cache
                header("Expires: " .gmdate('D, d M Y H:i:s') ." GMT");
                header("Cache-control: private");
                header("Pragma: private");

                ob_end_clean();
                readfile($file);


                // Delete uploaded file
                system("rm -rf ".UPLOAD_DIR."*.pdf");

                // Delete temp files
                system("rm -rf ".RESULT_ZIP_FILE_DIR."*.pdf");

                // Delete result file
                unlink($file);

                exit();
            }
        }

    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}
?>
