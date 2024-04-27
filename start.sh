#!/bin/bash

# Run the ETL script
python etl.py

# Run the API after the ETL script has finished
python api.py
