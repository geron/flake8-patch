.PHONY: init test lint format

CODE = flake8_patch
TEST = poetry run pytest --verbosity=2 --showlocals --strict

init:
	poetry install
	echo '#!/bin/sh\nmake lint test\n' > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

test:
	$(TEST) -k "$(k)"

lint:
	poetry run flake8 --jobs 4 --statistics --show-source $(CODE) tests
	poetry run pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	poetry run mypy $(CODE) tests
	poetry run black --target-version py36 --check $(CODE) tests

format:
	poetry run isort --apply --recursive $(CODE) tests
	poetry run black --target-version py36 $(CODE) tests

bump_major:
	poetry run bumpversion major

bump_minor:
	poetry run bumpversion minor

bump_patch:
	poetry run bumpversion patch
