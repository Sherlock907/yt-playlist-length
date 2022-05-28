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
app.secret_key = "LMJlcau05qOOHZU3TOCXpofLa"


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        try:
            if (x:=str(request.form['yt-link']).lower()) == "bautz" or sorted(x) == sorted("bautz") :
                flash("Sie suchen also nach dem großen Lebautzski")
                flash(Markup("Hier werden Sie fündig:  <a href='https://youtu.be/9cK3QYZ7XaA'>The Big Lebautzski</a>"))
                return render_template('index.html')
            elif x == "mariya":
                flash(Markup("<h5 style='padding-bottom: 15px;text-decoration:underline;'>Thank you for your insightful tutorials, Mariya.</h5>"))
                return render_template('index.html')
            elif sorted(x) == sorted("mariya"):
                flash("Having a hard time writing your own name? - No Problem.")
                flash(Markup('<script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/2.0.2/anime.min.js"></script>'))
                flash(Markup('''<h1 class="ml2">It's Mariya</h1>'''))
                flash(Markup('''<script>var textWrapper=document.querySelector('.ml2');textWrapper.innerHTML=textWrapper.textContent.replace(/\S/g,"<span class='letter'>$&</span>");anime.timeline({loop:true}).add({targets:'.ml2 .letter',opacity:[0,0],translateZ:0,easing:"easeOutExpo",duration:1750,delay:(el,i)=>70*i}).add({targets:'.ml2 .letter',scale:[4,1],opacity:[0,1],translateZ:0,easing:"easeOutExpo",duration:2550,delay:(el,i)=>700*i}).add({targets:'.ml2',opacity:0,duration:1000,easing:"easeOutExpo",delay:1000});</script>'''))
                return render_template('index.html')
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