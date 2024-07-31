import os
import sys
import urllib.request
import json
import pandas as pd
import time




def naver_search():
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

        client_id = "k5K8PLgTE8lcRewiN6sA"    # 네이버 api에 접속 가능한 id
        client_secret = "0i0fiO7U_D"          # 네이버 api에 접속 가능한 pw

        encText = urllib.parse.quote(query)   # 여기 안에 단어를 바꿀 때

    #     print(encText)
        url = f"https://openapi.naver.com/v1/search/{service}.json?query={encText}&display=10&start={start}" # JSON 결과
    #     print("url: " , url, end= "\r")
        try: 
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()

            if(rescode==200):
                response_body = response.read()
                data = json.loads(response_body.decode('utf-8'))
                book_lists.append(json.loads(response_body.decode('utf-8'))) # book_lists 리스트에 넣기
                total_pages = data['total'] // 10 + 1

            else:
                print("Error Code:" + rescode)
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



            time.sleep(0.3)  # 0.3 초 단위로 결과값을 출력함. 
        except Exception as e:
            print(e)
            break




    result = pd.DataFrame()

    for book_list in book_lists[:]: 
        temp = pd.json_normalize(book_list['items'])
        result = pd.concat([result, temp])

    result
    result.to_csv(f"naver_{service}_api_fintech_{query}_result.csv", encoding = "utf-8") # 안될때는 'utf-8' 로 변경해서 저장?

naver_search()