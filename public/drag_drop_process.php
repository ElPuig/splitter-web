<?php
header('Content-Type: application/json');

define("PYTHON_SCRIPT", "ButlletinsSplitter.py");
define("PYTHON_SCRIPT_DIR", "../batch/");
define("RESULT_ZIP_FILE", "butlletins.zip");
define("RESULT_ZIP_URL", "/splitter.local/batch/tmp/");
define("UPLOAD_DIR", "../uploads/");

$uploaded_file = $_FILES["file"]["tmp_name"];
$fileType = "pdf";
$result_file = UPLOAD_DIR.time().".".$fileType;
if(!empty($uploaded_file)) {
	if (filesize($uploaded_file) > 25000000) {  // Check file size
	    echo "Sorry, your file is too large.\n";
	} elseif (filesize($uploaded_file) == 0) {  // Check file is not empty
	    echo "Sorry, your file is empty.\n";
	} elseif ($fileType != "pdf" ) {  // Allow only PDF format
	    echo "Sorry, only PDF files are allowed.\n";
	} else if (move_uploaded_file($uploaded_file,
        UPLOAD_DIR.time().".".$fileType)) {
            exec("python ".PYTHON_SCRIPT_DIR.PYTHON_SCRIPT." ".$result_file);
            $file_url = RESULT_ZIP_URL.RESULT_ZIP_FILE;

            // Send result file location to client
	        echo json_encode(array('zip' => $file_url));
	} else {
        echo "Sorry, the server experienced an internal error.\n";
   	}
} else {
 	echo "Sorry, there was an error uploading your file.\n";
}
?>
