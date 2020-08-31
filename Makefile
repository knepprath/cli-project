test:
	python -m unittest -b

integration:
	behave

lint:
    pre-commit run --all-files