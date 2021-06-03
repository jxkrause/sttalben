"""
Datum 02.06.2021
Autor jxkrause@posteo.de
Musikalbendatenbank
- Einlesen csv
"""
import argparse
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import pandas as pd
from sttalben import DB_URI, TABLE, table_struct


def read_from_csv(fn):
    """
    Liest Alben-Information aus csv-Datei (Trenner ;)
    und füllt DB damit
    """
    print(fn)
    df = pd.read_csv(fn, sep=';')
    df.fillna(method='ffill', inplace=True)
    con = create_engine(DB_URI)
    try:
        con.execute(f"SELECT * FROM {TABLE} LIMIT 1")
    except OperationalError:
        recreate_table()
    df.to_sql(TABLE, con, if_exists = 'append')
    return df

recreate_query = [f"DROP TABLE IF EXISTS {TABLE}",
"""
CREATE TABLE alben (
	"index" INT,
	"Künstler" TEXT,
	"AlbumTitel" TEXT,
	"Erscheinungsjahr" INT,
	"Liedertitel" TEXT
)
"""]

def recreate_table():
    """
    erzeugt DB-Tabelle neu (und löscht vorhandenen Inhalt)
    """
    con = create_engine(DB_URI)
    con.execute(f"DROP TABLE IF EXISTS {TABLE}")
    create_sql = f"CREATE TABLE {TABLE}  ("
    for row in table_struct.iterrows():
        name = row[1].iloc[0]
        dtype = row[1].iloc[1]
        create_sql = create_sql + f"\"{name}\" {dtype},"
    create_sql = create_sql[:-1] + ')'
    con.execute(create_sql)

    for query in recreate_query:
        con.execute(query)

def write_header():
    lst = table_struct.iloc[:,0].to_list()
    print(';'.join(lst))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lesen Alben aus csv')
    parser.add_argument('fn', nargs='*', help='List von Dateinamen')
    parser.add_argument('-r', '--recreate', help='Tabelle neugenerieren',
                    action='store_true')
    parser.add_argument('-t', '--template', 
        help='Erzeuge Kopfzeile für csv-Datei', action='store_true')

    args = parser.parse_args()

    if args.recreate:
        recreate_table()

    if args.template:
        write_header()

    for x in args.fn:
        read_from_csv(x)
