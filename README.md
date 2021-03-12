# splitter-web
Split SAGA PDF reports ("butlletins") into student individual PDFs. Count passed and evaluated UF from SAGA PDF reports ("actes").

## Installation
Clone the repository into your web root folder.

Make sure `uploads/` and `script/tmp/` directories are web writable.

## Requirements
```
sudo apt install apache2
sudo apt install php libapache2-mod-php
sudo apt install python3
sudo apt install python3-pypdf2	
```

## Apache configuration: VirtualHost
```
<VirtualHost *:80>
	ServerAdmin admin@splitter.local
	ServerName www.splitter.local
	ServerAlias splitter.local
	DocumentRoot /var/www/html/splitter.local/public
	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

## How to run
Start the server with:

`sudo systemctl start apache2`


Visit localhost:80 from your browser.
