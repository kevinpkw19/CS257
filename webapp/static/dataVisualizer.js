// gets Base URL for the API
function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}


//onclick function that gets the specific metric for the specified playlist based on user choice
function getOnePlaylistDetails(){
  playlist1=document.getElementById('DDButtonPlaylist').value
  metric=document.getElementById('DDButtonMetric').value
  if (!(playlist1=='default' || metric=='default')){
  url= getAPIBaseURL() + '/graph_one_playlist?playlist1=' + playlist1 +'&metric=' + metric;
  console.log(url)
  {fetch(url,{method: 'get'})
  .then((response) => response.json())
  .then(function(results){
    loadDataIntoChart(results);
  })
}
}else{
  window.alert("Please select some options using the dropdown menus")
}}

// Loads the data into the chart
function loadDataIntoChart(playlist_details){
  if (playlist_details.length===0){
    window.alert("There are no songs in this playlist!")
  } else{
    xLine=[]
    yLine=[]
    keys=Object.keys(playlist_details[0])
    if (keys.includes('tempo')){
    for (let item of playlist_details){
      xLine.push(item.song_name)
      yLine.push(item.tempo)
    }
  } else if (keys.includes('danceability')){
    for (let item of playlist_details){
    xLine.push(item.song_name)
    yLine.push(item.danceability)
  }
  }else if (keys.includes('duration')){
    for (let item of playlist_details){
    xLine.push(item.song_name)
    yLine.push(item.duration)
  }
  }else if (keys.includes('popularity')){
    for (let item of playlist_details){
    xLine.push(item.song_name)
    yLine.push(item.popularity)
  }
  }

  //chart variable
  var ctx = document.getElementById('myChart').getContext('2d');
  var myChart = new Chart(ctx, {
      type: 'line',
      data: {
          labels: xLine,
          datasets: [{
              label: metric,
              data: yLine,
              pointRadius: 5,
              backgroundColor:
                  'rgba(255, 99, 132, 0.4)',
              borderColor:
                  'rgba(139,0,0, 1 )',
              borderWidth: 1
          }]
      },
      options: {
        legend: {
                labels: {
                    fontColor: "white",
                    fontSize: 14
                }
            },
          scales: {
              yAxes: [{
                display: true,
                       scaleLabel: {
                           display: true,
                           fontColor: "white",
                           fontSize: 14,
                           labelString: document.getElementById('DDButtonMetric').value
                       },
                  ticks: {
                      fontColor: "white",
                      fontSize: 10,
                      beginAtZero: true
                  }
              }], xAxes: [{
                display: true,
                       scaleLabel: {
                           display: true,
                           fontColor: "white",
                           fontSize: 14,
                           labelString: 'Songs'
                       },
                    ticks: {
                        fontColor: "white",
                        fontSize: 14,
                        stepSize: 1,
                    }
                }]
          }
      }
  });
}}

// Returns all playlists from the database to be used as options in the dropdown menu
function returnPlaylistnames(){
  all_playlist_names_url= getAPIBaseURL() + '/playlist_menu';
  {fetch(all_playlist_names_url, {method: 'get'})
  .then((response) => response.json())
  .then(function(results){
    console.log(results)
    loadAllOptionsIntoDropDownPlaylist(results)
  })
  }
}

// Loads a single option into the dropdown menu
function loadOneOptionIntoDropDownPlaylist(playlist_name){
  var DropDownPlaylist= document.getElementById('DDButtonPlaylist')
  var option=document.createElement("option")
  option.setAttribute('id',playlist_name)
  option.setAttribute('value',playlist_name)
  option.appendChild(document.createTextNode(playlist_name));
  DropDownPlaylist.appendChild(option)
}

// uses a for loop to load each option into the dropdown menu in combination with load_one_option_into_DropDownPlaylist
function loadAllOptionsIntoDropDownPlaylist(results){
  for (let item of results){
    name=item.playlist_name
    loadOneOptionIntoDropDownPlaylist(name)
  }
}

async function initialize(){
  returnPlaylistnames()
}
window.onload=initialize
