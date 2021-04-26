import os
import glob
import pandas as pd
from database_connector import GenericDatabaseConnector

db = GenericDatabaseConnector()
engine = db.engine
big_data = pd.concat(
    [pd.read_csv(data, sep=';') for data in glob.glob(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), r'../', r'../', 'data', '*.csv'))])

for _ in range(10):
    big_data.to_sql('big_table', con=engine, if_exists='append')