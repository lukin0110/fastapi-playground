#!/bin/bash
echo "Run isort"
poetry run isort .
echo "Run black"
poetry run black .
echo "Run flake8"
poetry run flake8 .
echo "Run mypy"
poetry run mypy .
