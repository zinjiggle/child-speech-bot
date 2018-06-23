from flask import Flask, request, send_from_directory


app = Flask(__name__, static_url_path='')


@app.route("/")
def root():
  return send_from_directory('', 'index.html')


@app.route('/app/<path:path>')
@app.route('/js/<path:path>')
@app.route('/bootstrap/<path:path>')
@app.route('/jquery/<path:path>')
def send_static(path):
  return send_from_directory('static', request.path.lstrip('/'))
