from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import zipfile

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    songs = []

    if request.method == "POST":
        url = request.form.get("url")

        # 🔥 YAHI PASTE KARNA HAI
        ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
    'noplaylist': False,
    'quiet': True,
    'js_runtimes': {'node': {}},  # ✅ FIXED
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
}

        # 👇 ye same rehna hai
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            if 'entries' in info:
                for entry in info['entries']:
                    if entry:
                        songs.append(entry['title'] + ".mp3")
            else:
                songs.append(info['title'] + ".mp3")

    return render_template("index.html", songs=songs)


@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)


@app.route("/download_all")
def download_all():
    zip_path = os.path.join(DOWNLOAD_FOLDER, "songs.zip")

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in os.listdir(DOWNLOAD_FOLDER):
            if file.endswith(".mp3"):
                zipf.write(os.path.join(DOWNLOAD_FOLDER, file), file)

    return send_file(zip_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)