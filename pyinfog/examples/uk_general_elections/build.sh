#!/bin/bash

export PYTHONPATH=`pwd`/../../..:$PYTHONPATH

python3 download_uk_election_data.py
python3 som_ukelection.py
python3 hemicycle_ukelection.py
python3 transition_ukelection.py
