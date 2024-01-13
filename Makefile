install: # Install project
	poetry install

update: # Update dependencies
	poetry update

gendiff: # Run script "gendiff"
	poetry run gendiff

build: # Build project
	poetry build

publish: # Imitate publishing
	poetry publish --dry-run

package-install: # Install package
	python3 -m pip install --user dist/*.whl

package-reinstall: # Reinstall package
	python3 -m pip install --user dist/*.whl --force-reinstall

lint: # Run flake8
	poetry run flake8

test: # Run pytest
	poetry run pytest

coverage: # Run coverage
	poetry run coverage run -m pytest
	poetry run coverage xml