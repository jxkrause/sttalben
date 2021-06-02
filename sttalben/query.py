"""
Datum 02.06.2021
Autor jxkrause@posteo.de
Musikalbendatenbank
- Abfragen cli
"""
import argparse
from sqlalchemy import create_engine
import pandas as pd
from sttalben import table_struct, DB_URI, TABLE

def search(args):
    """
    sucht in der Datenbank nach Alben und Liedern
    args ist ein Namespace-Objekt wie von 'argparse' erzeugt
    """
    args_dict = vars(args)
    ausgabe = args.full
    if ausgabe == -1:
        #automatischer Modus: wenn Lieder in Abfrage vorhanden -> 1 sonst ->
        wert = args_dict.get(table_struct.iloc[-1,0], None)
        if wert is None:
            ausgabe = 0
        else:
            ausgabe = 1

    #baue Abfrage String
    query = f"SELECT * FROM {TABLE} "
    konjunktion = ['WHERE','AND']
    num = 0
    for row in table_struct.iterrows():
        name = row[1].iloc[0]
        wert = args_dict.get(name, None)
        if not wert is None:
            query = query + konjunktion[num] + f" {name} =  '{wert}' "
            num = 1
    #print('-->',query)

    #hole Datem
    con = create_engine(DB_URI)
    df_lieder = pd.read_sql_query(query, con)
    if df_lieder.empty:
        return ("Kein Album gefunden", None)

    #Auasgage
    if ausgabe == 0:
        spalten_ausser_lieder = table_struct.iloc[:-1,0].tolist()
        df_alben = df_lieder[spalten_ausser_lieder].groupby(spalten_ausser_lieder, as_index=False).first()
        return ("Gefundene Alben", df_alben)

    spalten_ausser_index = table_struct.iloc[:,0].tolist()
    return ("Gefundene Lieder", df_lieder[spalten_ausser_index])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Datenbank Abfragen Muski Alben')
    for row in table_struct.iterrows():
        name = row[1].iloc[0]
        parser.add_argument('-'+name[0], '--'+name, help=name)
    parser.add_argument('-f', '--full',
        type=int, default=-1,
        help='Ausgabe (1) alle Lieder, (0) nur Alben, (-1 default) automatisch')

    args = parser.parse_args()

    text, df = search(args)
    print(text)
    if not df is None:
        print(df)
