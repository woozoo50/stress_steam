import matplotlib
from flask import Flask,render_template
from flask import request
import pandas as pd
import seaborn as sns
import csv
import os
from server import start_input
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from flask import Flask, send_file
from io import BytesIO



import csv
import numpy as np

app=Flask(__name__)
@app.route('/')
def index():
    #start_instance=start_input.start()
    # return "메인 페이지"
    return  render_template('index.html')
@app.route('/social')
def social():
    return render_template('social.html')
@app.route('/individual')
def individual():
    return render_template('individual.html')
@app.route('/qwer')
def map():
    return render_template('qwer.html')
@app.route('/season')
def get_season():
    seasons=["봄","여름","가을","겨울"]
    season="여름"
    return render_template('season.html',season=season,seasons=seasons)
@app.route('/stress_go')
def stress_go():
    # 데이터 파일 읽기
    try:
        df_go = pd.read_csv('./static/고혈압2.csv')
        df_stress = pd.read_csv('./static/스트레스데이터.csv')
    except FileNotFoundError as e:
        return f"Error: {e}"

    # 불필요한 열 삭제
    df_go.drop('시군구별(1)', axis=1, inplace=True)
    df_stress.drop('시군구별(1)', axis=1, inplace=True)

    # 데이터 평탄화
    go_list = df_go.values.flatten()
    stress_list = df_stress.values.flatten()

    # 새로운 데이터프레임 생성
    df_stress_go = pd.DataFrame({
        '고혈압': go_list,
        '스트레스': stress_list
    })

    # 디렉토리 존재 여부 확인 및 생성
    if not os.path.exists('./static'):
        os.makedirs('./static')

    # 그래프 설정 및 생성
    plt.rc('font', family='AppleGothic')
    g = sns.lmplot(x='스트레스', y='고혈압', data=df_stress_go, height=6, aspect=2)

    plt.title('고혈압과 스트레스 수준 간의 관계')
    plt.xlabel('스트레스 수준')
    plt.ylabel('고혈압 수치')

    save_path = './static/stress_go.png'
    g.savefig(save_path)  # 그래프를 저장할 경로
    plt.close()  # 메모리 해제를 위해 그래프 닫기

    # 저장된 파일이 실제로 존재하는지 확인
    if not os.path.isfile(save_path):
        return "Error: 그래프 파일을 생성할 수 없습니다."

    return render_template('stress_go.html')


@app.route("/loop")
def get_loop():
    item=['a','b','c','d']
    return  render_template("loop.html",items=item)
@app.route("/calc",methods=['GET','POST'])
def calculate():
    if request.method=="POST":
        #폼에 입력된 글자는 문자 이미르ㅗ 숫자로 변환
        temp=''
        try:
            num=int(request.form['num'])
            if num %2==0:
                temp='짝수'
            else:
                temp='홀수'
            return render_template("calcresult.html",temp=temp,num=num)
        except ValueError as e:
            num=request.form['num']
            erroMessage=f'{num}이 정수임???????????'
            return render_template("calculate.html",erroMessage=erroMessage)
    else:
        return render_template("calculate.html")


if __name__=="__main__":
    app.run(debug=True)

