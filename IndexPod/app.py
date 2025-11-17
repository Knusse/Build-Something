import requests
import base64
import sys
from flask_caching import Cache
from flask import Flask, render_template, jsonify, Response
# from kubernetes import client, config

#DB_DOMAIN = "http://database:7500" # Internal kube db domain name & port
DB_DOMAIN = "http://localhost:7500" # Localhost for testing

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 120})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/<word>')
@cache.cached(timeout=120)
def search(word):
    url = DB_DOMAIN + f"/video/{word}/links"
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return "Search not found", 404
    
@app.route('/video/<string:video_name>/thumbnail', methods=['GET'])
@cache.cached(timeout=120)
def fetch_thumbnail(video_name):
    url = f"{DB_DOMAIN}/video/{video_name}/thumbnail"
    response = requests.get(url, timeout=5)
    data = response.json()
    img_bytes = base64.b64decode(data["thumbnail_data"])
    return Response(img_bytes, mimetype='image/png')
if __name__ == "__main__":
    if len(sys.argv) > 1: # Set domain
        DB_DOMAIN = sys.argv[1]
    app.run(debug=True, host="0.0.0.0", port=7700)