all: test

PYTHON ?= python3
TEST_DIRS = tests/

test:
	# $(PYTHON) -m pytest -vv $(TEST_DIRS)
	coverage run --source=. -m pytest -vv $(TEST_DIRS)

coverage:
	$(MAKE) test &> /dev/null ; coverage report -m 

install:
	pip3 install requests ;
	pip3 install kafka-python ;
	pip3 install psycopg2 ;
	pip3 install argparse ;
	pip3 install pytest ;
	pip3 install coverage

producer:
	$(PYTHON) site_monitoring.py -c myconfig.json -t "https://duckduckgo.com" -i 10

consumer:
	$(PYTHON) database_writer.py -c myconfig.json  

.PHONY: test coverage install producer consumer



