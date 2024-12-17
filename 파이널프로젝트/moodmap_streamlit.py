import folium
import requests
import json
from folium.plugins import MarkerCluster
from folium.features import DivIcon
from folium import Marker, Popup, Icon
import streamlit as st
from streamlit_folium import st_folium
from streamlit_elements import elements, mui, html
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from dotenv import load_dotenv
import os
import openai
import pandas as pd
from streamlit.components.v1 import html
import time

place_result = pd.read_csv('./place_result.csv')

# load_dotenv에 파일 경로를 지정
load_dotenv("./.env_openai")

openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit 페이지 설정
st.set_page_config(layout="wide")

# JavaScript로 모바일 감지 코드 삽입
st.markdown(
    """
    <script>
        const isMobile = window.innerWidth < 768;
        window.parent.postMessage({isMobile}, "*");
    </script>
    """,
    unsafe_allow_html=True
)

# Streamlit에서 받은 메시지를 통해 모바일 상태 업데이트
if "is_mobile" not in st.session_state:
    st.session_state.is_mobile = False

# 페이지 새로고침 여부를 확인하기 위한 상태
if "page_loaded" not in st.session_state:
    st.session_state.page_loaded = False

# 페이지가 처음 로드되었을 때 한 번만 새로고침
if not st.session_state.page_loaded:
    st.markdown(
        """
        <script>
            window.location.reload();  // 페이지를 강제로 새로고침
        </script>
        """,
        unsafe_allow_html=True
    )
    st.session_state.page_loaded = True  # 새로고침이 반복되지 않도록 설정

# 모바일 여부 설정 함수
def set_mobile_status(is_mobile):
    st.session_state.is_mobile = is_mobile
    
    # 새로운 입력이 있을 때 메시지를 초기화하는 함수
def reset_message():
    st.session_state["show_thank_you"] = False

# 입력 완료 후 입력 필드 초기화하는 함수
def save_input():
    plus_region = st.session_state["input_text"]
    if plus_region and plus_region != st.session_state["last_saved_region"]:
        # 파일에 새로운 지역 이름 추가
        with open("추가하고 싶은 지역.txt", "a") as f:
            f.write(plus_region + "\n")
        
        # 세션 상태 업데이트
        st.session_state["last_saved_region"] = plus_region
        st.session_state["show_thank_you"] = True  # "의견 감사합니다" 메시지를 표시하도록 설정
        st.session_state["input_text"] = ""  # 입력 완료 후 입력 필드를 초기화
        
# <head> 태그용 Google Tag Manager 코드
gtm_head_code = """
<!-- Google Tag Manager -->
<script>
  (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-WRGV87W7');
</script>
<!-- End Google Tag Manager -->
"""

# <body> 태그용 백업 iframe 코드
gtm_body_code = """
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-WRGV87W7"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
"""

# <head> 부분에 삽입
html(gtm_head_code, height=0)

# <body> 부분에 해당하는 백업용 코드 삽입
html(gtm_body_code, height=0)

# # Google Analytics 코드 추가
# google_analytics_code = """
# <script async src="https://www.googletagmanager.com/gtag/js?id=G-69PRS1XSXE"></script>
# <script>
#   window.dataLayer = window.dataLayer || [];
#   function gtag(){dataLayer.push(arguments);}
#   gtag('js', new Date());
#   gtag('config', 'G-69PRS1XSXE');
# </script>

# <script>
#   // 드롭다운 선택, 버튼 클릭, 마커 클릭 이벤트 추적 함수
#   function trackEvent(eventName, eventCategory, eventLabel) {
#     console.log("Event triggered:", eventName, eventCategory, eventLabel); // 디버깅용 로그
#     gtag('event', eventName, {
#       'event_category': eventCategory,
#       'event_label': eventLabel
#     });
#   }

#   // MutationObserver를 사용하여 만족도 조사 링크 클릭 추적
#   document.addEventListener("DOMContentLoaded", function() {
#     const observer = new MutationObserver((mutations) => {
#       mutations.forEach((mutation) => {
#         if (mutation.addedNodes) {
#           mutation.addedNodes.forEach((node) => {
#             if (node.classList && node.classList.contains("small-button")) {
#               node.addEventListener("click", function() {
#                 trackEvent("Satisfaction_Survey_Click", "Link", "Satisfaction Survey");
#               });
#               observer.disconnect();  // 이벤트가 추가되면 observer 중지
#             }
#           });
#         }
#       });
#     });
# </script>
# """
# st.markdown(google_analytics_code, unsafe_allow_html=True)

# 지역 목록 정의
famous_places = ["명동", "홍대", "강남역", "이태원", "신촌", "여의도", "북촌", "성수동", "청담동", "연남동"]
emerging_places = ["망원동", "을지로", "성내동", "문래동", "봉천동", "녹사평", "도곡동", "불광동", "장위동", "수색동"]

# 서울 행정구역 json 파일 로드 (로컬 파일로 불러오기)
with open('seoul_municipalities_geo_simple.json', 'r', encoding='utf-8') as f:
    seoul_geo = json.load(f)


# 지도 초기화: 서울 중심으로 설정
m = folium.Map(location=[37.5665, 126.9780], tiles="Cartodb Positron", zoom_start=11)
folium.GeoJson(seoul_geo, name='지역구').add_to(m)

folium.plugins.LocateControl().add_to(m)

# 서울 구별 중심 좌표와 구 이름
districts = {
    "종로구": [37.5735, 126.9792],
    "중구": [37.5631, 126.9979],
    "용산구": [37.5326, 126.9909],
    "성동구": [37.5636, 127.0379],
    "광진구": [37.5384, 127.0822],
    "동대문구": [37.5744, 127.0396],
    "중랑구": [37.6063, 127.0925],
    "성북구": [37.5894, 127.0167],
    "강북구": [37.6396, 127.0253],
    "도봉구": [37.6659, 127.0318],
    "노원구": [37.6543, 127.0565],
    "은평구": [37.6177, 126.9227],
    "서대문구": [37.5794, 126.9368],
    "마포구": [37.5663, 126.9019],
    "양천구": [37.5172, 126.8664],
    "강서구": [37.5509, 126.8495],
    "구로구": [37.4955, 126.8874],
    "금천구": [37.4563, 126.8956],
    "영등포구": [37.5264, 126.8963],
    "동작구": [37.5124, 126.9394],
    "관악구": [37.4784, 126.9514],
    "서초구": [37.4836, 127.0327],
    "강남구": [37.5172, 127.0473],
    "송파구": [37.5145, 127.1050],
    "강동구": [37.5301, 127.1238]
}

# 각 구에 텍스트 표시
for district, coords in districts.items():
    folium.Marker(
        location=coords,
        icon=DivIcon(
            icon_size=(150, 36),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 12pt; color: black; font-weight: bold;">{district}</div>',
        )
    ).add_to(m)
    
# 각 지역에 대한 마커 추가
locations = [
    {
        "name": "명동",
        "coords": [37.5636, 126.9869],
        "description": "대형 브랜드 매장과 화장품, 패션 아이템이 밀집해 있으며, 한류와 관광이 결합된 상권",
        "image": "https://cdn.thescoop.co.kr/news/photo/202305/57665_89482_111.jpg"
    },
    {
        "name": "홍대",
        "coords": [37.5563, 126.9220],
        "description": "독립적인 상점과 카페, 스트리트 아트, 클럽과 공연장 등 다양한 문화 콘텐츠가 있는 지역",
        "image":"https://i.namu.wiki/i/6v8oGwuvwQTt85VnupCSsfQ1S2oXX24eAgts7d9M-8EGfR5-lXRj8bIScJbvzNGCmNC0YcSCzz1cmJudjIcGaW19oAmPfd8UA-smwkEfJK0IvGSfUidx3LsVdf9gLHJAQ-xSdUukYS7teB7XN_x_zQ.webp"
    },
    {
        "name": "강남역",
        "coords": [37.4979, 127.0276],
        "description": "회사와 사무실 밀집, 고급 브랜드, 다양한 음식점과 쇼핑 시설이 모여 있는 지역",
        "image":"https://i.namu.wiki/i/KJmURamoD2t16saSVzLomUJOQ1hNjOicO06lwQIwdB5gHhgMF8uyRp9aCjkVJ9h01RLdn2Y8Q1tPykUumTiKDQ.webp"
    },
    {
        "name": "이태원",
        "coords": [37.5340, 126.9948],
        "description": "다국적 레스토랑과 바, 외국인이 많이 찾는 문화 중심지로 다양한 글로벌 문화를 경험할 수 있는 장소",
        "image": "https://minio.nculture.org/amsweb-opt/multimedia_assets/165/85860/94092/c/%EC%9D%B4%ED%83%9C%EC%9B%90%EA%B1%B0%EB%A6%AC-%288%29_rev-medium-size.jpg"
    },
    {
        "name": "신촌",
        "coords": [37.5585, 126.9394],
        "description": "대학가 특유의 분위기로 인해 저렴하고 접근성이 좋은 카페와 음식점, 청년층을 겨냥한 상업시설이 많은 지역",
        "image":"https://www.sdm.go.kr/lib/culture/images/contents/sub2000/img_sub2050_1.png"
    },
    {
        "name": "여의도",
        "coords": [37.5219, 126.9245],
        "description": "비즈니스 중심지이자 한강공원이 있는 지역",
        "image": "https://i.namu.wiki/i/TcpbZAY5CetJ-RIQknixiIikj0t5WGF_c6nNiWEJxgbZJUbtbgY-RL3UxYndV6EsGHS9bKjRZigFhFk1ndglBA.webp"
    },
    {
        "name": "북촌",
        "coords": [37.5843, 126.9830],
        "description": "한옥과 현대적 갤러리가 어우러져 있어 관광객과 문화 애호가가 선호하는 지역",
        "image":"https://korean.visitseoul.net/data/kukudocs/seoul2133/20220518/202205181617250471.jpg"
    },
    {
        "name": "성수",
        "coords": [37.5447, 127.0558],
        "description": "창의적이고 개성 있는 카페와 독립 상점이 많아 MZ 세대가 많이 찾는 지역",
        "image": "https://blog.igisam.com/app/uploads/2023/01/%EA%B7%B8%EB%A6%BC2-2-1024x682.jpg"
    },
    {
        "name": "청담",
        "coords": [37.5197, 127.0474],
        "description": "명품 매장과 고급 레스토랑이 있어 패션과 럭셔리를 중시하는 소비자들이 찾는 지역",
        "image": "https://dh.aks.ac.kr/Edu/wiki/images/thumb/0/05/%EC%B2%AD%EB%8B%B4%EB%8F%99.jpg/600px-%EC%B2%AD%EB%8B%B4%EB%8F%99.jpg"
    },
    {
        "name": "연남",
        "coords": [37.5661, 126.9256],
        "description": "소규모 카페와 개성 있는 음식점이 많아, 개성을 중시하는 소비자들이 자주 찾는 곳",
        "image":"https://cdn.thescoop.co.kr/news/photo/201909/36658_48383_542.jpg"
    },
    {
        "name": "망원",
        "coords": [37.5569, 126.9023],
        "description": "감성적인 소규모 카페와 개성 있는 상점들이 많으며, '망리단길'로 불리는 거리에서 최신 트렌드를 엿볼 수 있음",
        "image":"https://love.seoul.go.kr/tmda/Pds/Board/seoul_news_write/202305_03_1200.jpg"
    },
    {
        "name": "을지로",
        "coords": [37.5660, 126.9910],
        "description": "오래된 공장과 작업장들이 많아 '힙지로'로 불리며, 빈티지 감성의 바와 카페들이 밀집해 있어 젊은층 사이에서 인기 상승 중",
        "image":"https://mblogthumb-phinf.pstatic.net/MjAyMTAzMTdfNTUg/MDAxNjE1OTM3NTYyNDA4.q9XslyF7jKUHI6QbbhHqbBqk19Ox3GNAQoT9hxbqOkAg.fRlvymC8y7o-4LgTKKPUHR4zymM4da2dnHPtRveiD8Mg.JPEG.ichufs/DSC_3894.jpg?type=w800"
    },
    {
        "name": "성내",
        "coords": [37.5276, 127.1251],
        "description": "송파구 내 주택가와 어우러진 조용하고 감성적인 상권으로, 인디 카페와 소규모 매장들이 많이 생겨나고 있음",
        "image":"https://www.ksponco.or.kr/olympicpark/img/sub/s1_01_pic02.jpg"
    },
    {
        "name": "문래",
        "coords": [37.5149, 126.8965],
        "description": "공장 지역과 예술가들의 작업실이 공존하는 독특한 분위기로, 예술과 창작 활동에 관심 있는 사람들이 자주 찾는 곳",
        "image":"https://www.ydp.go.kr/site/tour/images/contents/cts5313_img.jpg"
    },
    {
        "name": "봉천",
        "coords": [37.4823, 126.9510],
        "description": "대학가 근처로 감성적인 소규모 상점과 음식점이 모여 있어 새로운 핫플레이스로 부상하고 있음",
        "image":"https://www.gwanak.go.kr/images/gwanak/m7/02.png"
    },
    {
        "name": "녹사평",
        "coords": [37.5345, 126.9868],
        "description": "이태원과 인접하지만 비교적 조용한 분위기를 갖춘 상권으로, 감각적인 카페와 식당들이 많아지면서 부상하고 있음",
        "image":"https://lh5.googleusercontent.com/proxy/Buu-eeOXRA7UH3z3Wqjqh6gCuAoGYlUYxfv6BsDfHcoyOQIUNandvVSQHwh0KMSIp6MvAusHrQCjaDmdRBT2ZveEGzkz7mQwL7wTWORNUjDqnd3LrQRKgzoH29zb-tr6zddh8I-CJXo2W_hRVyr_Sxn7TEHo2AstxxFeAlV8P4WdNpo"
    },
    {
        "name": "도곡",
        "coords": [37.4908, 127.0535],
        "description": "고급 주거 지역이지만 최근 작은 독립 서점과 트렌디한 카페들이 생겨나면서 새로운 상권으로 성장 중",
        "image":"https://img0.yna.co.kr/photo/cms/2017/03/24/01/C0A8CA3D0000015AFF24D58F000D4854_P2.jpeg"
    },
    {
        "name": "불광",
        "coords": [37.6105, 126.9307],
        "description": "은평구에 위치한 이 지역은 산과 가까워 자연 친화적인 공간이 많고, 힐링 카페와 소규모 상점이 늘어나고 있음",
        "image":"https://upload.wikimedia.org/wikipedia/commons/3/30/Eunpyeong_Hanok_Village_20200920_002.jpg"
    },
    {
        "name": "장위",
        "coords": [37.6103, 127.0516],
        "description": "성북구에 위치한 장위동은 재개발이 진행 중이며, 빈티지와 뉴트로 감성을 가진 상점들이 늘어나면서 부상 중인 상권",
        "image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjOL2F0im482RuKwAEWozZSIbTzo_Jp0qThQ&s"
    },
    {
        "name": "수색",
        "coords": [37.5817, 126.9012],
        "description": "은평구와 마포구 경계에 있는 수색 지역은 재개발과 함께 새로운 상권으로 형성되고 있으며, 복합 문화 공간과 트렌디한 매장들이 주목받고 있음",
        "image":"https://image.chosun.com/sitedata/image/202103/13/2021031301156_0.jpg"
    }
]

# 각 지역에 대한 마커 추가
for loc in locations:
    popup_html = f"""
    <div style="width:300px; display: flex;">
        <img src="{loc['image']}" width="100px" height="100px" style="margin-right:10px;">
        <div>
            <h4>{loc['name']}</h4>
            <p>{loc['description']}</p>
        </div>
    </div>
    """
    marker = folium.Marker(
        location=loc["coords"],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=loc["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    )
    marker.add_to(m)  # 마커를 지도에 추가

# 왼쪽에 지도 표시
with st.container():

    with st.expander("정보"):
        st.write(
            """목적과 지역을 선택해서 지역 분위기를 알아보세요.
            보고 계신 버전은 1차로 만든 버전입니다."""
            )
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
    
        # 제목과 나머지 버튼
        st.markdown(
            """
            <style>
            .title-and-buttons {
                display: flex;
                align-items: center;
                margin-top: 10px; /* '정보' 버튼과 제목 간격 */
                margin-bottom: 20px;
            }
            .title {
                font-size: 1.5em;
                font-weight: bold;
                margin-right: 10px;
            }
            .small-button {
                font-size: 12px;
                padding: 4px 8px;
                margin-right: 8px;
                text-decoration: none;
                color: #333;
                background-color: #f0f0f0;
                border-radius: 5px;
                display: inline-block;
            }
            .small-button:hover {
                background-color: #e0e0e0;
            }
            </style>
            <div class="title-and-buttons">
                <span class="title">서울 분위기 지도</span>
                <a href="https://forms.gle/di1BSZWZ4xZAzDJC8" target="_blank" class="small-button">만족도 조사</a>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 지도 표시
        # st_folium(m, width=960, height=600)
        #st_folium(m, width=map_width, height=map_height)
        if st.session_state.is_mobile:
        # 모바일 레이아웃 (세로 배치)
            st.write("서울 분위기 지도")  
            st_folium(m, width=350, height=400)  # 모바일에서는 폭을 줄여 표시
        else :
            st_folium(m, width=960, height=600)
            
        # Session State 초기화
        if "last_saved_region" not in st.session_state:
            st.session_state["last_saved_region"] = None
        if "show_thank_you" not in st.session_state:
            st.session_state["show_thank_you"] = False
        if "input_text" not in st.session_state:
            st.session_state["input_text"] = ""  # 입력 필드 초기값을 빈 문자열로 설정



        # "지역 추가하기" 입력 필드
        st.text_input(
            '지역 추가하기', 
            value=st.session_state["input_text"], 
            placeholder="추가하고 싶은 지역을 적고 엔터를 눌러주세요. 예시) 샤로수길, 흑석동",
            label_visibility = 'collapsed',
            key="input_text",  # 세션 상태에서 관리되는 입력 필드 값
            on_change=save_input  # 입력이 완료되면 save_input 호출
        )

        # "의견 감사합니다" 메시지 표시 (show_thank_you가 True일 때만)
        if st.session_state["show_thank_you"]:
            st.success(f"'{st.session_state['last_saved_region']}'이(가) 입력되었습니다. 의견 감사합니다.")
        


    with col2:
        st.write("### 지역 분위기 분석")

        # 지역 선택 UI
        places = ["명동", "홍대", "강남역", "이태원", "성수", "신촌", "여의도", "북촌", "청담", "연남동", 
                  "망원동", "을지로", "성내동", "문래동", "봉천동", "녹사평", "도곡동", "불광동", "장위동", "수색동"]
        purposes = ["약속", "여행", "거주"]
        
        select_purpose = st.selectbox("목적을 선택하세요:", purposes)
        # 목적 선택 구글 애널리틱스 코드
        st.markdown(f"<script>trackEvent('Purpose_Select', 'Dropdown', '{select_purpose}');</script>", unsafe_allow_html=True)
        select_place = st.selectbox("지역을 선택하세요:", places)
        # 지역 선택 구글 애널리틱스 코드
        st.markdown(f"<script>trackEvent('Place_Select', 'Dropdown', '{select_place}');</script>", unsafe_allow_html=True)
        w2v_r = place_result[place_result['search_term'] == select_place]['word2vec_result'].iloc[0]
        
        # session_state에 'gpt_response' 키가 없으면 초기화
        if 'gpt_response' not in st.session_state:
            st.session_state.gpt_response = None
            
        # 버튼 클릭 시 OpenAI API 호출
        if st.button("분석", type="primary", use_container_width=True):
            st.markdown(f"<script>trackEvent('Analyze_Button_Click', 'Button', 'Purpose: {select_purpose}, Place: {select_place}');</script>", unsafe_allow_html=True)
            with st.spinner("분석중입니다..."):
                try:
                    # OpenAI의 새로운 ChatCompletion API 호출
                    response = openai.ChatCompletion.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": f"{w2v_r} 이건 {select_place}이라는 단어와 연관있는 단어와 중요도를 표시한 거야. 이 단어들로 {select_place}의 분위기를 {select_place}에 {select_purpose}하려는 사람에게 말해주는 거처럼 지역의 분위기를 유추해줘. 분위기는 3개로 유추해주고 어떤 단어들로 유추했는지랑 설명도 해주고 마지막으로 유추한 분위기를 토대로 {select_purpose}에 적합한 곳인지 10점 만점에 몇 점인지 정량적 평가 해줘. 그리고 평가한 이유도 설명해줘. 반드시 예의바르게 말을 해야 해."}
                        ]
                    )

                    # 응답 저장
                    st.session_state.gpt_response = response['choices'][0]['message']['content'].strip()
                    
                    # 선택한 목적과 지역을 텍스트 파일에 저장
                    with open("목적이랑 지역 쌍으로 저장하기.txt", "a") as file:
                        file.write(f"{select_purpose} & {select_place}\n")

                
                except Exception as e:
                    # 오류 메시지 출력
                    st.write("OpenAI API 연결에 실패했습니다.")
                    st.write("에러 메시지:", e)
                
        # 분석 결과가 존재할 때 화면에 출력
        if st.session_state.gpt_response:
            st.subheader("분석 결과")
            st.write(st.session_state.gpt_response)
            
        