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
install_dir = os.path.dirname(os.path.abspath(__file__))
conf_file = os.path.join(install_dir, 'columns.txt')
table_struct = pd.read_csv(conf_file, sep=' ', header=None)
