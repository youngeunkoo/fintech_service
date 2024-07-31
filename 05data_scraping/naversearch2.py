import requests
import pandas as pd
import time
from dotenv import load_dotenv
import os 

# .env 파일에서 환경 변수 로드 
load_dotenv()

# 환경변수에 접근



def naver_search():
    '''이 함수는 네이버 검색하는 서비스를 requests로 구현한 것입니다.'''
    
    
    service = input('''검색 서비스 번호를 입력하세요: 
    1 블로그
    2 책
    3 뉴스
    4 전문자료 
    ''')
    query = input("검색어를 입력하세요: ")
     
    if service == '1':
        service = 'blog'
    elif service == '2':
        service = 'book'
    elif service == '3':
        service = 'news'
    elif service == '4':
        service = 'doc'
        
    book_lists = []
    page = 1
    start = 1
    
    while True:
    
        # 아이디랑 비번 노출시키지 않는 방법
        url =f"https://openapi.naver.com/v1/search/{service}.json"
        client_id = os.getenv('client_id') # 네이버 api에 접속 가능한 id
        client_secret = os.getenv('client_secret')     # 네이버 api에 접속 가능한 pw
        payload = {'query' : '핀테크', 'display' : 10, 'start' : 1, 'sort' : 'sim'}
        payload = dict(query = query ,display=10 ,start= start, sort = sort)
        headers = {'X-Naver-Client-Id' : client_id, 'X-Naver-Client-Secret' : client_secret}

       
            
        try: 
            r = requests.get(url, params = payload, headers = headers)
            
            print(r.url)
            
            if(r.status_code == 200):
                data = r.json() 
                print(type(data))
                book_lists.append(json.loads(response_body.decode('utf-8'))) 
                total_pages = data['total'] // 10 + 1

            else:
                print("Error Code:" + r.status_code)
                break
            
            

            if page < total_pages : 
                page += 1
                if start != 991:
                    start += 10
                elif start == 991:
                    start += 9
                print(f"{page:03d}/{total_pages} 추출중", end= "\r")

            else:
                break



            time.sleep(0.3)   
        except Exception as e:
            print(e)
            break