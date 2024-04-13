import yt_dlp
import ffmpeg
from flask import Flask, request, jsonify
import flask-cors

app = Flask(__name__)
CORS(app)

@app.route('/v', methods=['GET'])
def download_video():
    url = request.args.get('url')
    if url:
        ydl_opts = {
            'format': 'best',
            'embed_thumbnail': True,
            'postprocessors': [{
                'key': 'EmbedThumbnail',
                'ffmpeg_o': '-c:v mjpeg -vf crop="\'if(gt(ih,iw),iw,ih)\':\'if(gt(iw,ih),ih,iw)\'"'
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            if 'url' in result:
                media_url = result['url']
                return send_file(media_url, as_attachment=True)
            else:
                return 'URL not found in result', 500
    else:
        return 'URL parameter is required', 400

@app.route('/a', methods=['GET'])
def download_audio():
    url = request.args.get('url')
    if url:
        ydl_opts = {
            'format': 'bestaudio',
            'embed_thumbnail': True,
            'postprocessors': [{
                'key': 'EmbedThumbnail',
                'ffmpeg_o': '-c:v mjpeg -vf crop="\'if(gt(ih,iw),iw,ih)\':\'if(gt(iw,ih),ih,iw)\'"'
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            if 'url' in result:
                media_url = result['url']
                return send_file(media_url, as_attachment=True)
            else:
                return 'URL not found in result', 500
    else:
        return 'URL parameter is required', 400

if __name__ == '__main__':
    app.run()
