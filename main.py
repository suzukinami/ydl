import yt_dlp
import ffmpeg
from flask import Flask, request, send_file
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

@app.route('/v', methods=['GET'])
def download_video():
    url = request.args.get('url')
    if url:
        ydl_opts = {
            'f': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'o': '/tmp/%(title)s-[%(id)s].%(ext)s',
            'ffmpeg-location': '/tmp/ffmpeg',
            
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # ダウンロードした動画のパスを取得
            video_path = ydl.prepare_filename(info)
            return send_file(video_path, as_attachment=True)
    else:
        return 'URL parameter is required', 400

@app.route('/a', methods=['GET'])
def download_audio():
    url = request.args.get('url')
    if url:
        ydl_opts = {
            'f': 'bestaudio[ext=m4a]',
            'o': '/tmp/%(title)s-[%(id)s].%(ext)s',
            'ffmpeg-location': '/tmp/ffmpeg',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # ダウンロードした動画のパスを取得
            video_path = ydl.prepare_filename(info)
            return send_file(video_path, as_attachment=True)
    else:
        return 'URL parameter is required', 400

if __name__ == '__main__':
    app.run()
