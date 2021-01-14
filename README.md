# splitter-web
Split SAGA PDF reports ("butlletins") into student individual PDFs. Count passed and evaluated UF from SAGA PDF reports ("actes").

## Installation
Clone the repository into your web root folder.

Make sure `uploads/` and `batch/tmp/` directories are web writable.

## Requirements
```
sudo apt install apache2
sudo apt install php7-4-cli
sudo apt install php libapache2-mod-php
sudo apt-get install python3	
sudo apt-get install python3-pypdf2
sudo apt install default-jdk
sudo apt install python3-pip
pip3 install tika
```
[Install Apache Tika](https://thecustomizewindows.com/2018/06/how-to-install-apache-tika-on-ubuntu/)

## Crontab configuration
Add the following line to your crontab:
```
@reboot bash /var/www/html/splitter.local/batch/tika_server_start.sh &
```

## Apache configuration: VirtualHost
```
<VirtualHost *:80>
	ServerAdmin admin@splitter.local
	ServerName www.splitter.local
	ServerAlias splitter.local
	DocumentRoot /var/www/splitter.local/public
	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

