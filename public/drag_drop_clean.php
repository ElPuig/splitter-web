<?php
    header('Content-Type: application/json');

	define("RESULT_ZIP_FILE", "butlletins.zip");
	define("RESULT_ZIP_FILE_DIR", "../batch/tmp/");
    define("UPLOAD_DIR", "../uploads/");


    function clean_uploaded_file() {
		system("rm -rf ".UPLOAD_DIR."*.pdf");
	}


    function clean_temp_files() {
		system("rm -rf ".RESULT_ZIP_FILE_DIR."*.pdf");
	}


	function clean_result_file() {
		system("rm -rf ".RESULT_ZIP_FILE_DIR.RESULT_ZIP_FILE);
	}


	clean_uploaded_file();
	clean_temp_files();
	clean_result_file();
?>
