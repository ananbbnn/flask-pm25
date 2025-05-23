import pandas as pd
import pymysql



def update_db():
    api_url = 'https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=540e2ca4-41e1-4186-8497-fdd67024ac44&limit=1000&sort=datacreationdate%20desc&format=CSV'
    sqlstr = '''
        insert ignore into pm25(site,county,pm25,datacreationdate,itemunit)
        values(%s,%s,%s,%s,%s) 
        '''
    row_count = 0
    message = ''
    try:
        df = pd.read_csv(api_url)
        df['datacreationdate'] = pd.to_datetime(df['datacreationdate'])
        df1 = df.dropna()
        values = df1.values.tolist()

        conn = open_db()
        cur = conn.cursor()
        cur.executemany(sqlstr,values)
        row_count = cur.rowcount
        conn.commit()
        print(f'更新{row_count}筆資料')
        message = '更新資料庫成功!'

    except Exception as e:
        print(e)
        message = f'更新失敗:{e}'

    return row_count,message

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
    return columns,datas1 ,datas2


if __name__=="__main__":
    update_db()