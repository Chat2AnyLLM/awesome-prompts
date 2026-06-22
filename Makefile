.PHONY: validate build ci clean install

install:
	pip install -r requirements.txt

validate:
	python scripts/validate.py

build:
	python scripts/build.py

ci: validate build

clean:
	rm -rf dist/
