from sqlalchemy import create_engine
from exdbinfo import db, dbtype, id, pw, host, database   
# MySQL 의 database="hanabank_info" 에 테이블 저장됨 
# from exdbinfo import db, dbtype, id, pw, host, news_database  
# from naver_api_info import news_database
import pymysql
import time


pymysql.install_as_MySQLdb()

# exchange_rate 용
# sql 불러와서 아이디랑 비번 
def db_connect():
    engine = create_engine("%s+%s://%s:%s@%s/%s" % (db, dbtype, id, pw, host, database))
    conn = engine.connect()
    return conn

# DB에 접속해서 저장하는 함수
def exi_to_db(table_name, date, df):
    conn = db_connect()
    df.to_sql(table_name, con=conn, if_exists='append', index=False) 
    conn.close()
    
    return print(f"{table_name}_{date}, {'저장완료':<30s}", end="\r")




# # 네이버 뉴스용
# # sql 불러와서 아이디랑 비번 
# def news_db_connect():
#     engine = create_engine("%s+%s://%s:%s@%s/%s" % (db, dbtype, id, pw, host, news_database))
#     conn = engine.connect()
#     return conn

# # DB에 접속해서 저장하는 함수
# def news_to_db(table_name, date, df):
#     conn = news_db_connect()
#     df.to_sql(table_name, con=conn, if_exists='append', index=False) 
#     conn.close()
    
#     return print(f"{table_name}_{date}, {'저장완료':<30s}", end="\r")