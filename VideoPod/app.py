import requests
import time
import sys
from flask import Flask, Response

DB_DOMAIN = "http://localhost:7500"
app = Flask(__name__)
video_files = {}

@app.route("/playvideo/<string:video_name>")
def get_video(video_name):
    if video_name not in video_files.keys():
        return "Video not found", 404
    video_bytes = video_files[video_name]
    return Response(video_bytes, mimetype="video/mp4")

def load_videos():
    global video_files
    url = f"{DB_DOMAIN}/video/%2A/links"
    response_data = None
    while True: # Get all video names
        response = requests.get(url)
        if response.status_code == 200:
            response_data = response.json()
            break
        print(f"{url} | Server not responding, retrying...")
        time.sleep(1)

    for video_info in response_data: # Using all video names fetch corresponding video files
        name = video_info["name"].lower()
        url = f"{DB_DOMAIN}/video/{name}/video"
        while True:
            response = requests.get(url)
            if response.status_code == 200:
                video_files[name] = response.content
                print(f"Fetched video: {name}")
                break
            print(f"{url} | DB Server not responding, retrying...")
            time.sleep(1)
if __name__ == "__main__":
    if len(sys.argv) > 1: # Set domain/ip
        DB_DOMAIN = sys.argv[1]
    load_videos()
    app.run(debug=True, host="0.0.0.0", port=7600)