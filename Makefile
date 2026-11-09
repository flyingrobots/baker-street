.PHONY: test cases install

test:
	python3 -m unittest discover -s tests -v

cases:
	python3 evals/run.py list

install:
	python3 -m scripts.install
