import os
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask import send_from_directory
from parsers import MediaParser
from parsers import AvsParser


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'd:/temp'

@app.route('/static/metronic_v5.0.2/metronic_v5.0.2/theme/dist/html/default')
def default():
  # return send_from_directory(app.config['UPLOAD_FOLDER'])
  return None

@app.route('/static/metronic_v5.0.2/metronic_v5.0.2/theme/dist/html/demo2')
def demo2():
  # return send_from_directory(app.config['UPLOAD_FOLDER'])
  return None

@app.route('/static/styles')
def styles():
  return None

@app.route('/static/scripts')
def scripts():
  return None

@app.route('/')
def index():
  return render_template('site_specific/index.html')


@app.route('/encode/video')
def video_command():
  return 'Video Command Here.'


@app.route('/encode/audio')
def audio_command():
  return 'Audio Command Here.'


@app.route('/extract/subtitle')
def sub_extract_command():
  return 'Sub-Extraction Command Here.'


@app.route('/extract/video')
def video_extract_command():
  return 'Video-Extraction Command Here.'


@app.route('/extract/audio')
def audio_extract_commmand():
  return 'Audio-Extraction Command Here.'


@app.route('/info/ffmpeg')
def ffmpeg_info():
  return 'ffmpeg info Here.'


@app.route('/info/x264')
def x264_info():
  return 'X264 info here.'


@app.route('/info/x265')
def x265_info():
  return 'X265 info here.'


@app.route('/info/libopus')
def libopus_info():
  return 'libopus info here.'


@app.route('/info/libfdk_aac')
def libfdk_info():
  return 'libfdk_aac info here.'


@app.route('/merge/mkvmerge')
def mkvmerge_command():
  return 'mkvmerge command here.'


@app.route('/ajax/metadata', methods=["GET", "POST"])
def ajax_parse_metadata():

  xml_string = request.json['mediainfo']
  avs_string = request.json['avscript']

  if not xml_string:
    pass

  media_parser = MediaParser(xml_string)
  avs_parser = AvsParser(avs_string)

  data = dict()
  data['general_details'] = media_parser.get_general_details(media_parser.mediainfo)
  data['video_details'] = media_parser.get_video_details(media_parser.mediainfo)
  data['audio_details'] = media_parser.get_audio_details(media_parser.mediainfo)
  data['subtitle_details'] = media_parser.get_subtitle_details(media_parser.mediainfo)
  data['menu_details'] = media_parser.get_menu_details(media_parser.mediainfo)

  return jsonify(data)

