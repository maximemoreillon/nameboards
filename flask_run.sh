#!/bin/bash


export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=main.py
python3.5 -m flask run --host=0.0.0.0
