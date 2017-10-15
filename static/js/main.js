function startPage(){
    // var thing = document.getElementsByClassName("test");
    // console.log(thing);

    // $(".ytp-large-play-button").click(function() {
    //     // var thing = $(".ytp-title-link").attr('href')
    //     console.log("here")
    // });

    // $("#test").html('WORKINTG')
    // $.getJSON($SCRIPT_ROOT + '/playlists/JSON', function(data) {
    //     playlists = data["Playlists"];
    //     for (playlist in playlists){
    //         console.log(playlists[playlist])
    //     }
    //   });

      // 2. This code loads the IFrame Player API code asynchronously.
    //
    //   var tag = document.createElement('script');
    //
	//   var thing = "{{songList}}"
	//   var test = thing.split(",");
    //
    //
    //   tag.src = "https://www.youtube.com/iframe_api";
    //   var firstScriptTag = document.getElementsByTagName('script')[0];
    //   firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    //   // 3. This function creates an <iframe> (and YouTube player)
    //   //    after the API code downloads.
    //   var player;
    //   function onYouTubeIframeAPIReady() {
    //     player = new YT.Player('player', {
	// 		playerVars: {
	// 			controls: 2,
	// 			iv_load_policy: 3,
	// 			rel: 0,
	// 			playsinline: 1
	// 		},
	// 		loadPlaylist:{
	// 			listType: 'playlist',
	// 			list: test,
	// 			index: parseInt(0),
	// 			suggestedQuality: 'large'
	// 		},
    //     	events: {
	// 			'onReady': onPlayerReady
    //       	}
    //     })
    //
    //
    //   }
    //
    // //   4. The API will call this function when the video player is ready.
    //   function onPlayerReady(event) {
    //     event.target.loadPlaylist(test)
    //   }
    //
    //   // 5. The API calls this function when the player's state changes.
    //   //    The function indicates that when playing a video (state=1),
    //   //    the player should play for six seconds and then stop.
    // //   var done = false;
    // //   function onPlayerStateChange(event) {
    // //     if (event.data == YT.PlayerState.PLAYING && !done) {
    // //       setTimeout(stopVideo, 6000);
    // //       done = true;
    // //     }
    // //   }
    //   function stopVideo() {
    //     player.stopVideo();
    //   }

};

$(document).ready(startPage);
$(document).on('page:load', startPage);
