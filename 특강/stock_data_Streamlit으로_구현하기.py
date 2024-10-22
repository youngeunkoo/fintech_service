
# 세션 상태에서 ticker 값을 False로 초기화
st.session_state["ticker"] = False

# 제목을 표시
st.write("# 📈 Stock Market DashBoard")

##################################################################################################
import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime  # datetime 모듈을 추가


# 섹터별 ETF 티커와 한국어 이름 설정
sector_etfs = {
    '기술 (Technology)': 'XLK',
    '에너지 (Energy)': 'XLE',
    '헬스케어 (Healthcare)': 'XLV',
    '소재 (Materials)': 'XLB',
    '산업재 (Industrials)': 'XLI',
    '자유소비재 (Consumer Discretionary)': 'XLY',
    '필수소비재 (Consumer Staples)': 'XLP',
    '금융 (Financials)': 'XLF',
    '통신 (Communication Services)': 'XLC',
    '유틸리티 (Utilities)': 'XLU',
    '부동산 (Real Estate)': 'XLRE'
}

# Streamlit 대시보드 제목
st.title("섹터별 기간별 수익성 분석 및 종목 노출")

# 데이터 다운로드 기간 설정 (2019-01-01부터 2024-09-27까지)
start_date = '2019-01-01'
end_date = '2024-09-27'

# 섹터별 데이터 다운로드 (Adj Close)
@st.cache_data
def load_sector_data():
    return yf.download(list(sector_etfs.values()), start=start_date, end=end_date)['Adj Close']

# 데이터 로드
sector_data = load_sector_data()

# 기간별 수익률을 계산하는 함수 정의
def calculate_returns(data, periods):
    return data.iloc[-1] / data.iloc[-periods] - 1

# 각 기간에 해당하는 인덱스 계산 (거래일 기준)
one_month = 21  # 약 1개월
three_months = 63  # 약 3개월
six_months = 126  # 약 6개월
one_year = 252  # 1년
three_years = 252 * 3  # 3년
five_years = 252 * 5  # 5년
ytd = len(sector_data[sector_data.index.year == 2024])  # YTD (2024년의 일 수만큼)

# 전체 섹터에 대한 기간별 수익률 계산
all_returns_df = pd.DataFrame({
    '1M': [calculate_returns(sector_data[etf], one_month) for etf in sector_etfs.values()],
    '3M': [calculate_returns(sector_data[etf], three_months) for etf in sector_etfs.values()],
    '6M': [calculate_returns(sector_data[etf], six_months) for etf in sector_etfs.values()],
    '1Y': [calculate_returns(sector_data[etf], one_year) for etf in sector_etfs.values()],
    '3Y': [calculate_returns(sector_data[etf], three_years) for etf in sector_etfs.values()],
    '5Y': [calculate_returns(sector_data[etf], five_years) for etf in sector_etfs.values()],
    'YTD': [calculate_returns(sector_data[etf], ytd) for etf in sector_etfs.values()]
}, index=sector_etfs.keys())

# 그라데이션을 적용한 전체 섹터 수익률 테이블 생성
styled_all_returns_df = all_returns_df.style.format("{:.2%}").background_gradient(cmap='coolwarm', axis=0)

# 1. 섹터별 수익성 분석 (그라데이션 적용된 테이블 상단에 표시)
st.subheader("섹터별 수익성 분석 ")
st.dataframe(styled_all_returns_df)

# 2. 섹터 선택 버튼 표시 (버튼 형식으로 섹터 표시)
st.subheader("섹터를 선택하세요")

# 섹터 선택 영역 (버튼을 사용)
if "selected_sector" not in st.session_state:
    st.session_state.selected_sector = None

if "selected_sector_name" not in st.session_state:
    st.session_state.selected_sector_name = None

cols = st.columns(4)  # 4개씩 버튼을 한 줄에 배치
for i, (sector_name, etf) in enumerate(sector_etfs.items()):
    if cols[i % 4].button(sector_name):
        st.session_state.selected_sector = etf
        st.session_state.selected_sector_name = sector_name

# 파일 경로
#file_path = "C:/Users/sunmi/Desktop/holdings-daily_xlk.xlsx" # 파일 경로 변경 필요!!!!!!!!!!!!!
file_path = "C:/fintech_service/특강/holdings-daily_xlk.xlsx"

    
###############################################################################################
# 선택한 섹터가 "기술 (Technology)"인 경우 파일에서 데이터 불러오기
if st.session_state.selected_sector == 'XLK':  # 기술 섹터가 선택된 경우
    st.subheader(f"{st.session_state.selected_sector_name} 섹터의 종목 정보")

    # 파일에서 데이터 로드
    df = pd.read_excel(file_path)

    # 필요한 필드만 필터링 (Name, Ticker, Weight)
    filtered_df = df[['Name', 'Ticker', 'Weight']]

    # 테이블 형식으로 출력
    st.dataframe(filtered_df)


# 선택한 섹터가 "기술 (Technology)"인 경우 파일에서 데이터 불러오기
if '기술 (Technology)' in sector_etfs.keys():
    st.subheader(f"기술 (Technology) 섹터의 종목 정보")

    if os.path.exists(file_path):
        # 파일에서 데이터 로드
        df = pd.read_excel(file_path)
        filtered_df = df[['Name', 'Ticker', 'Weight']]

        # 테이블 형식으로 출력
        #st.dataframe(filtered_df)

        # Ticker 검색 위젯 추가
        selected_ticker = st.selectbox("주 Ticker를 선택하세요", filtered_df['Ticker'].unique())

        # 기본 날짜 설정
        default_start_date = datetime(2019, 1, 1)
        default_end_date = datetime(2024, 9, 27)

        # 사용자로부터 시작일과 종료일을 입력받는 위젯
        start_date = st.date_input("시작 날짜를 선택하세요", default_start_date)
        end_date = st.date_input("종료 날짜를 선택하세요", default_end_date)

        # 종료일이 시작일보다 이전인 경우 오류 메시지 출력
        if start_date > end_date:
            st.error("종료 날짜는 시작 날짜보다 이후여야 합니다.")
        else:
            # 선택한 티커의 데이터 다운로드 (Adj Close)
            @st.cache_data
            def load_ticker_data(ticker, start, end):
                data = yf.download(ticker, start=start, end=end)['Adj Close']
                return data

            # 데이터 로드
            ticker_data = load_ticker_data(selected_ticker, start_date, end_date)

            if not ticker_data.empty:
                # 선택한 티커 주가 데이터를 기준으로 시작일을 100으로 설정한 수익률 계산
                ticker_returns = (ticker_data / ticker_data.iloc[0]) * 100

                # 동종업계 비교 섹션
                st.subheader("동종업계 기업 비교")

                # 다중 선택 위젯: 여러 티커를 선택할 수 있도록 구성
                selected_comparisons = st.multiselect("동종업계 Ticker를 선택하세요", filtered_df['Ticker'].unique())

                if selected_comparisons:
                    # 선택한 동종업계 티커들의 데이터 로드
                    @st.cache_data
                    def load_comparison_data(tickers, start, end):
                        return yf.download(tickers, start=start, end=end)['Adj Close']

                    comparison_data = load_comparison_data(selected_comparisons, start_date, end_date)

                    # 데이터가 여러 티커인 경우 처리
                    if isinstance(comparison_data, pd.DataFrame):
                        # 여러 티커의 수익률 계산
                        comparison_returns = (comparison_data / comparison_data.iloc[0]) * 100
                    else:
                        # 단일 티커인 경우 처리
                        comparison_returns = (comparison_data / comparison_data.iloc[0]) * 100
                        comparison_returns = comparison_returns.to_frame(name=selected_comparisons[0])

                    # 선택한 티커의 데이터와 동종업계 데이터 합치기
                    combined_returns = pd.concat([ticker_returns.to_frame(name=selected_ticker), comparison_returns], axis=1)

                    # 모든 선택한 티커와 동종업계 티커들에 대한 수익률 그래프 그리기
                    plt.figure(figsize=(10, 6))
                    for ticker in combined_returns.columns:
                        plt.plot(combined_returns.index, combined_returns[ticker], label=f'{ticker}: {combined_returns[ticker].iloc[-1]:.2f}%')

                    plt.xlabel('기간')
                    plt.ylabel('수익률 (기준=100)')
                    plt.title(f'{selected_ticker} 및 동종업계 주가 변동 ({start_date} ~ {end_date})')
                    plt.grid(True)
                    plt.legend()

                    # 그래프 출력
                    st.pyplot(plt)
                else:
                    # 선택된 동종업계 티커가 없을 때 주 티커만 그래프 출력
                    plt.figure(figsize=(10, 6))
                    plt.plot(ticker_returns.index, ticker_returns.values, label=f'{selected_ticker}: {ticker_returns.iloc[-1]:.2f}%', color='blue')
                    plt.xlabel('기간')
                    plt.ylabel('수익률 (기준=100)')
                    plt.title(f'{selected_ticker} 주가 변동 ({start_date} ~ {end_date})')
                    plt.grid(True)
                    plt.legend()

                    # 그래프 출력
                    st.pyplot(plt)

                # **엔비디아(NVDA)** 선택 시 회사 개요 및 투자 포인트 추가
                if selected_ticker == "NVDA":
                    st.subheader("엔비디아 (NVIDIA) 회사 개요 및 투자 포인트")

                    # 회사 개요
                    st.markdown("""
                        **엔비디아(NVIDIA)**는 그래픽 처리 장치(GPU) 시장에서 선도적인 위치를 차지하고 있는 세계적인 반도체 회사입니다. 
                        엔비디아는 AI, 데이터 센터, 자율주행, 클라우드 컴퓨팅 등 다양한 기술 분야에서 영향력을 발휘하며, 
                        특히 인공지능(AI)과 고성능 컴퓨팅(HPC) 분야에서 핵심적인 역할을 하고 있습니다.
                    """)

                    st.markdown("""
                    ### 회사 개요:
                    - **설립연도**: 1993년
                    - **본사 위치**: 미국 캘리포니아주 산타클라라
                    - **주요 제품**: 그래픽 처리 장치(GPU), 인공지능(AI) 컴퓨팅 플랫폼, 자율주행 시스템, 데이터센터용 칩 등
                    - **주요 시장**: 게임, 데이터센터, AI 및 머신러닝, 자율주행차, 클라우드 컴퓨팅
                    - **시장 점유율**: 엔비디아는 게임, 그래픽 및 AI 기술을 위한 GPU 시장에서 압도적인 점유율을 차지하며, 데이터 센터 및 클라우드 AI 솔루션에서도 중요한 파트너로 자리매김하고 있습니다.
                    """)

                    # 투자 포인트
                    st.markdown("""
                    ### 투자 포인트:
                    1. **AI와 데이터센터의 성장**: 엔비디아는 GPU 기술을 바탕으로 AI 및 머신러닝 연산에서 필수적인 인프라를 제공합니다. 최근 AI 기반 연산 수요가 폭증함에 따라 데이터센터와 클라우드 기반 솔루션의 수요도 증가하고 있습니다.
                    2. **Gaming 및 Esports 시장의 확대**: 전 세계 게이밍 시장에서 큰 비중을 차지하고 있으며, 특히 게이밍용 GPU는 고성능 그래픽 처리와 실시간 렌더링에 필수적입니다.
                    3. **자율주행차 및 로보틱스**: 엔비디아의 드라이브(Drive) 플랫폼은 자율주행차에 필요한 AI 기술을 제공하는 핵심 솔루션입니다.
                    4. **메타버스 및 AR/VR 확장**: 메타버스와 증강현실(AR), 가상현실(VR)의 성장이 기대되면서, 엔비디아의 GPU는 이러한 가상 세계에서의 컴퓨팅 성능을 제공하는 핵심 하드웨어로 자리 잡고 있습니다.
                    5. **재무 건전성**: 강력한 재무구조와 현금흐름을 보유하고 있으며, 지속적인 기술 혁신을                     5. **재무 건전성**: 엔비디아는 강력한 재무구조와 현금흐름을 보유하고 있으며, 
                       지속적인 기술 혁신을 위한 연구개발(R&D)에 막대한 투자를 하고 있습니다. 
                       높은 마진율과 강력한 성장세를 유지하고 있어 투자자들에게 안정적인 수익을 제공할 가능성이 큽니다.
                    """)

            else:
                st.warning(f"{selected_ticker}에 대한 데이터를 불러올 수 없습니다. 다른 티커를 선택해 주세요.")
    else:
        st.error(f"파일을 찾을 수 없습니다: {file_path}")

    
