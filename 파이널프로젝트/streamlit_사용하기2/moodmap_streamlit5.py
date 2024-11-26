import streamlit as st


# HTML과 JavaScript 코드
def generate_kakao_map_html(locations, selected_location):
    # 선택된 지역의 중심 좌표
    center_lat, center_lng = locations[selected_location]["coords"]

    # HTML 생성
    data = locations[selected_location]
    lat, lng = data["coords"]
    title = selected_location

    # 마커 생성 및 인포윈도우 추가
    marker_js = f"""
        var marker = new kakao.maps.Marker({{
            position: new kakao.maps.LatLng({lat}, {lng}),
            map: map,
            title: "{title}"
        }});

        // 인포윈도우 내용
        var iwContent = '<div style="padding:5px;">{title}</div>';
        var infowindow = new kakao.maps.InfoWindow({{
            content: iwContent,
            removable: true
        }});

        // 마커에 클릭 이벤트를 등록하여 인포윈도우를 표시
        kakao.maps.event.addListener(marker, 'click', function() {{
            infowindow.open(map, marker);
        }});
    """

    # 폴리곤 생성
    polygon_coords = ", ".join(
        [f"new kakao.maps.LatLng({lat}, {lng})" for lat, lng in data["polygon"]]
    )
    polygon_js = f"""
        var polygonPath = [{polygon_coords}];
        var polygon = new kakao.maps.Polygon({{
            path: polygonPath,
            strokeWeight: 2,
            strokeColor: '#004c80',
            strokeOpacity: 0.8,
            fillColor: '#00a9ff',
            fillOpacity: 0.5
        }});
        polygon.setMap(map);
    """

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Kakao Map</title>
        <script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=cf3a0088cdd7e5a988917a5d9d8f16c9"></script>
    </head>
    <body>
        <div id="map" style="width:100%;height:600px;"></div>
        <script>
            var mapContainer = document.getElementById('map'),
                mapOption = {{
                    center: new kakao.maps.LatLng({center_lat}, {center_lng}),
                    level: 4
                }};
            var map = new kakao.maps.Map(mapContainer, mapOption);

            {marker_js}
            {polygon_js}
        </script>
    </body>
    </html>
    """
    return html_code



# 지역별 데이터
locations = {
    "망원": {
        "coords": [37.5569, 126.9023],
        "polygon": [
            [37.5595, 126.8979], [37.5590, 126.9080], [37.5545, 126.9085], [37.5540, 126.8975], [37.5595, 126.8979]
        ],
        "keywords": ["한적", "트렌디한 카페", "힙한 거리"],
        "description": "망원동은 다양한 개성 있는 카페와 상점들이 모여 있어 젊은 층에게 사랑받는 지역입니다.",
        "image": "image_망원.png"
    },
    "연남": {
        "coords": [37.5661, 126.9256],
        "polygon": [
            [37.5681, 126.9206], [37.5631, 126.9306], [37.5611, 126.9286], [37.5641, 126.9196], [37.5681, 126.9206]
        ],
        "keywords": ["소박함", "힐링", "자연"],
        "description": "연남동은 조용한 분위기와 공원 인근의 여유로운 공간으로 유명합니다.",
        "image": "image_연남.png"
    },
    "연희": {
        "coords": [37.5688, 126.9276],
        "polygon": [
            [37.5718, 126.9226], [37.5668, 126.9326], [37.5648, 126.9296], [37.5678, 126.9206], [37.5718, 126.9226]
        ],
        "keywords": ["한적함", "고급스러운 분위기", "조용한 거리"],
        "description": "연희동은 고급스러운 주거 지역과 함께 조용한 분위기로 알려져 있습니다.",
        "image": "image1_연희.png"
    },
    "합정": {
        "coords": [37.5495, 126.9137],
        "polygon": [
            [37.5525, 126.9087], [37.5465, 126.9187], [37.5445, 126.9147], [37.5485, 126.9067], [37.5525, 126.9087]
        ],
        "keywords": ["트렌디함", "문화", "젊은 분위기"],
        "description": "합정은 다양한 문화 공간과 젊은 세대가 즐길 수 있는 트렌디한 상점들이 많습니다.",
        "image": "image1_합정.png"
    },
    "홍대": {
        "coords": [37.5563, 126.9220],
        "polygon": [
            [37.5593, 126.9170], [37.5533, 126.9270], [37.5513, 126.9230], [37.5553, 126.9150], [37.5593, 126.9170]
        ],
        "keywords": ["예술적", "활기찬", "다양한 문화"],
        "description": "홍대는 젊은이들의 문화가 살아 숨 쉬는 예술적인 거리입니다.",
        "image": "image1_홍대.png"
    },
    "상수": {
        "coords": [37.5476, 126.9227],
        "polygon": [
            [37.5506, 126.9177], [37.5446, 126.9277], [37.5426, 126.9227], [37.5466, 126.9147], [37.5506, 126.9177]
        ],
        "keywords": ["세련됨", "힙한 공간", "작은 갤러리"],
        "description": "상수동은 세련된 분위기와 독특한 갤러리, 카페들로 유명합니다.",
        "image": "image1_상수.png"
    },
    "신촌": {
        "coords": [37.5585, 126.9394],
        "polygon": [
            [37.5615, 126.9344], [37.5555, 126.9444], [37.5535, 126.9404], [37.5575, 126.9324], [37.5615, 126.9344]
        ],
        "keywords": ["대학가", "활기찬", "청년 문화"],
        "description": "신촌은 대학가 특유의 활기찬 분위기와 다양한 청년 문화가 살아 있는 지역입니다.",
        "image": "image1_신촌.png"
    },
    "이대": {
        "coords": [37.5599, 126.9457],
        "polygon": [
            [37.5629, 126.9407], [37.5569, 126.9507], [37.5549, 126.9467], [37.5589, 126.9387], [37.5629, 126.9407]
        ],
        "keywords": ["여성적", "패션", "세련됨"],
        "description": "이대는 패션과 여성적인 분위기가 강조된 세련된 공간입니다.",
        "image": "image1_이대.png"
    }
}


# Streamlit 설정
st.set_page_config(layout="wide")

# 선택된 지역
selected_location = st.selectbox("지역을 선택하세요", list(locations.keys()))

# 컬럼 레이아웃 설정
col1, col2 = st.columns([3, 2])

with col1:
    # 카카오 지도 표시
    st.components.v1.html(generate_kakao_map_html(locations, selected_location), height=600)

with col2:
    # 오른쪽 정보 표시
    st.title(f":round_pushpin: {selected_location}")

    # 분위기 키워드
    st.markdown("### 분위기 키워드")
    keywords = locations[selected_location]["keywords"]
    st.markdown(
        f"""
        <style>
        .keyword {{
            background-color: #7B68EE;
            color: white;
            padding: 8px 15px;
            border-radius: 15px;
            font-weight: bold;
            display: inline-block;
            margin-right: 10px;
        }}
        .keyword2 {{
            background-color: #FF6347;
            color: white;
            padding: 8px 15px;
            border-radius: 15px;
            font-weight: bold;
            display: inline-block;
            margin-right: 10px;
        }}
        .keyword3 {{
            background-color: #FFA500;
            color: white;
            padding: 8px 15px;
            border-radius: 15px;
            font-weight: bold;
            display: inline-block;
            margin-right: 10px;
        }}
        </style>
        <div>
            <span class="keyword">#{keywords[0]}</span>
            <span class="keyword2">#{keywords[1]}</span>
            <span class="keyword3">#{keywords[2]}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<br><br>", unsafe_allow_html=True)  # 두 줄 간격

    # 설명 출력
    st.markdown("### 분위기 설명")
    st.write(locations[selected_location]["description"])

    st.markdown("<br><br>", unsafe_allow_html=True)  # 두 줄 간격
    # 이미지 출력
    st.markdown("### 이미지 보기")
    st.image(locations[selected_location]["image"], caption=f"{selected_location} 이미지", use_column_width=True)
