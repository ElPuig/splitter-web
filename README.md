# splitter-web
Split SAGA based PDFs reports into student individual PDFs.

## Installation
Clone the repository into your web root folder.

Make sure `uploads/` and `batch/tmp/` directories are web writable.

## Requirements
	 sudo apt-get install python3
	
	 sudo apt-get install python3-pypdf2

## apache2 configuration: Virtual Host
	 <VirtualHost *:80>
		 ServerAdmin admin@splitter.local
		 ServerName www.splitter.local
		 ServerAlias splitter.local
		 DocumentRoot /var/www/splitter.local/public
		 ErrorLog ${APACHE_LOG_DIR}/error.log
		 CustomLog ${APACHE_LOG_DIR}/access.log combined
	 </VirtualHost>
