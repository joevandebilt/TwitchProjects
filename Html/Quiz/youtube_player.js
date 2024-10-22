var Debugging = false;
var enablePlayer = true;

var playlists = [
    //You can add a whole playlist here
    "https://www.youtube.com/playlist?list=PLW_omwEM1aiem13x9zZVQ4IQEqAEVKA7S",	//ROYALTY FREE PLAYLIST
    "https://www.youtube.com/playlist?list=PLzCxunOM5WFLNCSF0UEHZqFJJlmdeL71S", //Soundcloud
    "https://www.youtube.com/playlist?list=PLpBHp10gVHH1vNdFsh6qDIOB7oIz7zj69",	//DANKMUS VIDEOS
    "https://www.youtube.com/playlist?list=PLwJjxqYuirCLkq42mGw4XKGQlpZSfxsYd"  //8-Bit Games
];

var videos = [
    //You can put individual video links in here!
    "https://www.youtube.com/watch?v=6jIJKQCDeVc&ab_channel=mastertegm"
];

var player;
function GetRandomVideo () {
    var index = Math.round(Math.random() * (videos.length - 1));
    var entry = videos[index];
    if (entry.length === 11) {
        return entry;
    } else {
        entry = getParameterByName("v", entry);
    }
    return entry;
}

function onYouTubePlayerAPIReady(videoId) {
    if (enablePlayer) {
        player = new YT.Player('player', {
            width: '1920',
            height: '1080',
            events: {
                onReady: onPlayerReady,
                onStateChange: onPlayerStateChange
            },
            playerVars: {
                "autoplay": true,
                "shuffle": true,
                "fullscreen": true,
                "rel": false
            }
        });
    }
}

// autoplay video
function onPlayerReady(event) {

    log("onPlayerReady");
    log(event);

    if (playlists.length === 0) {
        player.loadVideoById(GetRandomVideo());
        event.target.playVideo();
    } else {
        CueNextPlaylist(event);
    }
}

function playingVideo(event){
    log("Playing Video")
    log(event.target.getVideoData());

    var videoData = event.target.getVideoData();
    
    document.getElementById("videoTitle").innerHTML = videoData.title;
    document.getElementById("videoOwner").innerHTML = videoData.author;
}

// when video ends
function onPlayerStateChange(event) {        
    log("Player State has changed: Status " + event.data);
    log(event);

    /*
        -1 – unstarted
        0 – ended
        1 – playing
        2 – paused
        3 – buffering
        5 – video cued
    */

    if(event.data === 0) {         
        log("Video has ended, playing next one"); 
        player.loadVideoById(GetRandomVideo());
    }
    else if (event.data === 1) {
        log("Video started playing");
        playingVideo(event);
    }
    else if (event.data === 3){
        log("Buffering Event");
    }
    else if (event.data === 5) {

        log("Video has been cued");

        //Add these videos to our master playlist
        videos = videos.concat(event.target.getPlaylist());

        if (playlists.length === 0) {
            player.loadVideoById(GetRandomVideo());
        }
        else {
            CueNextPlaylist(event);
        }
    }
    else 
    {
        log("Unhandled playback code detected: " + event.data);
        log("Attempting to just play another video");
    }
}

function CueNextPlaylist(event) {
    var playlistId = playlists.pop();
    if (playlistId.startsWith("http") || playlistId.startsWith("www") || playlistId.startsWith("youtube")) {
        playlistId = getParameterByName("list", playlistId);
    }

    event.target.cuePlaylist({
        listType: 'playlist',
        list: playlistId,
    });
}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
        name = name.replace(/[\[\]]/g, '\\$&');
    
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    
    if (!results) return null;
    if (!results[2]) return '';
    
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function log(input) {
    if (Debugging) {
        console.log(input);

        var linebreak = document.createElement("br");
        var consoleWindow = document.getElementById("ConsoleLog");
        
        if (typeof input === 'object' && input !== null)
        {
            input = "Data packet logged, check dev console for more info";                
        }
        consoleWindow.prepend(linebreak);
        consoleWindow.prepend(input);            

        consoleWindow.style = "";
    }
}