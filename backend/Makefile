APP_NAME := coffee

deps:
	pip install -r requirements.txt

run:
	FLASK_APP=./src/api.py FLASK_DEBUG=true flask run

start-db-server:
	pg_ctl -D /usr/local/var/postgres start

stop-db-server:
	pg_ctl -D /usr/local/var/postgres stop

connect-to-db:
	psql $(APP_NAME)