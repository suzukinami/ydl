import os
import mimetypes
from flask import Flask, request, jsonify, send_file
from subprocess import run
import yt-dlp

app = Flask(__name__)

@app.route('/v', methods=['GET'])
def download_video():
    video_id = request.args.get('id')
    if video_id:
        output_path = f"/tmp/%(title)s-%(id)s.%(ext)s"
        run(["yt-dlp", "--ffmpeg-location" , "https://apis.caymankun.f5.si/cgi-bin/ffmpeg" , "-o", output_path, f"https://www.youtube.com/watch?v={video_id}"])
        if os.path.exists(output_path):
            mime_type, _ = mimetypes.guess_type(output_path)
            return send_file(output_path, mimetype=mime_type, as_attachment=True)
        else:
            return jsonify({"error": "Failed to download video"}), 500
    else:
        return jsonify({"error": "Video ID is required"}), 400

@app.route('/a', methods=['GET'])
def download_audio():
    video_id = request.args.get('id')
    if video_id:
        output_path = f"/tmp/%(title)s-%(id)s.%(ext)s"
        run(["yt-dlp", "-x", "--audio-format", "mp3", "--ffmpeg-location" , "https://apis.caymankun.f5.si/cgi-bin/ffmpeg" , "-o", output_path, f"https://www.youtube.com/watch?v={video_id}"])
        if os.path.exists(output_path):
            mime_type, _ = mimetypes.guess_type(output_path)
            return send_file(output_path, mimetype=mime_type, as_attachment=True)
        else:
            return jsonify({"error": "Failed to download audio"}), 500
    else:
        return jsonify({"error": "Video ID is required"}), 400

if __name__ == '__main__':
    app.run()
