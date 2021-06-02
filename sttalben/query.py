from sqlalchemy import create_engine
import argparse
from sttalben import table_struct, DB_URI
import pandas as pd

def search(args):
    query = "SELECT * FROM alben "
    konjunktion = ['WHERE','AND']
    num = 0
    for k,v in vars(args).items():
        if not v is None:
            query = query + konjunktion[num] + f" {k} =  '{v}' "
            num = 1 
            #print(k,v,)
    print('-->',query)
    con = create_engine(DB_URI)
    df = pd.read_sql_query("SELECT * FROM alben WHERE Erscheinungsjahr =  '1959'",con)
    print(df)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Datenbank Abfragen Alben')
    for row in table_struct.iterrows():
        name = row[1].iloc[0]
        parser.add_argument('-'+name[0], '--'+name, help=name)

    args = parser.parse_args()

    search(args)