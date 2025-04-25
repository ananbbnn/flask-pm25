from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
import pymysql


app = Flask(__name__)

@app.route("/")
def index():
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
    return render_template('index.html',name=username,now=nowtime,books=books)

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
    return render_template('bmi.html',bmi=bmi,height=height,weight=weight)




app.run(debug=True)