# Application enviroment setup

## Enviroment variables
For dev and production.
+ For convenience, an `.env` file is provided and may contain needed enviroment variables.
+ Make a copy of `.env.example` and name it `.env`.
+ Setup your local enviroment configurations on the `.env` file.

## PostgreSQL
For dev and production.
+ Install postgresql (`apt install postgresql`)
+ In psql console (`sudo -u postgres psql`)
	```
	CREATE DATABASE db_name;
  	CREATE USER django WITH PASSWORD 'passwd';
  	ALTER ROLE django SET client_encoding TO 'utf-8';
  	ALTER ROLE django SET timezone TO 'UTC';
  	GRANT ALL PRIVILEGES ON DATABASE db_name TO django;
	```
+ Allow password authentication to postgres (in `/etc/postgresql/13/main/pg_hba.conf`)
  + CHANGE local all all peer ----> local all all md5
+ Restart postgres (`systemctl restart postgresql`)
+ To test, connect to psql with `psql <DATABASE> <USER>`

## Python
For dev and production.
+ Install python3-pip python3-dev libpq-dev
+ Install poetry by running:
```shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
+ Run `poetry install` (for development) or `poetry install --no-dev` (for production) in the directory of the project.
+ Use `poetry shell` to enter the virtual environment, or adjust your editor/IDE accordingly.
+ (For development) Run `pre-commit install`.

## Nginx
Only for production.
+ Install NGINX (`apt install nginx`)
+ Create conf at `/etc/nginx/sites-available/project_name.conf`
+ Link (`ln -s project_name.conf ../sites-enabled/`)

### /etc/nginx/sites-available/project_name.conf
```
upstream django {
	server unix:///tmp/uwsgi-web.sock;
}

server {
	listen 80;
	listen [::]:80;
	server_name EXAMPLE.COM IP.IP.IP.IP;

	location /media {
		alias /srv/NAME/current/media;
	}
	location /dist {
		alias /srv/NAME/current/static;
		expires 1M;
		add_header Cache-Control "public";
	}

	location / {
		uwsgi_pass django;
		include /srv/NAME/uwsgi_params;
	}
}
```

### /srv/NAME/uwsgi_params
```
uwsgi_param  QUERY_STRING       $query_string;
uwsgi_param  REQUEST_METHOD     $request_method;
uwsgi_param  CONTENT_TYPE       $content_type;
uwsgi_param  CONTENT_LENGTH     $content_length;

uwsgi_param  REQUEST_URI        $request_uri;
uwsgi_param  PATH_INFO          $document_uri;
uwsgi_param  DOCUMENT_ROOT      $document_root;
uwsgi_param  SERVER_PROTOCOL    $server_protocol;
uwsgi_param  REQUEST_SCHEME     $scheme;
uwsgi_param  HTTPS              $https if_not_empty;

uwsgi_param  REMOTE_ADDR        $remote_addr;
uwsgi_param  REMOTE_PORT        $remote_port;
uwsgi_param  SERVER_PORT        $server_port;
uwsgi_param  SERVER_NAME        $server_name;
```

## uWSGI
Only for production.
+ Install uWSGI package (`pip install uwsgi`)
+ Create vassals directory (`mkdir -p /etc/uwsgi/vassals/`)
+ Create /etc/systemd/system/uwsgi.service
+ Autostart uWSGI at boot: `systemctl enable uwsgi`

### /etc/uwsgi/vassals/NAME.ini
```
[uwsgi]
chdir=/srv/NAME/current
module=web.wsgi:application
home=/srv/NAME/current
chmod-socket=666

master=True
processes=4
vacuum=True
max-requests=5000
harakiri=20

socket=/tmp/uwsgi-web.sock
safe-pidfile=/tmp/uwsgi-web.pid
daemonize=/srv/NAME/log/web.log
```

### /etc/systemd/system/uwsgi.service
```
[Unit]
Description=uWSGI Emperor service

[Service]
ExecStartPre=/bin/bash -c 'mkdir -p /run/uwsgi; chown root:www-data /run/uwsgi'
ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```


## Deploy
### /srv/NAME/deploy.sh
```
REPO="https://github.com/USERNAME/REPO-NAME.git"
BRANCH="master"
PROJECT_PATH="/srv/NAME"
URL="https://ramosuc.cl/"

name=$(date +%Y%m%d%H%M%S)
echo "Deploy started at $name"

cd $PROJECT_PATH
echo "Clone repository"
git clone $REPO --branch=$BRANCH --depth=1 --quiet $name
python3 -m virtualenv $name

cd $PROJECT_PATH/$name
ln -s $PROJECT_PATH/.env $PROJECT_PATH/$name/.env
ln -s $PROJECT_PATH/settings.json $PROJECT_PATH/$name/scrape/settings.json
rm -rf $PROJECT_PATH/$name/media
ln -s $PROJECT_PATH/media $PROJECT_PATH/$name/media

source bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py collectstatic

echo "Deploying"
ln -nfs $PROJECT_PATH/$name $PROJECT_PATH/current
echo "Symlink created"

echo "Reload uWSGI"
touch /etc/uwsgi/vassals/ramosuc.ini

echo "Remove old deployments"
cd $PROJECT_PATH
find . -maxdepth 1 -name "20*" | sort | head -n -4 | xargs rm -Rf

echo "Deployment finished."
echo "Status code for $URL"
curl --write-out "%{http_code}\n" --silent --output /dev/null $URL
```

### /srv/NAME/rollback.sh
```
ln -nfs $path/$(find . -maxdepth 1 -name "20*" | sort | tail -n 2 | head -n1) $path/current
```
