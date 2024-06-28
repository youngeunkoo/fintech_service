create schema testdb;
create database testdb2;

# testdb3 이라는 이름의 DB파일이 없으면 만들어라. 
create database if not exists testdb3;

#drop : 삭제하기
DROP database testdb3;

# 해당 파일 있으면 삭제해라
Drop database if exists testdb3;
Drop database if exists testdb2;
Drop database testdb;

#------------------------------------------------------------------------------------------------------
Create database if not exists zwork;

Create database zwork_1;
Drop database zwork_1;
Create database if not exists zwork_1;
Drop database if exists zwork_1;
#------------------------------------------------------------------------------------------------------

use zwork;
create table highschool_students
(
   student_no  varchar(20), 
   student_name  varchar(100),
   grade  tinyint, 
   class  varchar(50),
   gender  varchar(20),
   age  smallint,
   enter_date  date
   ); #컬럼명, datatype 만들기

#생성한 테이블의 구조를 출력 describe, desc
describe highschool_students;

#제약조건 넣어 테이블 다시 만들어보기 : null, not null
create table highschool_students2
(
    student_no   varchar(20) not null, 
    student_name   varchar(100) not null,
    grade  tinyint null,
    class  varchar(50) null,
    gender  varchar(20)  null,
    age  smallint null,
    enter_date  date
    );

describe highschool_students2;

drop table highschool_students; #테이블 삭제하기 

#기본키를 포함해서 만들기 (기본키 : pk, primary key)
create table highschool_students
(
    student_no   varchar(20) not null primary key,  #콤마하지 않는다
	student_name   varchar(100) not null,
    grade  tinyint null,
    class  varchar(50) null,
    gender  varchar(20)  null,
    age  smallint null,
    enter_date  date
    );
describe highschool_students;
drop table highschool_students;



create table highschool_students
(
    student_no   varchar(20) not null,
	student_name   varchar(100) not null,
    grade  tinyint null,
    class  varchar(50) null,
    gender  varchar(20)  null,
    age  smallint null,
    enter_date  date,
    primary key(student_no) #이렇게도 primary key 지정 가능!
    );
describe highschool_students;
drop table highschool_students;

# constraint primary key 로 기본키 설정하기
create table highschool_students
(
    student_no   varchar(20) not null,
	student_name   varchar(100) not null,
    grade  tinyint null,
    class  varchar(50) null,
    gender  varchar(20)  null,
    age  smallint null,
    enter_date  date,
    constraint primary key(student_no) #이렇게도 primary key 지정 가능!
    );
describe highschool_students;



#기본키 삭제하기 : alter
#alter : 만들어진 데이터나 테이블을 수정하는 명령어
alter table highschool_students drop primary key;
#primary key 삭제하기
describe highschool_students;
	
#기본키 추가하기 : alter 
alter table highschool_students add primary key(student_no);
describe highschool_students;

#------------------------------------------------------------------------------------------------------











