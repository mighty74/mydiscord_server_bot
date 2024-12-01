from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is a Flask application accessible within the same network!"

@app.route('/now_time')
def now_time():
    return render_template('time.html')

@app.route('/music')
def music_truck():
    # musicディレクトリ内のMP3ファイルのリストを取得
    music_dir = 'music'
    tracks = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
    return render_template('music.html', tracks=tracks)

@app.route('/music/<filename>')
def music(filename):
    return send_from_directory('music', filename)



if __name__ == '__main__':
    # 0.0.0.0を使ってネットワーク内の他のデバイスからアクセス可能にする
    app.run(host='0.0.0.0', port=5000)


# 4060device  http://192.168.0.175:5000