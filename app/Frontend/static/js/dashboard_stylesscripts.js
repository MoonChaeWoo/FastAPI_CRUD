window.addEventListener('DOMContentLoaded', event => {

    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {

        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }
});

let air_value1;
let air_value2;
let air_value3;
let air_value4;

let data_air = $('#airTable tbody').data('air');
data_air = data_air.replaceAll("\'","\"");
data_air = data_air.replaceAll("None", "\"None\"");
data_air = JSON.parse(data_air);

data_air.forEach((value) => {
  if (value.stationName == '담양읍'){
    air_value1 = value
  }
  
  if (value.stationName == '곡성읍'){
    air_value2 = value
  }

  if (value.stationName == '구례읍'){
    air_value3 = value
  }

  if (value.stationName == '화순읍'){
    air_value4 = value
    // value4.push(value.pm10Value);
    // value4.push(value.pm25Value);
  }
});

let dis_value1;
let dis_value2;
let dis_value3;
let dis_value4;

let data_dis = $('#airTable tbody').data('dis');
console.log(data_dis);
data_dis = data_dis.replaceAll("\'","\"");
data_dis = data_dis.replaceAll("None", "\"None\"");
data_dis = JSON.parse(data_dis);

data_dis.forEach((value) => {
  if (value.lowrnkZnCd == 46710){
    dis_value1 = value;
  }

  if (value.lowrnkZnCd == 46720){
    dis_value2 = value;
  }

  if (value.lowrnkZnCd == 46730){
    dis_value3 = value;
  }

  if (value.lowrnkZnCd == 46790){
    dis_value4 = value;
    // value4.push(value.cnt);
  }
});

const data = {
  labels: [
    '담양군',
    '곡성군',
    '구례군',
    '화순군'
  ],
  datasets: [{
    type: 'bar',
    label: '미세먼지(PM10)',
    data: [air_value1.pm10Value, air_value2.pm10Value, air_value3.pm10Value, air_value4.pm10Value],
    borderColor: 'rgb(255, 99, 132)',
    backgroundColor: 'rgba(255, 253, 0, 0.5)'
  }, {
    type: 'bar',
    label: '미세먼지(PM25)',
    data: [air_value1.pm25Value, air_value2.pm25Value, air_value3.pm25Value, air_value4.pm25Value],
    borderColor: 'rgb(255, 99, 132)',
    backgroundColor: 'rgba(99, 233, 255, 0.5)'
  }, {
    type: 'line',
    label: '천식예측진료건수',
    data: [dis_value1.cnt, dis_value2.cnt, dis_value3.cnt, dis_value4.cnt],
    fill: false,
    borderColor: 'rgb(54, 162, 235)'
  }]
};

const config = {
  type: 'scatter',
  data: data,
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
};

const myChart = new Chart(
  document.getElementById('AirWeekChart'),
  config
);

//----------------------------------------------------
const data2 = {
  labels: [
    '아황산가스농도',
    '일산화탄소농도',
    '오존농도',
    '이산화질소농도'
  ],
  datasets: [{
    type: 'line',
    label: '담양군',
    data: [air_value1.so2Value, air_value1.coValue, air_value1.o3Value, air_value1.no2Value],
    fill: false,
    borderColor: 'rgb(245, 66, 66)'
  }, {
    type: 'line',
    label: '곡성군',
    data: [air_value2.so2Value, air_value2.coValue, air_value2.o3Value, air_value2.no2Value],
    fill: false,
    borderColor: 'rgb(236, 245, 66)'
  }, {
    type: 'line',
    label: '구례군',
    data: [air_value3.so2Value, air_value3.coValue, air_value3.o3Value, air_value3.no2Value],
    fill: false,
    borderColor: 'rgb(54, 162, 235)'
  }, {
    type: 'line',
    label: '화순군',
    data: [air_value4.so2Value, air_value4.coValue, air_value4.o3Value, air_value4.no2Value],
    fill: false,
    borderColor: 'rgb(182, 66, 245)'
  }]
};

const config2 = {
  type: 'scatter',
  data: data2,
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
};

const myChart2 = new Chart(
  document.getElementById('lineChart'),
  config2
);