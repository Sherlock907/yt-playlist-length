from flask import Flask, render_template, request,flash, Markup
from pytube import Playlist, YouTube


# https://youtu.be/P4F3PzCMrtk?list=PLqXS1b2lRpYTC04DA9J8hta6oYEKOd91N
def secondsTo(n):
    n = int(n)
    if n < 60:
        return f"{n} Sekunden"
    if n >= 60:
        min,sec  = n//60, n%60
        if n < 60*60:
            return f"{min} Minuten, {sec} Sekunden"
    if min >= 60:
        hours = min//60
        min = min %60
        return f"{hours}:{min}:{sec}"

app = Flask(__name__)
app.secret_key = "LMJlcau05qOOHZU3TOCXpofLa"


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        try:
            if str(request.form['yt-link']).lower() == "bautz":
                flash("Sie suchen also nach dem großen Lebautzski")
                flash("Copy Playlist link here:")
                return render_template('index.html')
            p = Playlist(request.form['yt-link'])
            playlist_duration = 0


            flash(Markup("Playlist: <a href='https://www.youtube.com/playlist?list=" + p.playlist_id + "'>" + p.title + "</a>"))
            for url in p:
                playlist_duration += YouTube(url).length
            flash("Total Playlist duration:\n" + secondsTo(playlist_duration))
            flash("Duration at 1.25x speed:\n" + secondsTo(playlist_duration // 1.25))
            flash("Duration at 1.5 speed:\n" + secondsTo(playlist_duration // 1.5))
            flash("Total Playlist Views: " + str(p.views))
            flash("Number of Videos: " + str(p.length))
            flash("Last updated: "+ str(p.last_updated))
            return render_template('yt-playlist.html')
        except:
            flash("Whoops!.. Something went wrong.")
            flash("Copy Playlist link here:")
            return render_template('index.html')

    flash("Copy Playlist link here:")
    return render_template('index.html')


"""@app.route("/yt-playlist", methods=["POST", "GET"])
def greet():
    flash("Hi " + str(request.form['name_input']) +", great to see you !")
    return render_template('index.html')"""

if __name__ == '__main__':
    app.run(port=1337, debug=False)