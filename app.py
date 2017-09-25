from flask import Flask 
app = Flask(__name__)

@app.route('/')
def index():
  return 'Hello World!'


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

