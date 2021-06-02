from sqlalchemy import create_engine
import pandas as pd
import argparse
from sttalben import DB_URI, TABLE


def read_from_csv(fn):
    df = pd.read_csv(fn, sep=';')
    df.fillna(method='ffill', inplace=True)
    con = create_engine(DB_URI)
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
    con = create_engine(DB_URI)
    for query in recreate_query:
        con.execute(query)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lesen Alben aus csv')
    parser.add_argument('fn', nargs='*', help='List von Dateinamen')
    parser.add_argument('-r', '--recreate', help='Tabelle neugenrieren',
                    type=bool, default = False)
    args = parser.parse_args()

    if args.recreate:
        recreate_table()

    for x in args.fn:
        df = read_from_csv(x)
        print(df)