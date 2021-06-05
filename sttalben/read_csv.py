"""
Datum 02.06.2021
Autor jxkrause@posteo.de
Musikalbendatenbank
- Einlesen csv
"""
import argparse
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, ProgrammingError
import pandas as pd
from sttalben import *

def fill_tablea(df, con):
    df_alben = df[spalten_ausser_lieder].groupby(spalten_ausser_lieder, as_index=False).first()
    df_alben.to_sql(TABLE0, con, if_exists = 'append', index=False)
    #finde ids aus db
    df_db=pd.read_sql(TABLE0, con)
    df_id = df_alben.merge(df_db, on=spalten_ausser_lieder)
    return df_id

def fill_tableb(df, con, df_ids):
    df_lieder = df.merge(df_ids, on=spalten_ausser_lieder)
    df_lieder = df_lieder[['id', table_struct.iloc[-1,0]]]
    df_lieder.to_sql(TABLE1, con, if_exists = 'append', index=False)


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
        con.execute(f"SELECT * FROM {TABLE0} LIMIT 1")
    except (OperationalError, ProgrammingError):
        recreate_tables()
    #df.to_sql(TABLEV, con, if_exists = 'append', index=False)
    df_ids = fill_tablea(df, con)
    fill_tableb(df, con, df_ids)
    return df


def recreate_atable():
    """
    erzeugt DB-Tabelle neu (und löscht vorhandenen Inhalt)
    """
    con = create_engine(DB_URI)
    con.execute(f"DROP TABLE IF EXISTS {TABLE0}")
    create_sql = f"CREATE TABLE {TABLE0}  ("
    create_sql = create_sql + "	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
    for row in table_struct.iloc[:-1].iterrows():
        name = row[1].iloc[0]
        dtype = row[1].iloc[1]
        create_sql = create_sql + f"\"{name}\" {dtype},"
    create_sql = create_sql[:-1] + ')'
    print(create_sql)
    con.execute(create_sql)

def recreate_ltable():
    """
    erzeugt DB-Tabelle neu (und löscht vorhandenen Inhalt)
    """
    con = create_engine(DB_URI)
    con.execute(f"DROP TABLE IF EXISTS {TABLE1}")
    create_sql = f"CREATE TABLE {TABLE1}  ("
    create_sql = create_sql + "	id INTEGER,"
    name = table_struct.iloc[-1,0]
    dtype = table_struct.iloc[-1,1]
    create_sql = create_sql + f"\"{name}\" {dtype},"
    create_sql = create_sql[:-1] + ')'
    print(create_sql)
    con.execute(create_sql)

def recreate_vtable():
    """
    erzeugt DB-Tabelle neu (und löscht vorhandenen Inhalt)
    """
    con = create_engine(DB_URI)
    con.execute(f"DROP VIEW IF EXISTS {TABLEV}")
    create_sql = f"CREATE VIEW {TABLEV}  AS SELECT "
    for row in table_struct.iterrows():
        name = row[1].iloc[0]
        create_sql = create_sql + f"\"{name}\","
    create_sql = create_sql[:-1] + f' FROM {TABLE0},{TABLE1} WHERE {TABLE0}.id = {TABLE1}.id'
    print(create_sql)
    con.execute(create_sql)


def recreate_tables():
    recreate_atable()
    recreate_ltable()
    recreate_vtable()

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
        recreate_tables()

    if args.template:
        write_header()

    for x in args.fn:
        read_from_csv(x)
