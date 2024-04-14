import yt_dlp
import ffmpeg
from flask import Flask, request, send_file
from flask_cors import CORS
import os
import requests

# ffmpegのダウンロード
ffmpeg_url = "https://apis.caymankun.f5.si/bin/ffmpeg"
ffmpeg_path = "/tmp/ffmpeg"

def download_ffmpeg(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        return False

# ダウンロードしてパスを追加
if download_ffmpeg(ffmpeg_url, ffmpeg_path):
    os.environ['PATH'] += os.pathsep + os.path.dirname(ffmpeg_path)

app = Flask(__name__)
CORS(app)

@app.route('/v', methods=['GET'])
def download_video():
    url = request.args.get('url')
    if url:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': '/tmp/%(title)s-%(id)s.%(ext)s',
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
            'format': 'bestaudio',
            'outtmpl': '/tmp/%(title)s-%(id)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # ダウンロードした音声のパスを取得
            audio_path = ydl.prepare_filename(info)
            # 音声をMP3形式に変換
            output_path = audio_path.replace('.m4a', '.mp3')
            ffmpeg.input(audio_path).output(output_path).run()
            return send_file(output_path, as_attachment=True)
    else:
        return 'URL parameter is required', 400

if __name__ == '__main__':
    app.run()
