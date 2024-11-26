import streamlit as st

# HTML과 JavaScript 코드
def generate_kakao_map_html(lat, lng):
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Kakao Map</title>
        <script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=cf3a0088cdd7e5a988917a5d9d8f16c9"></script>
    </head>
    <body>
        <div id="map" style="width:100%;height:400px;"></div>
        <script>
            var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
                mapOption = {{
                    center: new kakao.maps.LatLng({lat}, {lng}), // 지도의 중심좌표
                    level: 3 // 지도의 확대 레벨
                }};
            var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

            // 마커를 생성합니다
            var marker = new kakao.maps.Marker({{
                position: new kakao.maps.LatLng({lat}, {lng}) // 마커가 표시될 위치
            }});
            marker.setMap(map); // 마커를 지도 위에 표시합니다
        </script>
    </body>
    </html>
    """
    return html_code

# Streamlit UI
st.title(":round_pushpin: Kakao Map Integration with Streamlit")
default_latitude = "37.5665"
default_longitude = "126.9780"

# HTML 지도 생성 및 표시 (항상 표시)
st.components.v1.html(generate_kakao_map_html(default_latitude, default_longitude), height=450)