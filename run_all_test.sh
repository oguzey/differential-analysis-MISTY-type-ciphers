#!/bin/bash -e

cd dp_analyzer

export PYTHONPATH="$(pwd)"

pytest tests/test_variable.py
pytest tests/test_side.py
pytest tests/test_condition.py
