
$(document).ready(function() {

  var played_videos = []; //so we know we played the videos,
  var unplayed_videos = []; //which ones we haven't played

  function update(){
    rid = $("#room-info").attr("rid");
    $.ajax({
      url:'/update/' + rid,
      dataType: "json",
      success: function(response) {
        $('.queue-list').children().remove();
        for (q in response['queue']) {
          var title = response['queue'][q]['title'];
          var key = response['queue'][q]['key'];
          //we need to see if we've already played the video
          //we'll assume that the videos come in order of pk, or time submitted
          var item;
          if ($.inArray(key, played_videos) > -1) {//add extra class of played video
            item = $("<div>", {class:"row vid-played", text:title, key:key});
          }
          else {//if we get here, we need to check if we want to add it to the unplayed list
            item = $("<div>", {class:"row", text:title, key:key});
            if ($.inArray(key, unplayed_videos) <= -1) {//add extra class of played video
              unplayed_videos.push(key); //list of videos to queue
            }
          }
          $('.queue-list').append(item);
        };
        //we need to check the player state to know if we should start
        if (player != null) {
          if (player.getPlayerState() == -1 && unplayed_videos.length > 0) {
            player.loadVideoById(unplayed_videos[0]);
          }
        }
      },
    });
  }
  update();//call now to get the thing to load right away

  var tag = document.createElement('script');

  tag.src = "http://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

  var player;
  onYouTubeIframeAPIReady = function() {
    player = new YT.Player('yt-player', {
      height: '250',
      width: '400',
      videoId: null,
      events: {
        'onReady': onPlayerReady,
        'onStateChange': onStateChange,
      }
    });
  }

  function onPlayerReady(event) {
    player.loadVideoById(unplayed_videos[0]);
  }

  function onStateChange(event) {
    if (event.data == 0) {//ended
      //load the next song
      played_videos.push(unplayed_videos.shift());
      player.loadVideoById(unplayed_videos[0]);
    }
  }
  setInterval(update,8000);

  var yt_search_url = "https://gdata.youtube.com/feeds/api/videos";
  $( "#yt-search" ).autocomplete({
    source: function( request, response ) {
      $.ajax({
        url:yt_search_url,
        dataType: "json",
        data: {//query params
          q:request.term,
          "v":2,
          "max-results":5,
          "alt":"json",
        },
        success: function( data ) {
          response( $.map( data.feed.entry, function( item ) {
            return {
              label: item.title.$t,
              value: item.link[0].href
            }
          }));
        }
      });
    },
    minLength: 3,
    open: function() {
      $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
    },
    close: function() {
      $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
    }
  });

  $("#yt-url-upload").submit(function(e) {
    e.preventDefault();
    var data = $(this).serialize();
    $("#yt-search").val("");
    $(this).find("button").attr("disabled","disabled"); //hide the button
    $(this).find("img").css("visibility","visible");
    var form = $(this);
    form.find(".vid-submit-errors").text("");
    var rid = $("#room-info").attr("rid");
    $.ajax({
      url:"/room/" + rid,
      type:"POST",
      dataType: "json",
      data: data,
      success: function( data ) {
        form.find("button").removeAttr("disabled"); //hide the button
        form.find("img").css("visibility","hidden");
        if (data.errors) {
          form.find(".vid-submit-errors").text(data.errors);
        }
        update();
      },
    });
    return false;
  });


});




