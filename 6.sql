create database naver_db;
use naver_db;
show naver_db;
create table member_info
(
	mem_id  char(8)         not null     primary key,
    mem_name  varchar(10)   not null,
	mem_number  tinyint     not null,
    addr  char(2)           not null,
    phone1  char(3)         null,
    phone2  char(8)         null,
    height  tinyint         unsigned     null, 
    debut_date  date        null
);
describe member_info;

create table buy_info
( 
     num  int              not null     auto_increment     primary key,
     mem_id  char(8)       not null,
     prod_name  char(6)    not null,
     group_name  char(4)   null,
     price  int            not null,
     amount  smallint      not null
);
describe buy_info;


insert into `member_info`
(mem_id, mem_name, mem_number, addr, phone1, phone2, height, debut_date)
values
('TWC', '트와이스',  9, '서울','02', '11111111', 167, '2015-10-19'),
('BLK', '블랙핑크',  4, '경남', '055', '22222222', 163, '2016-08-08'),
('WMN', '여자친구',  6, '경기', '031', '33333333', 166, '2015-01-15'),
('OMY', '오마이걸',  7, '서울', null, null, 160, '2015-04-21'),
('GRL', '소녀시대',  8, '서울', '02', '44444444', 168, '2007-08-02'),
('ITZ', '잇지',     5, '경남', null, null, 167, '2019-02-12'),
('RED', '레드벨벳',  4, '경북', '054', '55555555', 161, '2014-08-01'),
('APN', '에이핑크',  6, '경기', '031', '77777777', 164, '2011-02-10'),
('SPC', '우주소녀',  13, '서울', '02', '88888888', 162, '2016-02-25'),
('MMU', '마마무',    4, '전남', '061', '99999999', 165, '2014-06-19');

select * from member_info;



insert into `buy_info`
(mem_id, prod_name, group_name, price, amount)
values
('BLK', '지갑', null, 30, 2),
('BLK', '맥북프로', '디지털', 1000, 1),
('APN', '아이폰', '디지털', 200, 1),
('MMU', '아이폰', '디지털', 200, 5),
('BLK', '청바지', '패션', 50, 3),
('MMU', '에어팟', '디지털', 80, 10),
('GRL', '혼공SQL', '서적', 15, 5),
('APN', '혼공SQL', '서적', 15, 2),
('APN', '청바지', '패션', 50, 1),
('MMU', '지갑', null, 30, 1),
('APN', '혼공SQL', '서적', 15, 1),
('MMU', '지갑', null, 30, 4);

select * from buy_info;

alter table buy_info add constraint foreign key(mem_id) references member_info(mem_id);
describe member_info;
describe buy_info;



# inner join  으로 테이블 합치기 
select * from member_info As m 
inner join buy_info As b 
On m.mem_id=b.mem_id ;

# left join  으로 테이블 합치기 
select * from member_info As m 
left join buy_info As b 
On m.mem_id=b.mem_id ;

# right join  으로 테이블 합치기 
select * from member_info As m 
right join buy_info As b 
On m.mem_id=b.mem_id ;

# ---------------------------------------------------------------------------
# 서브쿼리
# 쿼리 안에 또 다른 쿼리를 이용해서 원하는 데이터를 조회
# 이름의 에이핑크인 회원의 평균키 보다 큰 회원을 조회하기 
select * from member_info;
select * from buy_info;
select * from member_info order by height DESC;

# 쿼리를 한번에 써서 에이핑크의 키와 그보다 큰 사람 알아내기 
select mem_name, height from member_info where height > 164; #1
select * from member_info where mem_name = '에이핑크'; #2
# 합치기
select mem_name, height from member_info 
where height > (select height from member_info where mem_name = '에이핑크');

