window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

// mouse position
// const cvs = document.getElementById("AirWeekChart");
// const ctx = cvs.getContext("2d");
const data = {
    labels: [
      'Red',
      'Blue',
      'Yellow'
    ],
    datasets: [{
      label: 'My First Dataset',
      data: [300, 50, 100],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
      hoverOffset: 4
    }]
  };
  

const config = {
    type: 'doughnut',
    data: data,
    options: {
			maintainAspectRatio: false,
		}
  };

const myChart = new Chart(
    document.getElementById('raiderChart'),
    config
  );

  const myChart2 = new Chart(
    document.getElementById('raiderChart2'),
    config
  );

  // ------------------------------------------------------------------------

  const data2 = {
    labels: [
      'January',
      'February',
      'March',
      'April'
    ],
    datasets: [{
      type: 'bar',
      label: 'Bar Dataset',
      data: [10, 20, 30, 40],
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgba(255, 99, 132, 0.2)'
    }, {
      type: 'bar',
      label: 'Bar Dataset',
      data: [40, 30, 20, 10],
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgba(255, 99, 132, 0.2)'
    }, {
      type: 'line',
      label: 'Line Dataset',
      data: [50, 50, 50, 50],
      fill: false,
      borderColor: 'rgb(54, 162, 235)'
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

  const myChart3 = new Chart(
    document.getElementById('AirWeekChart'),
    config2
  );
