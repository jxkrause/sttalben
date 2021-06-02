"""
Datum 02.06.2021
Autor jxkrause@posteo.de
Musikalbendatenbank
- Einlesen csv
- Abfragen cli
- getestete Datenbanken sqite3
"""
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

_version_ = '0.1'

DB_URI = os.getenv('DB_URI')
TABLE='alben'

#struktur der Tabell wird hier gespeichert, letzte Spalte sind die Lieder
table_struct = pd.read_csv('conf/columns.txt', sep=' ', header=None)
