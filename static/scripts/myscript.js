$(document).ready(function() {

  function millisecToTime(string) {

    // Pad to 2 or 3 digits, default is 2
    function pad(number, decimal_places) {
      decimal_places = decimal_places || 2;
      return ('00' + number).slice(-decimal_places);
    }

    var millisec = string % 1000;
    string = (string - millisec) / 1000;
    var secs = string % 60;
    string = (string - secs) / 60;
    var mins = string % 60;
    var hrs = (string - mins) / 60;

    return pad(hrs) + ':' + pad(mins) + ':' + pad(secs) + '.' + pad(millisec, 3);
  }

  function populateDetails(selection_string, details) {

    for (var key in details)
    {
      var sample_elem = '<div class="row file-property m--margin-15 clickable">' + 
                        '  <div class="property-key"></div>' +
                        '  <div class="property-value"></div>' +
                        '</div>'

      if ('file_size' == key.toLowerCase() || 'stream_size' == key.toLowerCase())
      {
        var value = details[key] + '&nbsp;&nbsp;(' + 
          Number(details[key] / 1024 / 1024).toFixed(2) + ' MBs)'
      }
      else if ('duration' == key.toLowerCase())
      {
        var value = details[key] + '&nbsp;&nbsp(' + millisecToTime(details[key]) + ')'
      }
      else if ('resolution' == key.toLowerCase())
      {
        var value = details[key][0] + ' x ' + details[key][1]
      }
      else if ('bit_rate' == key.toLowerCase())
      {
        var value = details[key] + '&nbsp;&nbsp(' + 
          Number(details[key] / 1024).toFixed(2) + ' KB / sec)'
      }
      else
      {
        var value = details[key]
      }

      if ($.isArray(value))
      {
        key = value[0]
        value = value[1].replace(':', ' : ')
      }

      $('div' + selection_string + ' div.m-portlet__body').append(sample_elem)
      $('div' + selection_string + ' div.file-property:last').find(
          '.property-key').html(key.replace(/\_/g, ' '))
      $('div' + selection_string + ' div.file-property:last').find('.property-value').html(value)
    }
  }


  // click listener to change content for navigation tabs.
  $('ul.nav li a.nav-link').click(function()
  {
    var target_id = $(this).attr('href')

    $('div.tab-pane').addClass('active')
    $('div.tab-pane.process-tab').removeClass('active')
    $('div' + target_id).addClass('active') 
  })

  // click listener to emulate navigation tab link.
  $('.next-step-link').click(function()
  {
    var target_id = $(this).attr('target')
    var ajax_data = {
      'mediainfo': $('#mediainfo').val(),
      'avscript': $('#avscript').val(),
    }

    console.log(ajax_data)

    $.ajax({
      type: "POST",
      url: "/ajax/metadata",
      contentType: "application/json; charset=utf-8",
      dataType : "json",
      data: JSON.stringify(ajax_data),
      
      success: function(result) {
        $('ul.nav li a[href="' + target_id + '"]').trigger("click")

        details = result.general_details[0]
        populateDetails('#general_details', details)

        tracks = result.video_details
        for (i = 0; i < tracks.length; i++)
        {
          track_details = tracks[i]
          populateDetails('#video_details', track_details)
        }

        tracks = result.audio_details
        for (i = 0; i < tracks.length; i++)
        {
          track_details = tracks[i]
          populateDetails('#audio_details', track_details)
        }

        tracks = result.subtitle_details
        for (i = 0; i < tracks.length; i++)
        {
          track_details = tracks[i]
          populateDetails('#subtitle_details', track_details)
        }

        tracks = result.menu_details
        for (i = 0; i < tracks.length; i++)
        {
          track_details = tracks[i]
          populateDetails('#menu_details', track_details)
        }
      
        // $('div#general-details div.file-property').removeClass('m--hide')
      },

      error: function(result) {
        alert('error');
      }
    });
  })

});