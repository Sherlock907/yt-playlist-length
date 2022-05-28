from flask import Flask, render_template, request,flash, Markup
from pytube import Playlist, YouTube

def secondsTo(n):
    n = int(n)
    if n < 60:
        if n < 10:
            n = "0" + str(n)
        return f"{n} Seconds"
    if n >= 60:
        min,sec  = n//60, n%60
        if min < 10:
            min = "0" + str(min)
        if sec < 10:
            sec = "0" + str(sec)
        if n < 60*60:
            return f"{min} Minutes, {sec} Seconds"
    if min >= 60:
        hours = min//60
        min = min %60
        return f"{hours}:{min}:{sec}"

app = Flask(__name__)
app.secret_key = "SpoilerAlert"


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        try:
            p = Playlist(request.form['yt-link'])
            playlist_duration = 0
            flash(Markup("<a href='https://www.youtube.com/playlist?list=" + p.playlist_id + "'>" + p.title + "</a>"))
            for url in p:
                playlist_duration += YouTube(url).length
            flash("Total Playlist duration:\n" + secondsTo(playlist_duration))
            flash("Number of Videos: " + str(p.length))
            flash("Last updated: "+ str(p.last_updated))
            return render_template('yt-playlist.html')
        except:
            flash("Whoops!.. Something went wrong.")
            flash("Copy Playlist link here:")
            return render_template('index.html')

    flash("Copy Playlist link here:")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=1337, debug=False)