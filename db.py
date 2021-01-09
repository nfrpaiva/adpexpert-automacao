import config
import psycopg2
from datetime import datetime, timedelta
user = config.db_user
password = config.db_password
database = config.db_database
host = config.db_host

conn = psycopg2.connect(user=user, password=password,database=database, host=host)

def inserir_apontamento(data, colaborador, extra):
    dados =  (data, colaborador, extra)
    try:
        with conn.cursor() as cur:
            cur.execute("insert into apontamento (data, colaborador, extra) values (%s,%s,justify_interval(%s))", dados)
        if not config.read_only:
            conn.commit()
        else:
            conn.rollback();
            print("Rollback realizado. Trabalhando em modo read_only")
    except Exception as e:
        print(f"Ocorreu um erro ao grava apontamento no banco ({type(e)}): ", e)
