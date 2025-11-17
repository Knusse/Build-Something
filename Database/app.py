import sqlite3
import base64
from flask import Flask, Response, jsonify

app = Flask(__name__)
def insert_video(name, path_thumbnail, path_video):
    conn = sqlite3.connect('/storage/database.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO videos (name, path_thumbnail, path_video)
        VALUES (?, ?, ?)
        ''',
        (name, path_thumbnail, path_video)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return

def insert_placeholders():
    insert_video("duck", "storage/thumbnails/duck", "storage/videos/duck")
    insert_video("soldier", "storage/thumbnails/soldier", "storage/videos/soldier")
    insert_video("city", "storage/thumbnails/city", "storage/videos/city")

def initdb():
    conn = sqlite3.connect('/storage/database.db')
    cursor = conn.cursor()

    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY,
        name TEXT,
        path_thumbnail TEXT,
        path_video TEXT
    )
    '''
    )

    conn.commit()
    cursor.close()
    conn.close()
    return

# Get a video file / thumbnail
@app.route('/video/<string:video_name>/<string:resource>', methods=['GET'])
def request_video_resource(video_name, resource):
    conn = sqlite3.connect('/storage/database.db')
    cursor = conn.cursor()

    if resource == "video": # Returns the video file
        cursor.execute('SELECT path_video FROM videos WHERE name = ?', (video_name,))
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Video not found'}), 404
        path = row[0]
        cursor.close()
        conn.close()
        with open(path, "rb") as f:
            video_data = f.read()
        return Response(video_data, mimetype='video/mp4')
        
    elif resource == "thumbnail": # Returns the thumbnail
        cursor.execute('SELECT name, path_thumbnail FROM videos WHERE LOWER(name) = LOWER(?)', (video_name,))
        print("requesting: thumbnail for: ", video_name)
        row = cursor.fetchone()
        name_and_thumbnail = None
        cursor.close()
        conn.close()
        print("row: ", row)
        if not row:
            return jsonify({'error': 'Video not found'}), 404
        with open(row[1], "rb") as f:
            thumbnail_data = f.read()
            encoded_thumbnail = base64.b64encode(thumbnail_data).decode('utf-8')
            name_and_thumbnail = {
                "name": row[0], 
                "thumbnail_data": encoded_thumbnail
            }
        return jsonify(name_and_thumbnail)
    elif resource == "links": # Returns video- and thumbnail-links for each matching name
        if video_name == "*":
            video_name = ""
        cursor.execute('SELECT name FROM videos WHERE name LIKE ?', (f'{video_name}%',))
        rows = cursor.fetchall()
        links = []
        for row in rows:
            video_info = {
                "name": row[0],
                "thumbnail_link": f'/video/{row[0]}/thumbnail',
                "video_link": f'/playvideo/{row[0]}'
            }
            links.append(video_info)
        cursor.close()
        conn.close()
        return jsonify(links)
    else:
        return jsonify({'error': 'Resource type invalid'}), 404

if __name__ == "__main__":
    initdb()
    app.run(debug=True, host="0.0.0.0", port=7500)