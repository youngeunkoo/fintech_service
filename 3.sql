use world;
show tables; 
describe city;
describe country;
describe countrylanguage; 

select * from city;
select CountryCode, Name, District, Population, ID from city; 

select * from zwork.highschool_students;

select * from city where Countrycode = 'KOR' and District like 'k%';

select * from city where Countrycode = 'KOR' and District in('Seoul', 'Kyonggi');

select * from country where Population > 100000000 order by population desc;


#우리나라 인구와 비슷한 나라 찾기
select * from country where Name = 'South Korea'; 
select * from country where Population between 45000000 and 55000000;

#----------------------------------------------------------------------------------
# 박스오피스 데이터 조회
use zwork;
describe box_office; 

select * from box_office limit 5;


# 개봉날짜 : 2018-01-01 ~ 2018-12-31 사이에 개봉한 한국 영화 데이터 조회
select movie_name, rep_country, release_date from box_office 
where rep_country = '한국' and release_date >= '2018-01-01' and release_date <= '2018-12-31';

select movie_name, rep_country, release_date from box_office 
where rep_country = '한국' and release_date between '2018-01-01' and '2018-12-31';


# 2019년에 개봉한 영화 중, 관객이 천만 이상인 영화
# audience_num : 관객 수 
select * from box_office;

select * from box_office
where release_date between '2019-01-01' and '2019-12-31' 
and audience_num >= 10000000
order by audience_num desc;


#----------------------------------------------------------------------------------
# world country 테이블에서 인구가 1억명을 초과하는 나라를 추출하고 
# 인구순으로 내림차순 정렬
use world;
show tables;
select * from country ;
select Name, Population from country where Population > 100000000 
order by Population ;

# 조회된 데이터를 2개 컬럼을 기준으로 정렬
# country 테이블에서 인구수가 5000만명 이상인 나라를 찾아서
# continent 은 오름차순 정렬 , region 은 내림차순 정렬
use world;
select Name, Continent, Region, Population from country where Population >= 50000000
order by continent ASC, region DESC;

