// 지도 초기화
var mapContainer = document.getElementById('map'), // 지도를 표시할 div
    mapOption = { 
        center: new kakao.maps.LatLng(37.5561, 126.9239), // 홍대입구 중심 좌표
        level: 5 // 확대 레벨
    };

var map = new kakao.maps.Map(mapContainer, mapOption);

// 지역 정보
const locations = {
    "망원": {
        "coords": [37.5569, 126.9023],
        "description": "한적하면서도 트렌디한 카페와 힙한 거리가 젊은 층에게 인기 있는 동네",
        "image": "./image_망원.png"
    },
    "연남": {
        "coords": [37.5661, 126.9256],
        "description": "소박한 분위기와 힐링이 가능한 자연 친화적인 공간이 특징인 지역",
        "image": "./image_연남.png"
    },
    "연희": {
        "coords": [37.5688, 126.9276],
        "description": "고급스러운 분위기와 한적함이 어우러진 조용한 주거 지역",
        "image": "https://via.placeholder.com/150"
    },
    "합정": {
        "coords": [37.5495, 126.9137],
        "description": "트렌디한 상점과 문화 공간이 가득한 젊고 활기찬 지역",
        "image": "https://via.placeholder.com/150"
    },
    "홍대": {
        "coords": [37.5563, 126.9220],
        "description": "다양한 문화와 예술적 감각이 살아 있는 활기찬 거리",
        "image": "https://via.placeholder.com/150"
    },
    "상수": {
        "coords": [37.5476, 126.9227],
        "description": "세련된 분위기의 작은 갤러리와 힙한 카페로 유명한 곳",
        "image": "https://via.placeholder.com/150"
    },
    "신촌": {
        "coords": [37.5585, 126.9394],
        "description": "대학가의 활기와 다양한 청년 문화가 공존하는 에너지가 넘치는 동네",
        "image": "https://via.placeholder.com/150"
    },
    "이대": {
        "coords": [37.5599, 126.9457],
        "description": "세련된 패션과 여성스러운 분위기가 돋보이는 패션 중심지",
        "image": "https://via.placeholder.com/150"
    }
};

// 각 지역에 마커와 인포윈도우 추가
for (let location in locations) {
    const data = locations[location];
    
    // 마커 생성
    const marker = new kakao.maps.Marker({
        position: new kakao.maps.LatLng(data.coords[0], data.coords[1]),
        map: map // 마커를 지도에 추가
    });
    
    // 인포윈도우 내용 설정
    const iwContent = `
        <div style="padding:10px; font-size:12px; text-align:center;">
            <strong>${location}</strong><br>
            <img src="${data.image}" alt="${location}" style="width:100px; height:80px; margin:5px 0;"><br>
            <p style="margin:0;">${data.description}</p>
        </div>`;
    
    const infowindow = new kakao.maps.InfoWindow({
        content: iwContent // HTML 문자열로 설정
    });

    // 마커에 마우스오버 이벤트 등록 (인포윈도우 열기)
    kakao.maps.event.addListener(marker, 'mouseover', () => {
        infowindow.open(map, marker);
    });

    // 마커에 마우스아웃 이벤트 등록 (인포윈도우 닫기)
    kakao.maps.event.addListener(marker, 'mouseout', () => {
        infowindow.close();
    });
}
