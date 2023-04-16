
 

$('#omdb_btn').click(function() {

    if ($('#movie_title').val() != '') {
        $.ajax({
            type : 'GET',
            data : {
              datas : $('#movie_title').val()
            },
            success : function(res) {
              window.location.href = '/fetch-movie-data/' + '?title=' + $('#movie_title').val()
            }
        
          });
       }
});

$('#movie_title').keydown(function(e) {

   if (e.which == '13' && $('#movie_title').val() != '') {
    $.ajax({
        type : 'GET',
        data : {
          datas : $('#movie_title').val()
        },
        success : function(res) {
          window.location.href = '/fetch-movie-data/' + '?title=' + $('#movie_title').val()
        }
    
      });
   }
  });


$('#director_filter').keydown(function(e) {
    if (e.which == '13') {
        $.ajax({
            type : 'GET',
            success : function(res) {
              window.location.href = '/movie?' + 'director' + '=' + $('#director_filter').val()
            }
        
          });
    }
  });

  $('#title_filter').keydown(function(e) {
    if (e.which == '13') {
        $.ajax({
            type : 'GET',
            success : function(res) {
              window.location.href = '/movie?' + 'name' + '=' + $('#title_filter').val()
            }
        
          });
    }
  });

  $('#genre_filter').keydown(function(e) {
    if (e.which == '13') {
        $.ajax({
            type : 'GET',
            success : function(res) {
              window.location.href = '/movie?' + 'genre' + '=' + $('#genre_filter').val()
            }
        
          });
    }
  });

  $('#actor_filter').keydown(function(e) {
    if (e.which == '13') {
        $.ajax({
            type : 'GET',
            success : function(res) {
              window.location.href = '/movie?' + 'actor' + '=' + $('#actor_filter').val()
            }
        
          });
    }
  });