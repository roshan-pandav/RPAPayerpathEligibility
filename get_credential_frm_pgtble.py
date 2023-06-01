import pg8000
import pandas as pd

def get_conn(database, username, password, host, port):
    conn = pg8000.Connection(database=database,
                             user=username,
                             password=password,
                             host=host,
                             port=port)
    return conn
def SelectQueryToGetDataframe(conn, table_name):
    try:
        cursor = conn.cursor()
        postgreSQL_select_Query = f'select * from {table_name}'
        cursor.execute(postgreSQL_select_Query)
        dataFrame = pd.read_sql(postgreSQL_select_Query, conn)
        conn.commit()
        conn.close()
        return dataFrame
    except Exception as error:
        print(error)
        dataFrame=pd.DataFrame()

        return dataFrame

