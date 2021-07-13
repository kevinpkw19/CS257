//authors: Kevin Phung, Kyosuke Imai

//List of globally declared variables
var global_playlist_names= [];


// gets Base URL for the API
function getAPIBaseURL() {
    var base_url = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return base_url;
}

// Returns all the playlist names and the amount of songs for each one
function returnPlaylistnames(){
  all_playlist_names_url= getAPIBaseURL() + '/playlist_menu';
  {fetch(all_playlist_names_url, {method: 'get'})
  .then((response) => response.json())
  .then(function(results){
    loadPlaylistsIntoTable(results);
    for (let item of results){
      global_playlist_names.push(item.playlist_name);
    }
  })
  }
}

//Loads the playlists and their total song counts into the playlists table
function loadPlaylistsIntoTable(playlist_names){
  for (let item of playlist_names){
    name=item.playlist_name;
    count= item.total_songs;
    createRow(name,count);
  }
  document.getElementById("playlists_table").style.display= "inline";
}

// Creates a row for each playlist in the table
function createRow(name,total){
  var tbody = document.getElementById("playlists_table_body");
  var row = document.createElement("tr");
  var playlist_name = document.createElement("td");
  var count = document.createElement("td");
  var delete_cell = document.createElement("td");
  var delete_button=document.createElement("button");
  var href = getAPIBaseURL() + "/api/specific_playlist_page?playlist=" + name;
  row.setAttribute('id', name);
  playlist_name.appendChild(document.createTextNode(name));
  count.appendChild(document.createTextNode(total));
  delete_button.appendChild(document.createTextNode("Delete Playlist"));
  delete_cell.appendChild(delete_button)
  row.appendChild(playlist_name);
  row.appendChild(count);
  row.appendChild(delete_cell);
  tbody.appendChild(row);
  playlist_name.setAttribute("onclick", "goToPlaylist(this)");
  delete_button.setAttribute("onclick", "deletePlaylist(this)")
}

// an onclick function to allow the user to move to the specific playlist
// when clicking on playlist  name
function goToPlaylist(row){
  name= row.parentNode.id;
  url= getAPIBaseURL() + "/specific_playlist_page?playlist=" + name;
  window.location.replace(url)
}


//Deletes the playlist from the database
function deletePlaylist(row){
  var playlist_name=row.parentNode.parentNode.id
  var table= row.parentNode.parentNode.parentNode.id
  var tester = document.getElementById(playlist_name);
  delete_url= getAPIBaseURL() + '/delete_playlist'
  const data= {playlist_name};
  const options = {method: 'post', headers: {'Content-type': 'application/json' },body: JSON.stringify(data)};
  fetch(delete_url,options);
  index=global_playlist_names.indexOf(playlist_name)
  global_playlist_names.splice(index,1);
  deleteRow(playlist_name)
}

//Deletes the playlist's row from table
function deleteRow(rowid)
{
    var row = document.getElementById(rowid);
    row.parentNode.removeChild(row);
}

// Creates a new playlist based on input. Checks for certain rules and
// adds the row to the table
function createNewPlaylist(){
  var new_playlist_name=document.getElementById("input_playlist_name").value;
  if (global_playlist_names.includes(new_playlist_name)){
    window.alert("Playlist name already exists");
  }
  else if(new_playlist_name=="") {
    window.alert("Please enter a non-blank name for the playlist");
  }
  else{
    create_playlist_url= getAPIBaseURL() + '/create_playlist'
    const data= {new_playlist_name};
    const options = {method: 'post', headers: {'Content-type': 'application/json' },body: JSON.stringify(data)};
    fetch(create_playlist_url,options);
    global_playlist_names.push(new_playlist_name);
    createRow(new_playlist_name,0);
  }
}

// An onclick function to display an overlay for user input of playlist name
function openSearch() {
  document.getElementById("createPlaylistBar").style.display = "block";
}

// An onclick function to hide the overlay for user input of playlist name
function closeSearch() {
  document.getElementById("createPlaylistBar").style.display = "none";
}

// function for all functions that are initialized on load
function initialize(){
  returnPlaylistnames()
}

window.onload = initialize();
