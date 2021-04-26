"""
Database connector
"""
import logging
import urllib
import sqlalchemy as sa
from pandas import read_sql_query
import turbodbc
from turbodbc import make_options, Megabytes

class GenericDatabaseConnector:
    """
    Database connector definition
    """

    def __init__(self):
        """
        :param config:
        """
        try:
            #[].[dbo].[big_table]
            self.database = 'AdventureWorks2016'
            #[AdventureWorks2016].[Person].[Person]
            user = 'GFT\\ecsa'
            pwd = 'trusted'

            server = 'CRPC015162\SQLDEV'
            driver = 'ODBC+Driver+17+for+SQL+Server'
            driver = "{" + driver.replace("+", " ") + "}"

            options = make_options(read_buffer_size=Megabytes(100),
                                   parameter_sets_to_buffer=1000,
                                   varchar_max_character_limit=10000,
                                   use_async_io=True,
                                   prefer_unicode=True,
                                   autocommit=True,
                                   large_decimals_as_64_bit_types=True,
                                   limit_varchar_results_to_max=True)
            if pwd == 'trusted':
                self.cursor = turbodbc.connect(driver=driver, server=server, database=self.database,
                                               uid=user,
                                               Trusted_Connection='yes',
                                               turbodbc_options=options).cursor()
            else:
                self.cursor = turbodbc.connect(driver=driver,
                                               server=server,
                                               database=self.database,
                                               uid=user,
                                               pwd=pwd, turbodbc_options=options).cursor()

            con_string = f"DRIVER={driver};SERVER={server};DATABASE={self.database};Trusted_Connection=yes;" \
                if pwd == 'trusted' \
                else f"DRIVER={driver};" \
                     f"SERVER={server};" \
                     f"DATABASE={self.database};" \
                     f"UID={user};" \
                     f"PWD={pwd}"

            quoted = urllib.parse.quote_plus(con_string)
            self.engine = sa.create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))

        except turbodbc.exceptions.DatabaseError as ex:
            logging.exception(f"[Exception][database_connector][init][{str(ex)}]")

    def create_database_if_not_exists(self):
        """
        :return:
        """
        try:
            sql = f"""
                        IF NOT EXISTS (SELECT name FROM master.sys.databases WHERE name = N'{self.database}')
                            CREATE DATABASE {self.database}
                    """
            self.cursor.execute(sql)
        except turbodbc.exceptions.DatabaseError as ex:
            logging.exception(f"[Exception][database_connector]"
                              f"[CreateDataBaseIfnotExists][{0}]", str(ex))
