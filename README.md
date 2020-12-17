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

## How to use the splitter without web

Into the `batch/` directory you will find two scripts:

 ButlletinsSplitter.py

 SagaSplit.sh

Choose one according to your needs, being SagaReport.pdf the report that you have downloaded from Saga.

 python3 ButlletinsSplitter.py SagaReport.pdf

 sh SagaSplit.sh SagaReport.pdf

