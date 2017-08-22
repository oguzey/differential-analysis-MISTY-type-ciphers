#!/bin/bash

cd dp_analyzer
MYPYPATH="$(pwd):$(pwd)/data" mypy --python-version 3.5 **/*.py
