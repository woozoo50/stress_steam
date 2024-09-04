import matplotlib
matplotlib.use('Agg')  # GUI 백엔드 대신 비-GUI 백엔드 사용
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import plotly.graph_objects as go
import kaleido
from flask import Flask, render_template

class start:

    def __init__(self):
        print(123123)
        self.make_stress_go()
        print(123)
        self.make_stress_age()
        self.make_stress_gender()

    def make_stress_go(self):
        try:
            df_go = pd.read_csv('./static/고혈압2.csv')
            df_stress = pd.read_csv('./static/스트레스데이터.csv')
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return

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
        g.fig.savefig(save_path)  # FacetGrid 객체에서 `fig`를 통해 `savefig` 호출
        plt.close()  # 메모리 해제를 위해 그래프 닫기

        # 저장된 파일이 실제로 존재하는지 확인
        if not os.path.isfile(save_path):
            print("Error: 그래프 파일을 생성할 수 없습니다.")

    def make_stress_age(self):
        stress_gender = pd.read_csv("./static/스트레스남여.csv")

        # 남자만 가져오기
        man_stress = stress_gender.loc[3][2:].values

        # 여자만 가져오기
        woman_stress = stress_gender.loc[4][2:].values

        # 19~39
        youngMan_stress = (stress_gender.loc[5][2:].values + stress_gender.loc[6][2:].values) / 2
        # 40 ~ 59
        middleMan_stress = (stress_gender.loc[7][2:].values + stress_gender.loc[8][2:].values) / 2
        # 60세 이상
        oldMan_stress = (stress_gender.loc[9][2:].values + stress_gender.loc[10][2:].values) / 2

        woman_stress = woman_stress[9:]
        man_stress = man_stress[9:]
        oldMan_stress = oldMan_stress[9:]
        youngMan_stress = youngMan_stress[9:]
        middleMan_stress = middleMan_stress[9:]

        bar_width = 0.5
        years = list(map(int, range(2013, 2023)))

        plt.figure(figsize=(14, 6))
        plt.plot(years, youngMan_stress, ':o', color='k', label='청년')
        plt.plot(years, middleMan_stress, ':o', color='b', label='중년')
        plt.plot(years, oldMan_stress, ':o', color='g', label='노년')
        plt.xlabel('년도')
        plt.ylabel('스트레스 수치')
        plt.title('연령별 스트레스')
        plt.xticks(years)
        plt.legend()
        save_path = './static/stress_age.png'
        plt.savefig(save_path)  # 그래프를 저장할 경로
        plt.close()  # 메모리 해제를 위해 그래프 닫기

    def make_stress_gender(self):
        stress_gender=pd.read_csv("./static/스트레스남여.csv")
        man_stress=stress_gender.loc[3][2:].values

#여자만 가져오기
        woman_stress=stress_gender.loc[4][2:].values
        years = list(range(2013, 2023))
        fig = go.Figure()
        fig.add_trace(go.Bar(x=years,
                             y=man_stress,
                             name='남성',
                             marker_color='rgb(55, 83, 255)'
                             ))
        fig.add_trace(go.Bar(x=years,
                             y=woman_stress,
                             name='여성',
                             marker_color='rgb(255, 118, 109)'
                             ))

        fig.update_layout(
            title='남녀 스트레스',
            title_x=0.5,  # 타이틀을 중앙으로 정렬
            xaxis=dict(
                tickfont_size=14,
                dtick=1  # x축에 모든 년도가 표시되도록 설정
            ),
            yaxis=dict(
                title='스트레스 수치',
                titlefont_size=16,
                tickfont_size=14,
            ),
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            barmode='group',
            bargap=0.15,
            bargroupgap=0.1,
            width=1000,  # 그래프의 너비
            height=600   # 그래프의 높이
        )
        fig.write_image("./static/stress_gender.png")









