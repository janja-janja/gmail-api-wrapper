all: clean dist

clean:
	python setup.py clean --all
	rm -rf dist build

build:
	python setup.py build

tar_dist:
	python setup.py sdist

reinstall:
	which gmail-api-wrapper && pip uninstall -y gmail-api-wrapper || echo "no gmail-api-wrapper found"
	pip install .

whl_dist:
	python setup.py bdist_wheel -d dist/

publish: clean whl_dist
	twine upload dist/*

.PHONY: clean build dist all whl_dist reinstall
