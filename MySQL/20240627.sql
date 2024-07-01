use zwork;
select * from highschool_students;
# 테이블에 자료를 넣는 법 
# insert into `테이블명` (컬럼명1, 컬럼명2...) values (컬럼1 data, 컬럼2 data...) ;
# 따옴표가 아니라 왼쪽 상단 Esc 키 바로 밑

describe highschool_students;
insert into `highschool_students` 
(student_no, student_name, grade, class, gender, age, enter_date)
values 
('TB0001', '강나린', 1, '10반', '여자', 20, '2024-03-02');

insert into `highschool_students` 
(student_no, student_name, grade, class, gender, age, enter_date)
values 
('TB0002', '금나일', 1, '4반', '남자', 20, '2024-03-02'),
('TB0003', '곽현정', 1, '5반', '여자', 20, '2024-03-02'),
('TB0004', '임원재', 1, '2반', '남자', 20, '2024-03-02')
;

select * from highschool_students;


