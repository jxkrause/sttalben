from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

_version_ = '0.1' 

DB_URI = os.getenv('DB_URI')
TABLE='alben'

table_struct = pd.read_csv('conf/columns.txt', sep=' ', header=None)