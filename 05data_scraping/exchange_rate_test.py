
# DB에 접속해서 저장하는 함수
def exchange_rate_info_to_db(df):
    from sqlalchemy import create_engine
    import pymysql
    from dbenv import db, dbtype, id, pw, host, database
    from datetime import date
    pymysql.install_as_MySQLdb()

    today = str(date.today()).replace("-","")

    engine = create_engine("%s+%s://%s:%s@%s/%s" % (db, dbtype, id, pw, host, database))
    conn = engine.connect()
    df.to_sql(f"exchange_rate_info", con=conn, if_exists='append', index=False)
    conn.close()

    return print(f"{'저장완료':<30s}", end="\r")
exchange_rate_info_to_db(df)


