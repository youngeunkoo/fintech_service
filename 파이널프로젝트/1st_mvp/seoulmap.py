import folium
import requests
import json
from folium.plugins import MarkerCluster
from folium.features import DivIcon
import streamlit as st
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(layout="wide")  # 화면 전체 너비 사용

# 서울 행정구역 json raw파일(githubcontent)
r = requests.get('https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json')

c = r.content
seoul_geo = json.loads(c)
                              # 각 구마다 어떻게 구성이 되어있는지 json형태로 확인가능,
#seoul_geo                    # 일단 너무 길어서 주석처리함

# 지도 초기화: 서울 중심으로 설정
m = folium.Map(location=[37.5665, 126.9780], tiles="Cartodb Positron", zoom_start=12)
folium.GeoJson(seoul_geo, name='지역구').add_to(m)

# 서울 구별 중심 좌표와 구 이름
districts = {
    "종로구": [37.5735, 126.9792],
    "중구": [37.5641, 126.9979],
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
    
# 그룹별 색상 설정
group_colors = {
    "유명 지역": "blue",
    "뜨는 지역": "green"
}

# 그룹 생성
famous_group = folium.FeatureGroup(name="유명 지역")
emerging_group = folium.FeatureGroup(name="뜨는 지역")

# 위치 정보
locations = [
    # 유명 지역 10곳
    {
        "name": "명동",
        "coords": [37.5636, 126.9869],
        "description": "대형 브랜드 매장과 화장품, 패션 아이템이 밀집해 있으며, 한류와 관광이 결합된 상권",
        "image": "https://cdn.thescoop.co.kr/news/photo/202305/57665_89482_111.jpg",
        "group": "유명 지역"
    },
    {
        "name": "홍대",
        "coords": [37.5563, 126.9220],
        "description": "독립적인 상점과 카페, 스트리트 아트, 클럽과 공연장 등 다양한 문화 콘텐츠가 있는 지역",
        "image":"https://i.namu.wiki/i/6v8oGwuvwQTt85VnupCSsfQ1S2oXX24eAgts7d9M-8EGfR5-lXRj8bIScJbvzNGCmNC0YcSCzz1cmJudjIcGaW19oAmPfd8UA-smwkEfJK0IvGSfUidx3LsVdf9gLHJAQ-xSdUukYS7teB7XN_x_zQ.webp",
        "group": "유명 지역"
    },
    {
        "name": "강남역",
        "coords": [37.4979, 127.0276],
        "description": "회사와 사무실 밀집, 고급 브랜드, 다양한 음식점과 쇼핑 시설이 모여 있는 지역",
        "image":"https://i.namu.wiki/i/KJmURamoD2t16saSVzLomUJOQ1hNjOicO06lwQIwdB5gHhgMF8uyRp9aCjkVJ9h01RLdn2Y8Q1tPykUumTiKDQ.webp",
        "group": "유명 지역"
    },
    {
        "name": "이태원",
        "coords": [37.5340, 126.9948],
        "description": "다국적 레스토랑과 바, 외국인이 많이 찾는 문화 중심지로 다양한 글로벌 문화를 경험할 수 있는 장소",
        "image": "https://minio.nculture.org/amsweb-opt/multimedia_assets/165/85860/94092/c/%EC%9D%B4%ED%83%9C%EC%9B%90%EA%B1%B0%EB%A6%AC-%288%29_rev-medium-size.jpg",
        "group": "유명 지역"
    },
    {
        "name": "신촌",
        "coords": [37.5585, 126.9394],
        "description": "대학가 특유의 분위기로 인해 저렴하고 접근성이 좋은 카페와 음식점, 청년층을 겨냥한 상업시설이 많은 지역",
        "image":"https://www.sdm.go.kr/lib/culture/images/contents/sub2000/img_sub2050_1.png",
        "group": "유명 지역"
    },
    {
        "name": "여의도",
        "coords": [37.5219, 126.9245],
        "description": "비즈니스 중심지이자 한강공원이 있는 지역",
        "image": "https://i.namu.wiki/i/TcpbZAY5CetJ-RIQknixiIikj0t5WGF_c6nNiWEJxgbZJUbtbgY-RL3UxYndV6EsGHS9bKjRZigFhFk1ndglBA.webp",
        "group": "유명 지역"
    },
    {
        "name": "삼청동 & 북촌",
        "coords": [37.5843, 126.9830],
        "description": "한옥과 현대적 갤러리가 어우러져 있어 관광객과 문화 애호가가 선호하는 지역",
        "image":"https://korean.visitseoul.net/data/kukudocs/seoul2133/20220518/202205181617250471.jpg",
        "group": "유명 지역"
    },
    {
        "name": "성수동",
        "coords": [37.5447, 127.0558],
        "description": "창의적이고 개성 있는 카페와 독립 상점이 많아 MZ 세대가 많이 찾는 지역",
        "image": "https://blog.igisam.com/app/uploads/2023/01/%EA%B7%B8%EB%A6%BC2-2-1024x682.jpg",
        "group": "유명 지역"
    },
    {
        "name": "청담동",
        "coords": [37.5197, 127.0474],
        "description": "명품 매장과 고급 레스토랑이 있어 패션과 럭셔리를 중시하는 소비자들이 찾는 지역",
        "image": "https://dh.aks.ac.kr/Edu/wiki/images/thumb/0/05/%EC%B2%AD%EB%8B%B4%EB%8F%99.jpg/600px-%EC%B2%AD%EB%8B%B4%EB%8F%99.jpg",
        "group": "유명 지역"
    },
    {
        "name": "연남동",
        "coords": [37.5661, 126.9256],
        "description": "소규모 카페와 개성 있는 음식점이 많아, 개성을 중시하는 소비자들이 자주 찾는 곳",
        "image":"https://cdn.thescoop.co.kr/news/photo/201909/36658_48383_542.jpg",
        "group": "유명 지역"
    },

    # 뜨는 지역 10곳
    {
        "name": "망원동",
        "coords": [37.5569, 126.9023],
        "description": "감성적인 소규모 카페와 개성 있는 상점들이 많으며, '망리단길'로 불리는 거리에서 최신 트렌드를 엿볼 수 있음",
        "image":"https://love.seoul.go.kr/tmda/Pds/Board/seoul_news_write/202305_03_1200.jpg",
        "group": "뜨는 지역"
    },
    {
        "name": "을지로",
        "coords": [37.5660, 126.9910],
        "description": "오래된 공장과 작업장들이 많아 '힙지로'로 불리며, 빈티지 감성의 바와 카페들이 밀집해 있어 젊은층 사이에서 인기 상승 중",
        "image":"https://mblogthumb-phinf.pstatic.net/MjAyMTAzMTdfNTUg/MDAxNjE1OTM3NTYyNDA4.q9XslyF7jKUHI6QbbhHqbBqk19Ox3GNAQoT9hxbqOkAg.fRlvymC8y7o-4LgTKKPUHR4zymM4da2dnHPtRveiD8Mg.JPEG.ichufs/DSC_3894.jpg?type=w800",
        "group": "뜨는 지역"
    },
    {
        "name": "성내동",
        "coords": [37.5276, 127.1251],
        "description": "송파구 내 주택가와 어우러진 조용하고 감성적인 상권으로, 인디 카페와 소규모 매장들이 많이 생겨나고 있음",
        "image":"https://www.ksponco.or.kr/olympicpark/img/sub/s1_01_pic02.jpg",
        "group": "뜨는 지역"
    },
    {
        "name": "문래동",
        "coords": [37.5149, 126.8965],
        "description": "공장 지역과 예술가들의 작업실이 공존하는 독특한 분위기로, 예술과 창작 활동에 관심 있는 사람들이 자주 찾는 곳",
        "image":"https://www.ydp.go.kr/site/tour/images/contents/cts5313_img.jpg",
        "group": "뜨는 지역"
    },
    {
        "name": "봉천동",
        "coords": [37.4823, 126.9510],
        "description": "대학가 근처로 감성적인 소규모 상점과 음식점이 모여 있어 새로운 핫플레이스로 부상하고 있음",
        "image":"https://www.gwanak.go.kr/images/gwanak/m7/02.png",
        "group": "뜨는 지역"
    },
    {
        "name": "녹사평",
        "coords": [37.5345, 126.9868],
        "description": "이태원과 인접하지만 비교적 조용한 분위기를 갖춘 상권으로, 감각적인 카페와 식당들이 많아지면서 부상하고 있음",
        "image":"https://lh5.googleusercontent.com/proxy/Buu-eeOXRA7UH3z3Wqjqh6gCuAoGYlUYxfv6BsDfHcoyOQIUNandvVSQHwh0KMSIp6MvAusHrQCjaDmdRBT2ZveEGzkz7mQwL7wTWORNUjDqnd3LrQRKgzoH29zb-tr6zddh8I-CJXo2W_hRVyr_Sxn7TEHo2AstxxFeAlV8P4WdNpo",
        "group": "뜨는 지역"
    },
    {
        "name": "도곡동",
        "coords": [37.4908, 127.0535],
        "description": "고급 주거 지역이지만 최근 작은 독립 서점과 트렌디한 카페들이 생겨나면서 새로운 상권으로 성장 중",
        "image":"https://img0.yna.co.kr/photo/cms/2017/03/24/01/C0A8CA3D0000015AFF24D58F000D4854_P2.jpeg",
        "group": "뜨는 지역"
    },
    {
        "name": "불광동",
        "coords": [37.6105, 126.9307],
        "description": "은평구에 위치한 이 지역은 산과 가까워 자연 친화적인 공간이 많고, 힐링 카페와 소규모 상점이 늘어나고 있음",
        "image":"https://upload.wikimedia.org/wikipedia/commons/3/30/Eunpyeong_Hanok_Village_20200920_002.jpg",
        "group": "뜨는 지역"
    },
    {
        "name": "장위동",
        "coords": [37.6103, 127.0516],
        "description": "성북구에 위치한 장위동은 재개발이 진행 중이며, 빈티지와 뉴트로 감성을 가진 상점들이 늘어나면서 부상 중인 상권",
        "image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjOL2F0im482RuKwAEWozZSIbTzo_Jp0qThQ&s",
        "group": "뜨는 지역"
    },
    {
        "name": "수색동",
        "coords": [37.5817, 126.9012],
        "description": "은평구와 마포구 경계에 있는 수색 지역은 재개발과 함께 새로운 상권으로 형성되고 있으며, 복합 문화 공간과 트렌디한 매장들이 주목받고 있음",
        "image":"https://image.chosun.com/sitedata/image/202103/13/2021031301156_0.jpg",
        "group": "뜨는 지역"
    }
]

# 각 위치에 마커 추가 (가로로 긴 팝업과 이미지 포함)
for loc in locations:
    # HTML 형식으로 팝업 내용 구성
    popup_html = f"""
    <div style="width:300px; display: flex;">
        <img src="{loc['image']}" width="100px" height="100px" style="margin-right:10px;">
        <div>
            <h4>{loc['name']}</h4>
            <p>{loc['description']}</p>
        </div>
    </div>
    """
    # 마커 생성 및 그룹 추가
    marker = folium.Marker(
        location=loc["coords"],
        popup=folium.Popup(popup_html, max_width=300),  # 팝업 최대 너비 설정
        tooltip=loc["name"],
        icon=folium.Icon(color=group_colors[loc["group"]], icon="info-sign")  # 그룹 색상을 사용하여 색상 설정
    )

    # 그룹에 따라 마커 추가
    if loc["group"] == "유명 지역":
        famous_group.add_child(marker)
    else:
        emerging_group.add_child(marker)

# 지도에 그룹 추가
m.add_child(famous_group)
m.add_child(emerging_group)

# LayerControl 추가 (그룹 토글을 위해 필요)
folium.LayerControl(collapsed=False).add_to(m)

# Streamlit에서 지도 표시
st.title("서울 분위기 지도")
st_folium(m, width=1080, height=720)