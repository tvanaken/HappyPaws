#!/bin/bash

set -e
set -x

# build ui bundle
cd ui
npm run build
npm test
