#!/bin/bash
venv_dir="rentdrivepre"

if [ ! -d "$venv_dir" ]; then
    python3 -m venv "$venv_dir"
    echo "Creating virtual environment"
fi

source "$venv_dir/bin/activate"
echo "Installing dependencies"
pip install -e .

python3 execute.py "$@"

deactivate
