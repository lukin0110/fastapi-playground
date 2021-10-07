#!/bin/bash
echo "Run isort"
isort .
echo "Run black"
black .
echo "Run flake8"
flake8 .
echo "Run mypy"
mypy .
