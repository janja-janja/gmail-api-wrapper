all: clean dist

clean:
	python setup.py clean --all
	rm -rf dist build

build:
	python setup.py build

dist:
	python setup.py sdist

reinstall:
	which gmail-api-wrapper && pip uninstall -y gmail-api-wrapper || echo "no gmail-api-wrapper found"
	pip install .

.PHONY: clean build dist all reinstall
