.PHONY: validate build ci clean install scrape update-readme

install:
	pip install -r requirements.txt

validate:
	python scripts/validate.py

build:
	python scripts/build.py

scrape:
	python scripts/scrape.py

update-readme:
	python scripts/update_readme.py

ci: validate build

all: validate build scrape update-readme

clean:
	rm -rf dist/ scraped/
