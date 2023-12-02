#!/bin/bash

set -e
set -x

poetry install --no-root 


if [[ $* == *--exclude-db* ]]
then
  poetry run pytest -vs --ignore=tests/db
else
  poetry run pytest -vs
fi

