from flask import Flask, request, render_template, jsonify
import yt_dlp
import threading

app = Flask(__name__)

download_status = {
    'status': '',
    'title': ''
}

def download_video_thread(url, format):
    global download_status
    download_status['status'] = 'in_progress'
    try:
        ydl_opts = {
            'format': 'best' if format == 'video' else 'bestaudio',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if format == 'audio' else []
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            download_status['title'] = info.get('title', 'video')
        download_status['status'] = 'completed' if format == 'video' else 'audio_completed'
    except Exception as e:
        download_status['status'] = 'error_but_downloaded'
        download_status['title'] = info.get('title', 'video')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    thread = threading.Thread(target=download_video_thread, args=(url, 'video'))
    thread.start()
    return jsonify({'status': 'Download started'})

@app.route('/download_audio', methods=['POST'])
def download_audio():
    url = request.form['url']
    thread = threading.Thread(target=download_video_thread, args=(url, 'audio'))
    thread.start()
    return jsonify({'status': 'Download started'})

@app.route('/status')
def download_status_check():
    return jsonify(download_status)

if __name__ == '__main__':
    app.run(debug=True)
