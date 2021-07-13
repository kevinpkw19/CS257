var TableInArrayRows = [];

//Just gets the base url for the API call
function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

//format a results into array list to download into CSV
function formatPlaylistResultsIntoArray(results){

  for (let item of results){
        var row = [];
        row.push(item.song_name,item.artist_name,item.release_year,item.popularity,item.tempo,item.duration,item.danceability)
        TableInArrayRows.push(row);
  }
}

// Adds the name of the playlist to the header
function changeBodyHeader(){
  param = new URLSearchParams(window.location.search);
  playlist_name = param.get('playlist');
  document.getElementById("pageHeader").innerHTML = "Your Playlist: " + playlist_name;
}

//download table data into CSV file
function downloadCSVFile() {
    //define the heading for each row of the data
    var csv = 'Song Name, Artist,Release_Year,Popularity,Tempo,Duration,Danceability\n';
    param = new URLSearchParams(window.location.search);
    playlist_name = param.get('playlist');
    //merge the data with CSV
    TableInArrayRows.forEach(function(row) {
            csv += row.join(',');
            csv += "\n";
    });

    var hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
    hiddenElement.target = '_blank';

//provide the name for the CSV file to be downloaded
  hiddenElement.download = playlist_name;
  hiddenElement.click();
}

// Returns data for the songs in that specific playlist
function returnPlaylistdata(){
  var specific_playlist_url= getAPIBaseURL()+ "/specific_playlist_info"+ window.location.search;
  {fetch(specific_playlist_url, {method: 'get'})
  .then((response) => response.json())
  .then(function(results){
    load_results_into_table_playlists(results)
    formatPlaylistResultsIntoArray(results)
    changeBodyHeader()
  })
  }
}

// Loads all the rows for the songs in that playlist
function load_results_into_table_playlists(results){
  var del_button_prefix= "d,";
  let datahtml= '';
  playlist_table= document.getElementById("playlist_table");
  playlist_body= document.getElementById("playlist_body");

  for (let item of results){
    var exact_button=del_button_prefix+item.song_id
    datahtml+= `<tr id=${item.song_id}>
    <td>${item.song_name}</td>
    <td>${item.artist_name}</td>
    <td>${item.release_year}</td>
    <td>${item.popularity}</td>
    <td>${item.tempo}</td>
    <td>${item.duration}</td>
    <td>${item.danceability}</td>
    <td><button onclick="delete_from_playlist(this)" align='center' id= ${exact_button} style= 'display:inline' >Delete from Playlist</button></td></tr>`;
  }
  playlist_body.innerHTML= datahtml;
  playlist_table.style.display = "inline";
}

// Deletes the specific song chosen from the playlist
function delete_from_playlist(row)
{
var song_id=row.parentNode.parentNode.id;
  param = new URLSearchParams(window.location.search);
  playlist_name = param.get('playlist');
  delete_url= getAPIBaseURL() + '/delete_from_playlist'
  const data= {song_id,playlist_name};
  const options = {method: 'post', headers: {'Content-type': 'application/json' },body: JSON.stringify(data)};
  fetch(delete_url,options);

  button=document.getElementById("d,"+ song_id);
  button.style.display= 'none';
}

// Contains all functions that need to run on initialize
function initialize(){
  returnPlaylistdata()
}

window.onload = initialize();
