#!/bin/bash
echo "Running tests..."
export FLASK_CONFIG="Test"
pip install -e .

# Uncomment this line to debug tests
pytest --pdb --capture=no -vv /opt/code/$1  --cov-report html --cov

#pytest --capture=no -vv /opt/code/$1  --cov-report html --cov
