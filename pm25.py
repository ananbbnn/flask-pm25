import pandas as pd
import pymysql

def open_db():
    conn=None
    try:
        conn=pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='12345678',
        db='demo'
        )
    except Exception as e:
        print("資料庫開啟失敗",e)
    return conn

def get_pm25_data_from_mysql():
    conn = None
    datas1,datas2,columns = None,None,None
    try:
        conn = open_db()
        cur=conn.cursor()
        sqlstr1='select * from pm25 where datacreationdate = (select MAX(datacreationdate) from pm25);'
        sqlstr2='select * from pm25 order by datacreationdate desc'
        cur.execute(sqlstr1)
        columns = [col[0] for col in cur.description]
        datas1 = cur.fetchall()
        cur.execute(sqlstr2)
        datas2 = cur.fetchall()
    except Exception as e: 
        print(e)
    finally:
        if conn is not None:
            conn.close()
    return datas1 ,datas2, columns


if __name__=="__main__":
    conn = open_db
    print(conn)
    datas=get_pm25_data_from_mysql()
    print(datas)