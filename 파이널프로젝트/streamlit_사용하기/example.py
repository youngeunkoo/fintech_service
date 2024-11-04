import numpy as np
import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import json
from streamlit_elements import elements, mui, nivo, dashboard

# 페이지 설정
st.set_page_config(layout="wide")

# Streamlit Elements 레이아웃을 설정하여 드래그 가능한 대시보드 생성
with elements("dashboard"):
    # 대시보드 레이아웃 정의
    layout = [
        dashboard.Item("map", 0, 0, 8, 4),
        dashboard.Item("selection", 8, 0, 4, 2),
        dashboard.Item("radar_chart", 8, 2, 4, 2),
    ]
    
    with dashboard.Grid(layout):
        # 지도 위젯
        with mui.Paper(elevation=3, sx={"padding": 2}, key="map"):
            st.write("# 🚩 서울 분위기 지도 🚇")
            st.title("In Seoul")
            
            # 서울 행정구역 json 데이터 가져오기
            r = requests.get('https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json')
            seoul_geo = json.loads(r.content)

            # 지도 초기화
            m = folium.Map(location=[37.5665, 126.9780], tiles="Cartodb Positron", zoom_start=12)
            folium.GeoJson(seoul_geo, name='지역구').add_to(m)

            # 서울 구별 중심 좌표와 구 이름
            districts = {
                "종로구": [37.5735, 126.9792],
                "중구": [37.5641, 126.9979],
                "용산구": [37.5326, 126.9909],
                # 필요에 따라 추가 구역
            }

            # 각 구에 텍스트 표시
            for district, coords in districts.items():
                folium.Marker(
                    location=coords,
                    popup=district,
                    icon=folium.DivIcon(
                        html=f'<div style="font-size: 12pt; color: black; font-weight: bold;">{district}</div>',
                    )
                ).add_to(m)

            # Streamlit에서 지도 표시
            st_folium(m, width=700, height=500)

        # 지역 선택 위젯
        with mui.Paper(elevation=3, sx={"padding": 2}, key="selection"):
            st.markdown("<h3>서울 지역 선택</h3>", unsafe_allow_html=True)

            famous_places = ["명동", "홍대", "강남역", "이태원", "신촌"]
            emerging_places = ["망원동", "을지로", "성내동"]

            # 지역 유형 선택
            place_category = st.selectbox("지역 유형을 선택하세요:", ["유명 지역", "뜨는 지역"])
            if place_category == "유명 지역":
                selected_place = st.selectbox("지역을 선택하세요:", famous_places)
            else:
                selected_place = st.selectbox("지역을 선택하세요:", emerging_places)

            st.write("선택한 지역:", selected_place)

        # 레이더 차트 위젯
        with mui.Paper(elevation=3, sx={"padding": 2}, key="radar_chart"):
            st.markdown("<h3>지역 특성 비교</h3>", unsafe_allow_html=True)

            places = famous_places + emerging_places
            criteria = ["혼잡도", "활동성", "다양성"]

            # 지역1과 지역2 선택
            region1 = st.selectbox("지역1을 선택하세요:", places, key="region1")
            region2 = st.selectbox("지역2를 선택하세요:", places, key="region2")

            # 임의의 데이터 생성
            np.random.seed(0)
            data = {place: np.random.rand(3) * 10 for place in places}
            region1_data = data[region1]
            region2_data = data[region2]

            # Nivo Radar Chart
            with nivo.Radar():
                nivo.RadarChart(
                    data=[
                        {"criteria": c, region1: r1, region2: r2}
                        for c, r1, r2 in zip(criteria, region1_data, region2_data)
                    ],
                    keys=[region1, region2],
                    indexBy="criteria",
                    maxValue=10,
                    margin={"top": 70, "right": 80, "bottom": 40, "left": 80},
                    curve="linearClosed",
                    borderWidth=2,
                    borderColor={"from": "color"},
                    gridShape="circular",
                    colors={"scheme": "category10"},
                    fillOpacity=0.25,
                    dotSize=4,
                    dotColor={"theme": "background"},
                    dotBorderWidth=2,
                    dotBorderColor={"from": "color"},
                    enableDotLabel=True,
                    dotLabel="value",
                    dotLabelYOffset=-12,
                    legends=[
                        {
                            "anchor": "top-left",
                            "direction": "column",
                            "translateX": -50,
                            "translateY": -40,
                            "itemWidth": 80,
                            "itemHeight": 20,
                            "itemTextColor": "#999",
                            "symbolSize": 10,
                            "symbolShape": "circle",
                        }
                    ],
                )
