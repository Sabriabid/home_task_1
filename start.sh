#!/bin/bash

# Exécuter le script ETL
python etl.py

# Exécuter l'API après que le script ETL ait terminé
python api.py
