from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
import pymysql
import json
from pm25 import get_pm25_data_from_mysql ,update_db, get_pm25_data_by_site, get_all_counties, get_sites_by_county

nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
app = Flask(__name__)


@app.route("/filter", methods=["POST"])
def filter_data():
    county = request.form.get("county")
    columns, datas1, datas2 = get_pm25_data_from_mysql()
    df = pd.DataFrame(datas1,columns=columns)
    df1 = df.groupby("county").get_group(county).groupby("site")["pm25"].mean()
    print(df1)
    return {"county": county}



@app.route("/")
def index():
    columns, datas1, datas2 = get_pm25_data_from_mysql()
    df = pd.DataFrame(datas1,columns=columns)
    counties = sorted(df['county'].unique().tolist())
    
    county = request.args.get("county", "ALL")
    if county == "ALL":
        df1 = df.groupby("county")["pm25"].mean().reset_index()
        x_data = df1['county'].to_list()
    else:
        
        # 取得特定縣市的資料
        df = df.groupby("county").get_group(county)
        x_data = df['site'].to_list()

    columns = df.columns.tolist()
    datas = df.values.tolist()
    y_data = df['pm25'].to_list()


    return render_template('index.html',
                           datas1=datas1,
                           datas2=datas2,
                           columns=columns,
                           counties=counties,
                           select_county=county,
                           x_data=x_data,
                           y_data=y_data
                           )

@app.route("/pm25-data-site")
def pm25_data_by_site():
    county = request.args.get('county')
    site = request.args.get('site')

    if not county or not site:
        result = json.dumps({"error":"縣市或站點名稱不正確!"}, ensure_ascii=False)
    else:
        
        columns ,datas = get_pm25_data_by_site(county,site)
        df = pd.DataFrame(datas,columns=columns)
        date = df['datacreationdate'].apply(lambda x: x.strftime("%Y-%m-%d %H"))
        result = {
            "county":county,
            "site":site,
            "x_data" : date.to_list(),
            "y_data" : df['pm25'].to_list(),
            "higher": df["pm25"].max(),
            "lower" : df["pm25"].min(),
                }
    return result

@app.route("/pm25-site")
def pm25_site():
    counties = get_all_counties()

    return render_template('pm25-site.html',counties=counties)

@app.route("/pm25-county-site")
def pm25_county_site():
    county = request.args.get("county")
    sites = get_sites_by_county(county)
    result = json.dumps(sites, ensure_ascii=False)
    return result


@app.route("/update-db")
def update_pm25_db():
    count, message = update_db()
    result = json.dumps(
        {'時間': nowtime,'更新比數':count,'結果':message}, ensure_ascii=False) 
    return result

@app.route("/books")
def books_price():
    books={
        1:{
        "name":"Python book",
        "price":299,
        "image_url":"https://im2.book.com.tw/image/getImage?i=https://www.books.com.tw/img/CN1/136/11/CN11361197.jpg&v=58096f9ck&w=348&h=348"
        },

        2:{

        "name":"Java book",
        "price":399,
        "image_url":"https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/087/31/0010873110.jpg&v=5f7c475bk&w=348&h=348"
        },

        3:{
        "name":"C# book",
        "price":499,
        "image_url":"https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/036/04/0010360466.jpg&v=62d695bak&w=348&h=348"
        },
        }
    

    username = 'Harold'
    nowtime = datetime.now().strftime("%Y-%m-%d")
    print(username,nowtime)
    return render_template('books.html',name=username,now=nowtime,books=books)

@app.route('/pm25-data')
def get_pm25_data():
    api_url = 'https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=540e2ca4-41e1-4186-8497-fdd67024ac44&limit=1000&sort=datacreationdate%20desc&format=CSV'
    df = pd.read_csv(api_url)
    df["datacreationdate"] = pd.to_datetime(df["datacreationdate"])
    df1 = df.dropna().values.tolist()
    return render_template('pm25.html',info=df1)
    
@app.route('/bmi')
def get_bmi():
    weight = request.args.get('weight')
    height = request.args.get('height')
    bmi = round(eval(weight)/((eval(height)/100)**2),3)
    return render_template('bmi.html', **locals())



if __name__=="__main__":
    app.run(debug=False)