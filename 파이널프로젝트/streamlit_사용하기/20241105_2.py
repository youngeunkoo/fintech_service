# 필요한 라이브러리 임포트
import openai
import streamlit as st

# OpenAI API 키 설정
openai.api_key = "YOUR_OPENAI_API_KEY"  # 실제 API 키로 교체

# 분위기 설명을 가져오는 함수
def get_vibe_description(place_name):
    prompt = f"{place_name}의 분위기를 설명하는 텍스트를 작성해줘."
    response = openai.Completion.create(
        model="g-3W1Dr4kYz-jiyeog-bunwigi-alryeojuneun-jipiti",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Streamlit 인터페이스 설정
st.title("서울 분위기 설명 테스트")

# 지역 선택 드롭다운 메뉴
places = ["명동", "홍대", "강남역", "이태원", "신촌", "여의도", "북촌", "성수동", "청담동", "연남동"]
select_place = st.selectbox("지역을 선택하세요:", places)

# 분석 버튼
if st.button("분석"):
    with st.spinner("분석 중..."):
        vibe_description = get_vibe_description(select_place)
        st.subheader("분석 결과")
        st.write(f"**{select_place}의 분위기 유추:**")
        st.write(vibe_description)

