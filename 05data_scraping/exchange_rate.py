# final

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from bs4 import BeautifulSoup as bs
from datetime import date
import time
import pandas as pd
import dbio
# 주피터에 뜨는 경고 warning 없애기 
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# visual studio 에서 파일들의 경로가 같은 곳에 있어야 호출이 가능하다. 
# 매우매우 중요! 




today = str(date.today())  # 당일 날짜 수집하기 
    
# 컬럼명 바꾸기 : 명칭 바꾸기 
cols = ('통화', '현찰_살때_환율', '현찰_살때_Spread', '현찰_팔때_환율', '현찰_팔때_Spread', '송금_보낼때', '송금_받을때', 'T/C_살때', '외화_수표_팔때', '매매기준율', '환가_료율', '미화_환산율', 'date')
sorted_cols = ('date','통화', '현찰_살때_환율', '현찰_살때_Spread', '현찰_팔때_환율', '현찰_팔때_Spread', '송금_보낼때', '송금_받을때', 'T/C_살때', '외화_수표_팔때', '매매기준율', '환가_료율', '미화_환산율')


# 크롬 옵션즈에 정보를 담아 사람인 것 처럼 만들기
options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ['enable-logging'])
# options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
# options.add_argument('lang=ko_KR')
options.add_argument("--headless")  # Headless 모드 : 웹브라우저 창이 뜨지 않는거
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


# 크롬 웹브라우저 드라이버 자동 다운로드
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = options)
driver.set_window_size(1920, 1080) # 웹브라우저 해상도 조절
driver.get("https://www.kebhana.com/cms/rate/index.do?contentUrl=/cms/rate/wpfxd651_01i.do#//HanaBank")

wait = WebDriverWait(driver, 10) # 웹 요소가 나타날 때까지 최대 10초 기다림
time.sleep(5)

# tmpInqStrDt : 날짜 입력하기 
# search_box = wait.until(EC.presence_of_element_located(By.CSS_SELECTOR, "#tmpInqStrDt"))  # Expected condition
search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tmpInqStrDt")))
search_box.clear()
search_box.send_keys(today+Keys.ENTER )
time.sleep(2)

# 조회버튼 누르기
search_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#HANA_CONTENTS_DIV > div.btnBoxCenter > a")))
search_button.click()
time.sleep(5)


#searchContentDiv > div.printdiv > table
# 환율 정보 테이블이 뜰 때까지 기다림 
exchange_rate_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#searchContentDiv > div.printdiv > table")))

page_html = driver.page_source
df = pd.read_html(page_html)
df = df[1]
df['date'] = today  # 날짜 column 추가
df.columns = cols # cols 에 정의한 컬럼명으로 변경하기
df = df[[*sorted_cols]]  # date 칼럼을 가장 앞으로 보내기 


# DB에 저장
# vs에서 함수를 넣은 모듈을 하나 만들었음
dbio.exi_to_db("exchange_rate", today, df)  
driver.close()
