.PHONY: clean-pyc clean test lint install bootstrap

clean-pyc:
    find . -name '*.pyc' -exec rm --force {} +
    find . -name '*.pyo' -exec rm --force {} +
    find . -name '*~' -exec rm --force  {} +

clean:
	rm -f MANIFEST
	rm -rf build dist
	rm -rf *.egg-info

test:
	sh -c '. _virtualenv/bin/activate; nosetests tests'

lint:
    flake8 --exclude=.tox

install: test
	python setup.py sdist bdist_wheel #upload
	make clean

register:
	python setup.py register

bootstrap: _virtualenv
	_virtualenv/bin/pip install -e .
ifneq ($(wildcard test-requirements.txt),)
	_virtualenv/bin/pip install -r test-requirements.txt
endif
	make clean

_virtualenv:
    virtualenv _virtualenv
    _virtualenv/bin/pip install --upgrade pip
    _virtualenv/bin/pip install --upgrade setuptools

help:
    @echo "    clean-pyc"
    @echo "        Remove python artifacts."
    @echo "    clean-build"
    @echo "        Remove build artifacts."
    @echo "    lint"
    @echo "        Check style with flake8."
    @echo "    test"
    @echo "        Run nose test"
