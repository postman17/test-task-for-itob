db-init:
	python app.py db init

migrate:
	python app.py db migrate

upgrade:
	python app.py db upgrade

import-data:
	sqlite3 database.sqlite < data.sql