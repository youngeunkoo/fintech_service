use practice_1;
# 2024-06-28
# str_to_date('문자열', 출력 포멧)
select str_to_date('28,06,24', '%d, %m, %Y'); 
select str_to_date('19:30:15', '%H:%i:%s');
select str_to_date('19:30:15', '%h:%i:%s'); #변환 작업에 실패 --> 19가 24시간 형태인데 %h는 12시간 형태이기 때문
select str_to_date('07:30:15', '%h:%i:%s'); #이렇게 하면 변환 가능


# sysdate() : 현재 날짜와 시각을 반환
# now()와 차이점 존재
select sysdate();

# 현재 날짜를 기준으로 현재 일이 속한 월의 마지막 날짜에
# 해당하는 요일을 구하는 쿼리 작성하기. 
# 현재 날짜 : 2024-06-28 
select now();
select last_day('2024-06-28');
select dayname(last_day(now()));

# ---------------------------------------------------------------------------------------------
# 형 변환 함수 : 형 변환 데이터 타입을 변환하는 함수 
# 파이썬에서 매우 중요 : 데이터 타입이 동적으로 변한다. C는 그러지 않음. 
# cast(값 as 변환할 데이터 타입) 
# char / signed / decimal / double / float / date / datetime 

select cast(10 as char);
select cast('-10' as signed);
select cast('10.1234' as decimal); #정수로 변환됨
select cast('10.1234' as decimal(6,4)); #총자릿수 6, 소수점 4
select cast('10.1234' as double); 
select cast('2024-06-28' as date);
select cast('2024-06-28' as datetime);

# cast(값 as 변환할 데이터 타입) 
# convert(값, 변환할 데이터 타입)
# 똑같은 역할을 하는데 함수만 다를 뿐임 

# practice 
# 1.출력 컬럼 이름을 concat으로 합쳐서 출력하기 
use world;
# world의  country 테이블에서 인구가 4500만명 ~ 5500만명 사이에 있는 국가 조회
# code, name, continent, region, population 출력
# name (continent) 넣어서 출력하기

use world;
select * from country where population between 45000000 and 55000000 order by Population DESC;

select Code, Name, Continent, Region, Population from country 
where population between 45000000 and 55000000 order by Population DESC;

select Code, concat(Name, '(', Continent, ')') As Name_continent, Region, Population from country 
where population between 45000000 and 55000000 order by Population DESC;






