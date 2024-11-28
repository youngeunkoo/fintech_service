// 지도 초기화
var mapContainer = document.getElementById('map'),
    mapOption = { 
        center: new kakao.maps.LatLng(37.5561, 126.9239), // 홍대입구 중심 좌표
        level: 5 // 확대 레벨
    };

var map = new kakao.maps.Map(mapContainer, mapOption);

// 지역 정보
const locations = {
    "망원": {
        "coords": [37.5569, 126.9023],
        "description": "한적하면서도 트렌디한 카페와 힙한 거리가 젊은 층에게 인기 있는 동네.",
        "image": "./image_망원.png",
        "keywords": ["트렌디한 카페", "힙한 거리", "한적한 분위기"]
    },
    // 다른 지역 정보 추가 가능
};

// 마커 및 인포윈도우 생성
for (let location in locations) {
    const data = locations[location];
    
    // 마커 생성
    const marker = new kakao.maps.Marker({
        position: new kakao.maps.LatLng(data.coords[0], data.coords[1]),
        map: map
    });

    // 인포윈도우 내용 설정
    const iwContent = `
        <div style="padding:10px; font-size:12px; text-align:center;">
            <strong>${location}</strong><br>
            <img src="${data.image}" alt="${location}" style="width:100px; height:80px; margin:5px 0;"><br>
            <p style="margin:0;">${data.description}</p>
        </div>`;
    
    const infowindow = new kakao.maps.InfoWindow({
        content: iwContent
    });

    // 마커 클릭 이벤트 등록
    kakao.maps.event.addListener(marker, 'click', () => {
        // 인포윈도우 표시
        infowindow.open(map, marker);

        // 오른쪽 정보 창 업데이트
        showInfoPanel(location, data.keywords);
    });
}

// 오른쪽 정보 창 업데이트 함수
function showInfoPanel(location, keywords) {
    const infoPanel = document.getElementById('info-panel');
    const title = document.getElementById('location-title');
    const keywordsList = document.getElementById('keywords-list');

    // 정보 창 보이기
    infoPanel.classList.remove('hidden');

    // 제목 업데이트
    title.textContent = `${location} 관련 정보`;

    // 키워드 업데이트
    keywordsList.innerHTML = ""; // 기존 내용 제거
    keywords.forEach(keyword => {
        const li = document.createElement('li');
        li.textContent = keyword;
        keywordsList.appendChild(li);
    });
}
