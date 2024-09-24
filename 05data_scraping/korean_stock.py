import time
from datetime import date
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from sqlalchemy import create_engine, text


today = date.today()
print(today, type(today))
today = str(today)
# print(today, type(today))



page = 1
page_size = 100
final_result_df = pd.DataFrame()
while True:
    url = "https://kind.krx.co.kr/corpgeneral/corpList.do"
    payload = dict(method='searchCorpList',pageIndex=page, currentPageSize=page_size,orderMode=3,orderStat='D',searchType=13, fiscalYearEnd='all', location='all')
    r = requests.get(url, params=payload)
    print(r.status_code, end="\r")
    soup = bs(r.text, 'lxml')
    total_items = int(soup.select_one(".info.type-00 > em").text.replace(",", ""))
    total_pages = total_items // page_size + 1
    print(f"{page}/{total_pages} 수집중", end="\r")
    keys = soup.select_one("table.list.type-00.tmt30")['summary'].split(", ")  
    result = {}
    for tr in soup.select('tr'):
        for idx, (key, td) in enumerate(zip(keys, tr.select('td'))):
            if idx == 0:
                kinds = [img['alt'].strip() for img in td.select('img')]   # 1번째 증권 종류, 회사이름
                kind = ", ".join(kinds)
                code = td.select_one('a')['onclick'].split("'")[1]+"0" # 종목코드 추출
                result.setdefault('증권종류', []).append(kind) # 증권종류 저장
                result.setdefault(key, []).append(td.text)   # 회사이름 저장
                result.setdefault('종목코드', []).append(code)
            elif idx == 6:
                home_link = td.select_one('a')['href'] if td.string == None else ""  # 6번째 링크 찾기
                result.setdefault(key, []).append(home_link)
            else:
                result.setdefault(key, []).append(td.text)
    result_df = pd.DataFrame(result)
    final_result_df = pd.concat([final_result_df, result_df])
        
    if page < total_pages:
        page += 1
        time.sleep(5)
    else:
        break

#display(final_result_df)
#final_result_df.to_csv(f"상장기업정보{today}_기준.csv", encoding='utf-8', index=False)  # 수집일 기준으로 csv 파일로 저장


# MySQL 서버에 연결 (데이터베이스를 지정하지 않고 접속)
db="mysql"
dbtype="pymysql"
id="root"
pw="1234"
host="127.0.0.1:3306"
database="korean_stock"


# SQLAlchemy 엔진 생성
engine = create_engine(f"{db}+{dbtype}://{id}:{pw}@{host}")
conn = engine.connect()

# 데이터베이스에 지정한 데이터베이스 이름 생성
conn.execute(text("CREATE DATABASE IF NOT EXISTS korean_stock"))

engine = create_engine(f"{db}+{dbtype}://{id}:{pw}@{host}/{database}")

# DataFrame을 MySQL 테이블로 저장

conn = engine.connect()
final_result_df.to_sql('company_info', con=conn, if_exists='replace', index=False)
conn.close()
