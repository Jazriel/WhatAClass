web: gunicorn start:app
deploy: python hdeploy.py
stop_deploy: kill `cat wac.pid`
create_db: python create_db.py
tests: coverage run test.py
report: coverage report
