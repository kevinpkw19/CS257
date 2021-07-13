//authors: Kevin Phung, Kyosuke Imai

//List of globally declared variables
var add_button_prefix = "a,";
var results_table_song= undefined;
var results_table_artist= undefined;
var results_table_genre= undefined;
var songID_playlist_results = undefined;
var global_playlist_names= undefined;


window.onload = initialize;


// Swaps placeholder text in the search bar based on the category chosen
function changePlaceHolder(){
  var chosen_category = document.getElementById('DDButton');
  if (chosen_category.value == 'song'){
    document.getElementById('search_string').placeholder = 'Search for song name here (e.g Yesterday)';
  }
  else if (chosen_category.value == 'artist'){
    document.getElementById('search_string').placeholder = 'Search by artist name here (e.g The Beatles)';
  }
  else if (chosen_category.value == 'genre'){
    document.getElementById('search_string').placeholder = 'Search by genre name here (e.g Rock)';
  }

}

// Completes URL string depending on search category chosen
function getURLbyCategory(){

  var chosen_category = document.getElementById('DDButton');
  var search_string = document.getElementById('search_string')

  if (chosen_category.value == 'song'){
    var url ='/search_songs?search=' + search_string.value;
    return url;
  }
  else if (chosen_category.value == 'artist'){
    var url ='/search_artist?search=' + search_string.value;
    return url;
  }

  else if (chosen_category.value == 'genre'){
    var url ='/search_genre?search=' + search_string.value;
    return url;
  }
}

//Just gets the base url for the API call
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
    global_playlist_names=results;
  })
  }
}

// check if song_id is already in a specific playlist that was chosen by the user
function checkIfDuplicate(row){
  var song_id=row.parentNode.parentNode.id;
  var distinct_id = "a," + song_id;
  var add_playlist_ddm = document.getElementById(distinct_id);
  for (var dict of songID_playlist_results){
    if(dict.playlist_name == add_playlist_ddm.value){
      if(dict.song_id == song_id){
        return true;
      }
    }

  }
}

// Loads the song ID's and their corresponding playlist name as a list of json dictionaries
function loadAllPlaylists(){
  var song_ids_and_playlist_names_url = getAPIBaseURL() + '/get_song_ids_by_playlist';
  {fetch(song_ids_and_playlist_names_url, {method: 'get'})
  .then((response) => response.json())
  .then(function(results){
    songID_playlist_results = results;
  })
  }
}

// Adds all playlist names to the dropdown menu
function addPlaylistToDDM(playlist_names, row){
  for (let item of playlist_names){
    var add_playlist_ddm = document.getElementById(row);
    var new_option = document.createElement("option");
    new_option.text = new_option.value = item.playlist_name;
    add_playlist_ddm.appendChild(new_option);
    }
  }



// Inserts a song_id into a seletected playlist in the database if there are no duplicates and an option is chosen
function insertIntoSelectedPlaylist(row){
  if (checkIfDuplicate(row)==true){
    window.alert("The song is already in the Playlist!");
  }
  else{
    var song_id=row.parentNode.parentNode.id;
    insert_url= getAPIBaseURL() + '/insert_into_playlist'
    //display error message if try to add default
    add_playlist_ddm=document.getElementById("a,"+ song_id);
    playlist_name = add_playlist_ddm.value;
    if (playlist_name=='default'){
      window.alert("Please choose a playlist to add to, or make a new one");
    } else{
    const data= {playlist_name, song_id};
    const options = {method: 'post', headers: {'Content-type': 'application/json' },body: JSON.stringify(data)};
    fetch(insert_url,options);
    songID_playlist_results.push({'playlist_name':playlist_name, 'song_id':song_id});

  }
}
}


//Loads results into the table for searching by song name. Each row id is equivalent to the id of the song that populates it.
function loadResultsIntoTableSong(results){
  let datahtml= '';
  results_body_song= document.getElementById("search_results_body_song");
  results_table_song= document.getElementById("search_results_table_song");
  var list_of_dropdowns=[]

  for (let item of results){
    var exact_category=add_button_prefix+item.song_id
    list_of_dropdowns.push(exact_category)
    datahtml+= `<tr id=${item.song_id}>
    <td>${item.song_name}</td>
    <td>${item.artist_name}</td>
    <td>${item.release_year}</td>
    <td>${item.popularity}</td>
    <td>${item.tempo}</td>
    <td>${item.duration}</td>
    <td>${item.danceability}</td>
    <td><select id= ${exact_category}  style= 'display:inline' style="float:center;" >Choose Playlist <option id = "default" value = "default"> Choose Playlist</option></select></td>
    <td><button onclick = "insertIntoSelectedPlaylist(this)" style= 'display:inline' style="float:center;" >Choose Playlist</button></td></tr>`;
  }
  results_body_song.innerHTML= datahtml;
  for (let item of list_of_dropdowns){
  addPlaylistToDDM(global_playlist_names, item)
}
  results_table_song.style.display = "inline";
  //Checks if other tables are being displayed. If so, hides them
  if (results_table_genre != undefined){
    results_table_genre.style.display = "none";
  }
  if (results_table_artist != undefined){
    results_table_artist.style.display = "none";
  }


}

//Loads results into the table for searching by artist name. Each row id is equivalent to the id of the song that populates it.
function loadResultsIntoTableArtist(results){
  let datahtml= '';
  results_table_artist= document.getElementById("search_results_table_artist");
  results_body_artist= document.getElementById("search_results_body_artist");
  var list_of_dropdowns=[]


  for (let item of results){
    var exact_category=add_button_prefix+item.song_id
    if (list_of_dropdowns.indexOf(exact_category)==-1){
    list_of_dropdowns.push(exact_category)
  }else{
    exact_category=exact_category.split(',')
    exact_category[0]=exact_category[0]+'a'
    exact_category=exact_category.join()
    list_of_dropdowns.push(exact_category)
  }
    datahtml+= `<tr id=${item.song_id}>
    <td>${item.song_name}</td>
    <td>${item.artist_name}</td>
    <td>${item.release_year}</td>
    <td>${item.popularity}</td>
    <td>${item.tempo}</td>
    <td>${item.duration}</td>
    <td>${item.danceability}</td>
    <td>${item.artist_tempo}</td>
    <td>${item.artist_duration}</td>
    <td>${item.artist_danceability}</td>
    <td><select id= ${exact_category} align='center' style= 'display:inline' style="text-align: center" >Add to Playlist <option id = "default" value = "default"> Add to Playlist</option></select></td>
    <td><button onclick = "insertIntoSelectedPlaylist(this)" style= 'display:inline' style="width:20%" >Add to Playlist</button></td></tr>`;

  }
  results_body_artist.innerHTML= datahtml;
  for (let item of list_of_dropdowns){
  addPlaylistToDDM(global_playlist_names, item)
}
  results_table_artist.style.display = "inline";

  //Checks if other tables are being displayed. If so, hides them
  if (results_table_genre != undefined){
    results_table_genre.style.display = "none";
  }
  if (results_table_song != undefined){
    results_table_song.style.display = "none";
  }

}

//Loads results into the table for searching by genre name. Each row id is equivalent to the id of the song that populates it.
function loadResultsIntoTableGenre(results){
  let datahtml= '';
  results_body_genre= document.getElementById("search_results_body_genre");
  results_table_genre= document.getElementById("search_results_table_genre");
  var list_of_dropdowns=[]

  for (let item of results){
    var exact_category=add_button_prefix+item.song_id
    if (list_of_dropdowns.indexOf(exact_category)==-1){
    list_of_dropdowns.push(exact_category)
  }else{
    exact_category=exact_category.split(',')
    exact_category[0]=exact_category[0]+'a'
    exact_category=exact_category.join()
    list_of_dropdowns.push(exact_category)
  }
    datahtml+= `<tr id=${item.song_id}>
    <td>${item.song_name}</td>
    <td>${item.genre_name}</td>
    <td>${item.artist_name}</td>
    <td>${item.release_year}</td>
    <td>${item.popularity}</td>
    <td>${item.tempo}</td>
    <td>${item.duration}</td>
    <td>${item.danceability}</td>
    <td>${item.genre_tempo}</td>
    <td>${item.genre_duration}</td>
    <td>${item.genre_danceability}</td>
    <td><select id= ${exact_category} align='center' style= 'display:inline' style="text-align: center" >Add to Playlist <option id = "default" value = "default"> Add to Playlist</option></select></td>
    <td><button onclick = "insertIntoSelectedPlaylist(this)" style= 'display:inline' style="width:20%" >Add to Playlist</button></td></tr>`;


  }
  results_body_genre.innerHTML= datahtml;
  for (let item of list_of_dropdowns){
  addPlaylistToDDM(global_playlist_names, item)
}
  results_table_genre.style.display = "inline";

  //Checks if other tables are being displayed. If so, hides them
  if (results_table_artist != undefined){
    results_table_artist.style.display = "none";
  }
  if (results_table_song != undefined){
    results_table_song.style.display = "none";
  }

}


//Chooses which table to load the JSON response into based on the search category
function chooseResults(results){
    var chosen_category = document.getElementById('DDButton');
    if(chosen_category.value == 'song'){
      loadResultsIntoTableSong(results);
    }
    else if(chosen_category.value == 'artist'){
      loadResultsIntoTableArtist(results);
    }
    else if (chosen_category.value == 'genre'){
      loadResultsIntoTableGenre(results);
    }
}

// Returns the results from the chosen search query
function returnResults(){
  var url = getAPIBaseURL() + getURLbyCategory();
  {fetch(url, {method: 'get'})
  .then((response) => response.json())
  .then(function(results){
    chooseResults(results);


  })
  }

}



// function that runs on initializing the window.
function initialize(){
    loadAllPlaylists();
    returnPlaylistnames()
    OnXevent()
  }

// Allows user to press 'enter' to search
function onPressKeyEnter(){
    var input = document.getElementById("search_string");
    input.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("search_button").click();
    }
    });
  }


// assigns elements to names and assigns them their on X event.
 function OnXevent(){
    var searchButton = document.getElementById('search_button');
    var DDButton = document.getElementById('DDButton');
    if(DDButton){
      DDButton.onchange = changePlaceHolder;
    }
    if (searchButton){
      onPressKeyEnter();
      searchButton.onclick = returnResults;
    }
  }
