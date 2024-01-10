install: # Install project
	poetry install

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