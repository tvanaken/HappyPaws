#!/bin/bash

set -e
set -x

poetry install
poetry run isort .
poetry run black --exclude ui .
poetry run flake8 --exclude=ui

