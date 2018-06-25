import io
import os

# Imports the Google Cloud client library
from flask import Flask, request, send_from_directory
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


app = Flask(__name__, static_url_path='')

CONFIG = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
    language_code='en-US')
CLIENT = speech.SpeechClient()


@app.route('/')
def root():
  return send_from_directory('', 'index.html')


@app.route('/upload', methods=['POST'])
def inputSoundHandler():
  audio_file = request.files['data']
  content = audio_file.read()
  audio = types.RecognitionAudio(content=content)
  response = CLIENT.recognize(CONFIG, audio)
  print(response)
  return response.results[0].alternatives[0].transcript


@app.route('/app/<path:path>')
@app.route('/js/<path:path>')
@app.route('/bootstrap/<path:path>')
@app.route('/jquery/<path:path>')
def send_static(path):
  return send_from_directory('static', request.path.lstrip('/'))
