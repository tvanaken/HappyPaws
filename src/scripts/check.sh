#!/bin/bash

set -e
set -x

poetry install
poetry run black --check --exclude ui .
poetry run isort . --check-only
poetry run flake8 --exclude=ui

cd ui
npm ci
npm run check

