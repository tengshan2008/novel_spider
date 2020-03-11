test:
	python tests/test.py

start:
	nohup python -m novel --start 1 1>/dev/null 2>error.log & !
