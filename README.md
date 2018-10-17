# Book Share Pro

[Trello Project Management Board](https://trello.com/b/NCEfqRZA/book-dating-app-project)

## Application Summary
TBD

## Quick Start
1. Clone this repository.
1. In the terminal, run ```cd final_project```
1. Run ```touch .env```
1. In the .env file, paste the appropriate environment variables (ask a team member).
1. In a separate terminal instance, run ```psql```
1. Run ```CREATE DATABASE book_share;```
1. Back in the main terminal instance, run ```pipenv shell```
1. Run ```pipenv install```
1. Run ```./manage.py makemigrations```
1. Run ```./manage.py migrate```
1. Run ```./manage.py createsuperuser``` and follow the steps.
1. Run ```./manage.py runserver```
1. In your browser, navigate to ```localhost:8000/admin/``` and login with superuser credentials.
1. Under ```Sites``` click on ```Sites```
1. In the upper right, click on ```Add site +```
1. In the domain name field, type ```localhost:8000```. In the Display Name field, type ```Books Share```. Click ```Save```. On the top left, navigate back to ```Home```
1. On the admin console Home page, under ```Social Accounts```, click on ```Social Applications```. On this page, click on ```Add social application +```.
1. Under the provider dropdown, choose ```Facebook```.
1. In the ```Name``` field, type ```Books Share```.
1. In the ```Client id``` and ```Secret key``` fields, type in the App ID and App Secret from this app on ```https://developers.facebook.com/```
1. In the ```Sites``` field, select ```localhost:8000``` and click on the right arrow so it appears under ```Chosen sites```. Then click ```Save```.
1. Logout from the admin console.
1. Navigate to ```localhost:8000```.
1. Login using FB Oauth.

## Database Schema
TBD

## Quick deploying to AWS EC2
#### Deploying Django application to AWS EC2 instance (without Docker)

1. Create an EC2 instance and setup with a keypair using AWS console
1. From your root (after configuring .ssh/*.pem file), enter the AWS linux environment
    - `ssh <name of project>`

1. Inside the AWS linux environment, clone the repo and cd into repo
    - `git clone <repository>`
    - `cd <name of repo>`

1. Check for latest software update 
    - `sudo apt-get update && sudo apt-get upgrade -y`

1. Install essential applications/dependencies to linux console
    - ex. `sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx gunicorn psycopg2-binary -y`

1. Install virtual environment 'venv' and create directory with environement files name 'ENV'
    - `python3 -m venv ENV`

1. Activate the virtual environment
    - `source ENV/bin/activate`

1. Install application dependencies in virtual environment using pip or pip3
    - ex. `pip install psycopg2-binary django-allauth django-registration oauthlib python3-openid requests`

1. Save all the installed dependencies on to 'requirements.txt' file
    - `pip freeze > requirements.txt`

1. Open the activate file inside ENV/bin directory from root of your repository
    - `sudo nano ENV/bin/activate`

1. On the bottom of 'activate' file, place all of environment variables with 'export' infront (if value contains special characters, numbers, and letters, wrap around with single quotation).

    ex.
    ```
    export SECRET_KEY=''
    export DEBUG=
    export ALLOWED_HOSTS=['<AWS public DNS>',]
    export DB_NAME=
    export DB_HOST='<AWS RDS instance>'
    export DB_USER= <AWS RDS masteruser>
    export DB_PASSWORD= <AWS RDS masteruser password>
    export DB_PORT= (usually 5432)
    ```
1. Save and exit the file 
    - (EXIT) `CTL` + `x`
    - (SAVE) `y`
    - (CONFIRM) `Enter`

1. Exit out of virtual environment
    - `deactivate`

1. Exit out a directory from root of your repository
    - `cd ..`

1. Open and configure nginx file, remove existing content and paste with following information below:
    - `sudo nano /etc/nginx/nginx.conf`
    ```
    # nginx.conf
    user www-data;
    worker_processes 4;
    pid /var/run/nginx.pid;

    events {
        worker_connections 1024;
        # multi_accept on;
    }

    http {

        ##
        # Basic Settings
        ##

        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;
        # server_tokens off;

        server_names_hash_bucket_size 128;
        # server_name_in_redirect off;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        ##
        # Logging Settings
        ##

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        ##
        # Gzip Settings
        ##

        gzip on;
        gzip_disable "msie6";

        ##
        # Virtual Host Configs
        ##

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
    }
    ```
    - (EXIT) `CTL` + `x`
    - (SAVE) `y`
    - (CONFIRM) `Enter`

1. Configure nginx for your application
    - `sudo nano /etc/nginx/conf.d/<project_name>.conf`
    ```
    # <project name>.conf
    upstream <project name> {
        server 127.0.0.1:8000;
    }

    server {
        listen 80;

        server_name <AWS public DNS>;

        access_log  /home/ubuntu/.local/nginx.access.log;

        location / {
            proxy_set_header        Host $http_host;
            proxy_set_header        X-Real-IP $remote_addr;
            proxy_set_header        X-Forwarded-For  $proxy_add_x_forwarded_for;
            proxy_set_header        X-Forwarded-Proto $scheme;

            client_max_body_size    10m;
            client_body_buffer_size 128k;
            proxy_connect_timeout   120s;
            proxy_send_timeout      120s;
            proxy_read_timeout      120s;
            proxy_buffering         off;
            proxy_temp_file_write_size 64k;
            proxy_pass http://<name of project>;
            proxy_redirect          off;
        }
    }
    ```

1. Check the status of nginx
    - `sudo nginx -t`
    ```
    expect output:
    nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
    nginx: configuration file /etc/nginx/nginx.conf test is successful
    ```
    - Check the status: `sudo service nginx status`
        - restart if fails: `sudo service nginx restart`

1. Create and configure gunicorn  
    - `sudo nano /etc/systemd/system/gunicorn.service`
    ```
    [Unit]
    Description=gunicorn daemon
    After=network.target

    [Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/home/ubuntu/<name of repository>
    ExecStart=/home/ubuntu/<name of repository>/ENV/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/<name of repository>/<name of repository>.sock <direct parent directory of wsgi.py>.wsgi:application

    [Install]
    WantedBy=multi-user.target
    ```

1. Change directory into root of repository and start virtual environment
    - `source ENV/bin/activate`

1. Start up the gunicorn
    - `sudo systemctl enable gunicorn`
    - `sudo systemctl start gunicorn`
    - `sudo systemctl status gunicorn`
    - if fails, view error log:
        - `sudo tail -F /var/log/nginx/error.log`
    - test running gunicorn:
        - `gunicorn --bind 0.0.0.0:8000 <direct-parent-directory>.wsgi:application`



#### Cheat Sheet(most commonly used during debug) </br>
Venv </br>
     `source ENV/bin/activate` </br>
     `deactivate`</br>

Nginx </br>
     `sudo nano /etc/nginx/nginx.conf` </br>
     `sudo nano /etc/nginx/conf.d/<project_name>.conf` </br>
     `sudo service nginx status` </br>

Gunicorn </br>
     `sudo nano /etc/systemd/system/gunicorn.service` </br>
     `sudo systemctl stop gunicorn` </br>
     `sudo systemctl start gunicorn` </br>
     `sudo systemctl status gunicorn` </br>
     `gunicorn --bind 0.0.0.0:8000 <direct_parent_directory_of_wsgi.py>.wsgi:application`</br>

Error log </br>
     `sudo tail -F /var/log/nginx/error.log` </br>


### Authors:
- Andrew Baik
- Ben Hurst
- Liz Mahoney test test
- Roman Kireev
</br>
Verion 0.0.0
</br>
