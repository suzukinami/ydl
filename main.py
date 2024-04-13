import os
import mimetypes
from flask import Flask, request, jsonify, send_file
from subprocess import run

app = Flask(__name__)

# ファイルをダウンロードして指定されたパスに保存する関数
def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        return False

# yt-dlpをダウンロードして実行
yt_dlp_url = "https://apis.caymankun.f5.si/cgi-bin/yt-dlp"
yt_dlp_path = "/tmp/yt-dlp"
if download_file(yt_dlp_url, yt_dlp_path):
    os.chmod(yt_dlp_path, 0o755)  # ダウンロードしたファイルを実行可能にする

# ffmpegをダウンロードして実行
ffmpeg_url = "https://apis.caymankun.f5.si/cgi-bin/ffmpeg"
ffmpeg_path = "/tmp/ffmpeg"
if download_file(ffmpeg_url, ffmpeg_path):
    os.chmod(ffmpeg_path, 0o755)  # ダウンロードしたファイルを実行可能にする

@app.route('/v', methods=['GET'])
def download_video():
    video_id = request.args.get('id')
    if video_id:
        output_path = f"/tmp/%(title)s-%(id)s.%(ext)s"
        run([yt_dlp_path, "--ffmpeg-location" , ffmpeg_path , "-o", output_path, f"https://www.youtube.com/watch?v={video_id}"])
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
        run([yt_dlp_path, "-x", "--audio-format", "mp3", "--ffmpeg-location" , ffmpeg_path , "-o", output_path, f"https://www.youtube.com/watch?v={video_id}"])
        if os.path.exists(output_path):
            mime_type, _ = mimetypes.guess_type(output_path)
            return send_file(output_path, mimetype=mime_type, as_attachment=True)
        else:
            return jsonify({"error": "Failed to download audio"}), 500
    else:
        return jsonify({"error": "Video ID is required"}), 400

if __name__ == '__main__':
    app.run()
