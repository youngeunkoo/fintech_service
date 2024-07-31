document.write("자바스크립트 외부 링크 테스트");

// : 한줄 주석
/* 여러줄 주석 */

// 변수 variant : 자료를 넣는 상자, 1개만 담을 수 있음, 나중에 담은 것으로 대체
// let 변수명 : 자료를 업데이트 할 수 있는 변수
// const 변수명 : 처음 선언할때만 자료를 넣을 수 있고, 업데이트가 안되는 변수
// 변수 이름 만드는 법 : 카멜 표기법 - 시작은 소문자 다른 단어가 붙으면 그 단어는 대문자로
// ex) myName, finalResult  

// let : 같은 이름의 변수 생성 불가능
let num;   //num이라는 이름의 변수 선언 빈박스 만듦
num = 10;  //num이라는 박스에 10이라는 자료를 넣음
           // = 는 오른쪽에 있는 자료를 왼쪽에 넣는다(할당한다)는 뜻   

let num2 = 20; //변수를 선언함과 동시에 자료 할당

console.log(num);  // 웹브라우저의 개발자도구(f12)의 console에 출력
document.write(num + num2);  // 웹브라우저의 html 화면에 출력


// const : 상수형 변수, 같은 이름의 변수 생성 불가능, 선언 후 할당도 불가능
// 선언과 동시에 값을 할당

// const num3 ; //선언만 했기 때문에 오류
const num3 = 30;
document.write(num3);

//num3 = 40;  //const 변수에 재할당을 하려고 해서 에러 
let num4 = 50;
const num5 = 100;
let result = num4 * num5;
document.write(result);
// ------------------------------------------------------------------------------------------
// 자료형
// 숫자형(정수, 실수),  문자형,  논리형(True, False)
// 배열 array[숫자or문자or함수or 객체리터럴] --> 순서가 있음. 인덱싱, 스라이싱
// 객체리터럴, JSON, {key : value}

// 숫자형
num = 10; //정수형
num2 = 3.14;  //
num4 = 3;
let num6 = 2;
console.log(num*num2); //정수 * 실수 = 실수
console.log(num / num2); //정수 / 실수 = 실수
console.log(num / num4); //정수 / 정수 = 소숫점이 있어 실수
console.log(num / num6); //정수 / 정수 = 정수 


// 문자형
let string1 = "hello";
let string2 = "javascript" //쌍따옴표 말고도, 그냥 따옴표로 감싸도 됨
console.log(string1);
console.log(string1+string2); //문자+문자 = 연결됨, 즉 hellojavascript 라고 출력될거임
console.log(string1+" "+string2); //공백도 1개의 문자임, 즉 hello javascript 라고 출력될거임


// 이스케이프 문자: 대부분 모든 언어에서 공통되게 사용함!
console.log(string1+"\t"+string2); // \t : 수평 탭 --> hello	javascript
console.log(string1+"\n"+string2); // \n : 줄바꿈
console.log(string1+"\'"+string2+"\'"); // \' : 작은 따옴표 --> hello'javascript'

// 템플릿 문자열 (백틱 ` `)
let string3 = `템플릿 문자열은 큰따옴표(")나 작은따옴표(')가 아닌 백틱(\`)으로 문자열을 만듦` //양사이드 백틱임
console.log(string3);
let string4 = `템플릿 문자열은 \${\}을 이용해서 변수의 내용을 바로 출력 가능 
               num : ${num}`;
console.log(string4);
console.log(`num + num2 = ${num+num2}`);



//-----------------------------------------------------------------------------------------------
// 배열 array : 여러개의 자료가 나열되어 있는 형태의 자료형 
// [ ] 대괄호 안에 여러개의 다른 데이터형의 자료도 넣을 수 있음
// 순서가 있는 자료형, 순서에 맞춰 인덱스 번호가 부여됨
// 번호로 자료를 호출 가능, 범위를 지정해서 호출도 가능
let koreansScore = 80;
let englishScore = 70;
let mathScore = 90;
let scienceScore = 60;

let studentScore = [80, 70, 90, 60];  // 국어, 영어, 수학, 과학 점수 --> 객체 object 
// 객체 : 택배 박스 안 작은 소포 박스라고 생각하면 됨. 
// 넣는 개수는 제한되어 있지 않음
// 배열에는 문자 숫자 섞어서 넣는게 가능함 --> 유연한 언어임
// let arrayValues = [80, 3.14, "배열", {, '신기해',{배열:'array'}}]
let arrayValues = [80, 3.14, "배열", [1,'신기해',{배열:'array'}]];
console.log(studentScore);
console.log(arrayValues);
// 배열은 순서가 있다. 배열 안에 있는 자료를 꺼내는 방법 : 번호를 불러 꺼내면 됨
// 0번부터 번호가 순서대로 매겨짐
// 배열 안의 자료를 꺼내는 방법은 배열 변수명[번호]
console.log(studentScore[1]); //80이 0번, 70이 1번, 90이 3번, 60이 4번임 --> 그래서 70이 출력됨
console.log(studentScore[0]); // 0번은 80이 출력됨 
console.log(arrayValues[2]);
console.log(arrayValues[3][1]); //'신기해'출력하기 
// 금융사에서  openAPI 로 데이터 주고 받을 때, 까보면 다 배열 형식으로 되어있음. 
// 전문정의서랑 .js 형식으로 되어있는 걸 비교해서 확인 후 데이터를 보는 것이 중요하다.
// 그래서 배열을 이해하는게 중요함. 

let arrayValues2 = [60, 2, "연습", [3, '우와', {배열배우기 : 'pracitce'}]];
console.log(arrayValues2[3][1]);

// 객체 리터럴 JSON
// {key : value}
// key를 호출하면 value가 출력됨
// [홍길동, 보성고등학교, 18]  --> 배열 
// {name : '홍길동', school: '보성고등학교, age: 18}   --> 윗줄 배열보다 이게 더 명확하게 어떤 데이터인지 알 수 있음
// 그래서 요즘은 배열보다 객체 리터럴(JSON)을 거의 사용함
let addressList = {name : '홍길동', school: '보성고등학교', age: 18};
console.log(addressList);
let addressList2 = {name : ['홍길동', '둘리', '김연아'],
                    school : ['잠실', '동북', '정신'],
                    age : [18, 17, 19]};
console.log(addressList2);
// 객체 리터럴의 자료를 꺼내는 방법 : key를 호출한다. {key}
console.log(addressList2['name'][2]); //김연아 호출하기 type 1
console.log(addressList2.name[2]); //김연아 호출하기 type 2





//----------------------------------------------------------------------------------------------
// 자바스크립트는 자동 형변환이 됨.
// 형변환 : 자료형을 바꾸는 것
// 암시적 형변환
const numChar = 10 + "10"; //자바스크립트에서는 숫자와 문자 연산을 하면 자동으로 문자 
console.log(numChar); 
const numChar2 = 10 + "StingChar"; 
console.log(numChar2);

let strNum = "10";
num = 10;
if(num == strNum) {
    console.log("같음"); //strNum은 문자이지만 숫자형태라서 숫자 10과 비교시 숫자로 자동변환됨
}

let strNum2 = "10";
num = 10;
if(num === strNum2) {
    console.log("같음"); 
}else{
    console.log("다름"); 
}


// 전치연산 vs 후치연산 
// 연산자 : + - * / % **
// 전치연산 : ++a 는 a를 먼저 1 증가 후 +연산
// 후치연산 : a++ 는 먼저 더하기 후 1증가시켜 내보냄
let a = 1;
let b = 1;
console.log("a+b: ", a+b);  //출력 : 2
console.log("a++ + b++: ", a++ + b++);  //출력 : 2
console.log("a + b: ", ++a + ++b); //출력 : 6

//------------------------------------------------------------------------------------
// 비교연산자
// == : x, y의 값이 같으면 true
// === : x,y의 값과 자료형이 같으면 true
//-----------------------------------------------------------------------------------
// 논리 연산자
// && : and 연산
// || : or 연산 
//-----------------------------------------------------------------------------------
// 삼항 연산자 : x냐? 참 y, 거짓 z
let score = 90;
let grade = score >= 90? 'A+' : 'B';
console.log(grade);



//-----------------------------------------------------------------------------------
// 조건문 다루기 : if else. else if
/*  if (조건) {
    참 일때 실행문
    } else {
    거짓일 때 실행문
    } 
*/
num = "10";   //형변환이 자동으로 됨
if (num % 2 === 0) {   // 짝수인지 판별
    console.log("숫자는 짝수입니다.")
} else {
    console.log("숫자는 홀수입니다.")
}


num = 9;
if (num % 2 === 0) {   // 짝수인지 판별
    console.log("숫자는 짝수입니다.")
} else {
    console.log("숫자는 홀수입니다.")
}

num = 9;
if (num % 2 === 0) {   // 짝수인지 판별
    console.log("숫자는 짝수입니다.")
} else if (num % 2 === 1){
    console.log("숫자는 홀수입니다.")
} else {
    console.log("입력이 잘못 되었습니다.")
}

//---------------------------------------------------------------------------------
// 반복문 다루기 : for, for...in
// for(let i=0; i < 5 ; i++) {
// 반복 시킬 명령/문장 
// }
for (let i=0; i<5; i++){
    console.log(i, studentScore[i]); 
}
// let studentScore = [80, 70, 90, 60];  // 국어, 영어, 수학, 과학 점수 참고 



// 중첩 반복문 : 반복문 안에 반복문이 또 있는 것. 
// 안쪽 반복문이 다 돌고 바깥쪽이 돌아감  --> 바늘시계 
// 바늘시계 : 초 --> 분 --> 시 
// for (let i=0; i<=12; i++){
//     //console.log(`${i}시`);
//     for(let j=0; j<=59; j++){
//         console.log(`${i}시 ${j}분`);  //``백틱키를 사용함
//     }
// }


// for...in : 배열을 돌릴 때 아주 좋음
for(let index in studentScore) {
    console.log(studentScore[index]);  // 80, 70, 90, 60 으로 이어서 출력됨
}



// for...in 반복문 객체 리터럴(JSON)과 함께 사용
console.log(addressList);
// let addressList = {name : '홍길동', school: '보성고등학교', age: 18};
for(let keyName in addressList){
    console.log(keyName,addressList[keyName]);
}  // name 홍길동, school 보성고등학고,  age 18로 출력됨



// 여러 요소들이 있을 때 출력하기 
console.log(addressList2);
// let addressList2 = {name : ['홍길동', '둘리', '김연아'],
//     school : ['잠실', '동북', '정신'],
//     age : [18, 17, 19]};
for (let keyName in addressList2) { 
    console.log(keyName, addressList2[keyName]);
    for (let index in addressList2[keyName]){
        console.log(keyName,addressList2[keyName],[index]);
    }
}





// break문 : 반복문을 중단시킬 때 사용
// for(let i=0; i<=100; i++){
//     console.log(i);
//     if(i===10) break; 
// }

// // continue문 : 특정 조건을 만나면 건너뜀
// for(let i=1; i<=100, i++){
//     if(i%2 === 1){
//         console.log(i);
//     } else {
//         continue;
//     }
// }



//----------------------------------------------------------------------------------------
//  함수 fuction 함수명(인자or값){
//     인자 값 받아서 처리하는 코드 
//     return 값
//  }

// 함수명(값)
// console.log(String(num));
// 구구단 만들기 
function gugudan(num){
    for(let i=1; i<=9; i++){
        console.log(`${num} * ${i} = ${num*i}`);
    }
}
gugudan(3); //구구단 3단 출력하기



// const 변수명 = function 함수명() { 
//               인자 값 받아서 처리하는 코드 
//  } 
const fn1 = function gugudan(num) {
    for(let i=1; i<=9; i++){
        console.log(`${num} * ${i} = ${num * i}`);
    }
}
fn1(7);

// 화살표 함수 
// 요새는 거의 ()=>{} 이렇게 화살표함수로 함수를 정의함
// const gugudan = () => {
//     for(let i=1; i<=9; i++){
//         console.log(`3 * ${i} = ${3 * i}`);
//     }
// };
// gugudan();


// return 
const calcSum = (num1, num2) => {
    result = num1 + num2;
    return result;
}
let sumResult = calcSum(6,3)
console.log(sumResult);

// 문제?
//2개 숫자를 입력해서 그 사이에 있는 숫자 중에서 홀수인 수만 출력하고 리턴
const hol = (num1, num2) => {
    let arr = []
    for(let i=num1; num1<=num2; num1++){
        if(num1 % 2 === 1) {
            console.log(num1);
            arr.push(num1);
        }
    }
    return arr;
}
let holResult = hol(1,10)
console.log(holResult);









//-------------------------------------------------------------------------------------
// 브라우저 객체 모델 사용하기 
function popup() {
    window.open('http://www.naver.com','팝업', 'winth=200', height='100') 
}  