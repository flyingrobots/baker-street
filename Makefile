.PHONY: test cases

test:
	python3 -m unittest discover -s tests -v

cases:
	python3 evals/run.py list
