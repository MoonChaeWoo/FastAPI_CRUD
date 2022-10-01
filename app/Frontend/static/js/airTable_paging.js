// 테이블의 가로행
const rows = $('#airTable tbody tr')

// 페이지네이션의 ol id값
const pageNation = $('#numbers')

// 페이지당 보여줄 갯수
let rowsPerPage = 10;

// 페이지 인덱스 시작 
let numStart = 1;

// 한번에 보여줄 페이지 인덱스 갯수
let numPerCount = 5;

// 가로행의 tr 갯수
let rowsCount = rows.length;

// 페이지 수
let pageCount = Math.ceil(rowsCount/rowsPerPage);

// 페이지 인덱스의 끝
let numEnd = pageCount;

for(let i = 1; i <= pageCount; i++){
    pageNation.append('<li><a href="">'+ i +'</a></li>');
}

let pageNationLi = $('#numbers li');

let pageLength = pageNationLi.length;

// 첫번째 a태그 스타이리에 효과 부여
pageNation.find('li:first-child a').addClass('active');

// 페이징 함수 (Rows)
function displayRows(idx){
    let start = (idx - 1) * rowsPerPage;
    let end = start + rowsPerPage;

    rows.hide();
    rows.slice(start, end).show();
}

function displayNum(idx){
    let numberStart = idx - 1;
    let numberEnd = idx + numPerCount;

    pageNationLi.hide();

    if(numberEnd >= pageLength && numberStart > (pageLength - numPerCount)){
        pageNationLi.slice(pageLength - numPerCount, pageLength).show();
    }else if(numberStart <= (numPerCount - 2)){
        pageNationLi.slice(0, numPerCount).show();
    }else{
        pageNationLi.slice(idx - 3, idx + 2).show();
    }
}

displayRows(1);
displayNum(1);

pageNation.find('li a').click(function(e){
    e.preventDefault();
    $(this).parents('li').siblings().find('a').removeClass('active');
    $(this).addClass('active');
    let index = parseInt($(this).text());
    displayRows(index);
    displayNum(index);
});