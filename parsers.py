from pymediainfo import MediaInfo

class MediaParser(object):

  def __init__(self, xml_string):
    self.mediainfo = MediaInfo(xml_string)
    self.metadata = self.mediainfo.to_data()
  

  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  def get_general_details(self, mediainfo):

    general_details = list()
    for track in mediainfo.tracks:
      if 'general' in track.track_type.lower():
        track_details = dict()
        track_details['file_name'] = track.file_name
        track_details['file_extension'] = track.file_extension
        track_details['file_size'] = track.file_size
        track_details['codec'] = track.codec
        track_details['duration'] = float(track.duration)
        track_details['stream_size'] = track.stream_size
        track_details['attachments'] = track.attachments
        
        general_details.append(track_details)

    return general_details


  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  def get_video_details(self, mediainfo):

    vid_details = list()
    for track in mediainfo.tracks:
      if 'video' in track.track_type.lower():
        track_details = dict()
        track_details['_id'] = track.track_id
        track_details['codec'] = track.codec
        track_details['frame_rate_mode'] = track.frame_rate_mode
        track_details['frame_rate'] = float(track.frame_rate)
        track_details['resolution'] = (track.width, track.height)
        track_details['duration'] = float(track.duration)
        track_details['bit_rate'] = float(track.bit_rate)
        track_details['bit_depth'] = track.bit_depth
        track_details['stream_size'] = track.stream_size
        track_details['display_aspect_ratio'] = float(track.display_aspect_ratio)
        track_details['title'] = track.title
        track_details['language'] = track.language
        track_details['default'] = track.default
        track_details['forced'] = track.forced
        
        vid_details.append(track_details)

    return vid_details


  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  def get_audio_details(self, mediainfo):

    aud_details = list()
    
    for track in mediainfo.tracks:
      if 'audio' in track.track_type.lower():
        track_details = dict()
        track_details['_id'] = track.track_id
        track_details['codec'] = track.codec
        track_details['duration'] = float(track.duration)
        track_details['bit_rate'] = track.bit_rate
        track_details['channels'] = track.channel_s
        track_details['sampling_rate'] = track.sampling_rate
        track_details['stream_size'] = track.stream_size
        track_details['title'] = track.title
        track_details['language'] = track.language
        track_details['default'] = track.default
        track_details['forced'] = track.forced

        aud_details.append(track_details)

    return aud_details


  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  def get_subtitle_details(self, mediainfo):

    aud_details = list()
    
    for track in mediainfo.tracks:
      if 'text' in track.track_type.lower():
        track_details = dict()
        track_details['_id'] = track.track_id
        track_details['codec'] = track.codec
        track_details['duration'] = float(track.duration)
        track_details['bit_rate'] = track.bit_rate
        track_details['stream_size'] = track.stream_size
        track_details['title'] = track.title
        track_details['language'] = track.language
        track_details['default'] = track.default
        track_details['forced'] = track.forced

        aud_details.append(track_details)

    return aud_details


  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  def get_menu_details(self, mediainfo):

    menu_details = list()
    for track in mediainfo.tracks:
      if 'menu' in track.track_type.lower():
        menu_data = track.to_data()
        menu = list()
        for key in menu_data:
          if key.replace('_', str()).isdigit():
            menu.append((key.replace('_', ':'), menu_data[key]))

        menu_details.append(menu)

    return menu_details

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

class AvsParser(object):

  def __init__(self, avs_string):
    
    self.avs_content = [line for line in avs_string.split('\n')
      if line and not line.startswith('#') or line.startswith('##>') 
      or line.startswith('##!!')]

    print(self.avs_content)


  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  def parse_avs_chapters(self, avs_content):
  
    avs_chap_string = ''.join([x.strip('##!!') for x in avs_content 
      if x.startswith('##!!') and '>' in x and '<' in x])

    if not avs_chap_string:
      return None

    filtered_chaps = [x.strip('>').strip('<').strip(' ').strip('\n') 
      for x in avs_chap_string.split(',')] if avs_chap_string else None

    avs_chapters = dict()
    avs_chapters['names'] = list(); avs_chapters['frames'] = list()

    for chapter in filtered_chaps:
      name = chapter.split('[')[0]
      start = int(chapter.split('[')[1].split(':')[0].strip(' '))
      end = int(chapter.split('[')[1].split(':')[1].split(']')[0].strip(' '))
      avs_chapters['names'].append(name)
      avs_chapters['frames'].append((start, end))

    return avs_chapters

  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  def get_custom_commands(self, avs_content):

    commands_dict = dict()
    avsfile = open(input_file)
    file_content = avsfile.readlines()
    avsfile.close()

    commands = ','.join([x.strip('##>') for x in avs_content if x.startswith('##>')]).split(',')
    
    for command in commands:
      if not command or len(command) < 3:
        continue
    
      option, value = command.split('=')
      commands_dict[option] = value.strip('\r').strip('\n')

    avs_chapters = parse_avs_chapters(avs_content)
    return commands_dict
