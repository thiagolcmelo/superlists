Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv

eg, on Ubuntu:
sudo apt-get install nginx git python3 python3-pip
sudo apt-get install virtualenv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Upstart Job

* see gunicorn_staging_superlists.template.service
* replace SITENAME with, eg, staging.superlists-thiagolcmelo.tk

## Folder structure:
Assume we have a user account at /home/username

/home/username
- sites
-- SITENAME
-- database
-- source
-- static
-- virtualenv

## Directives for webserver configuration

SITENAME="superlists-thiagolcmelo.tk"
SITEDAEN="gunicorn_production_superlists"
cd deploy_tools/
sed "s/SITENAME/$SITENAME/g" nginx.template.conf | sudo tee /etc/nginx/sites-available/$SITENAME
sudo ln -s /etc/nginx/sites-available/$SITENAME /etc/nginx/sites-enabled/$SITENAME
sudo service nginx reload
sed "s/SITENAME/$SITENAME/g" "$SITEDAEN.template.service" | sudo tee "/etc/systemd/system/$SITEDAEN.service"
sudo systemctl start $SITEDAEN
