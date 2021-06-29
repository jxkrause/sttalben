"""
Datum 02.06.2021
Autor jxkrause@posteo.de
Musikalbendatenbank
- Einlesen csv
"""
import argparse
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.sql import select
import pandas as pd
from sttalben import *

def insert_new(con, df, tablename, columns):
    """
    nur Datensätze einfügen die neu sind
    con: Datenbankverbindung
    df: pandas DataFrame
    tablename: Tabellenname
    columns: Liste der Tabellennamen die gleich sein müssen (oder nicht)
    """
    meta = MetaData()
    table = Table(tablename, meta, autoload_with=con)
    ins = table.insert()
    for _,row in df.iterrows():
        sel = select([table])
        for col in columns:
            sel = sel.where(table.c[col]==row[col])
        res = con.execute(sel)
        if len(list(res)) == 0:
            con.execute(ins, row.to_dict())


def fill_table_alben(df, con):
    """
    Daten aus pandas in Datenbank -> Alben
    return pandas DataFrame mit ids
    """
    df_alben = df[spalten_ausser_lieder].groupby(spalten_ausser_lieder, as_index=False).first()
    insert_new(con, df_alben, TABLE0, spalten_ausser_lieder)
    #finde ids aus db
    df_db=pd.read_sql(TABLE0, con)
    df_id = df_alben.merge(df_db, on=spalten_ausser_lieder)
    return df_id

def fill_table_lieder(df, con, df_ids):
    """
    Daten aus pandas in Datenbank -> Lieder
    """
    df_lieder = df.merge(df_ids, on=spalten_ausser_lieder)
    df_lieder = df_lieder[['id', table_struct.iloc[-1,0]]]
    insert_new(con, df_lieder, TABLE1, df_lieder.columns)

def read_from_csv(fn):
    """
    Liest Alben-Information aus csv-Datei (Trenner ;)
    und füllt DB damit
    """
    df = pd.read_csv(fn, sep=';')
    df.fillna(method='ffill', inplace=True)
    con = create_engine(DB_URI)
    try:
        con.execute(f"SELECT * FROM {TABLE0} LIMIT 1")
    except (OperationalError, ProgrammingError):
        recreate_all_tables()
    df_ids = fill_table_alben(df, con)
    fill_table_lieder(df, con, df_ids)
    return df


def recreate_alben_table():
    """
    erzeugt DB-Tabelle neu (und löscht vorhandenen Inhalt)
    """
    con = create_engine(DB_URI)
    con.execute(f"DROP TABLE IF EXISTS {TABLE0}")
    create_sql = f"CREATE TABLE {TABLE0}  ("
    create_sql = create_sql + "	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
    for _,row in table_struct.iloc[:-1].iterrows():
        name = row.iloc[0]
        dtype = row.iloc[1]
        create_sql = create_sql + f"\"{name}\" {dtype},"
    create_sql = create_sql[:-1] + ')'
    #print(create_sql)
    con.execute(create_sql)

def recreate_lieder_table():
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
    #print(create_sql)
    con.execute(create_sql)

def recreate_albenlieder_view():
    """
    erzeugt DB-Tabelle neu (und löscht vorhandenen Inhalt)
    """
    con = create_engine(DB_URI)
    con.execute(f"DROP VIEW IF EXISTS {TABLEV}")
    create_sql = f"CREATE VIEW {TABLEV}  AS SELECT "
    for _,row in table_struct.iterrows():
        name = row.iloc[0]
        create_sql = create_sql + f"\"{name}\","
    create_sql = create_sql[:-1] + f' FROM {TABLE0},{TABLE1} WHERE {TABLE0}.id = {TABLE1}.id'
    #print(create_sql)
    con.execute(create_sql)


def recreate_all_tables():
    "Erzeuge Tabellen und Ansicht in Datenbank"
    recreate_alben_table()
    recreate_lieder_table()
    recreate_albenlieder_view()

def write_header():
    "Kopfzeile eine csv-Datei zur Eingabe"
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
        recreate_all_tables()

    if args.template:
        write_header()

    for x in args.fn:
        read_from_csv(x)
