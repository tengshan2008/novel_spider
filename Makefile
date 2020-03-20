test:
	python tests/test_novel.py

start:
	nohup python -m novel 1>/dev/null 2>error.log &

half:
	nohup python -m novel --start 12 --desc 1>/dev/null 2>error.log &

loop:
	nohup python -m novel --loop 1>/dev/null 2>error.log &

stop:
	pkill novel
