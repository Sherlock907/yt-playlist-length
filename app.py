from googleapiclient.discovery import build
from flask import Flask, render_template, request,flash, Markup
from pytube import Playlist, YouTube
import os



def getseconds(n):
    #decrypting the YT-API Timeformat
    n, temp, duration = n.replace("PT", ""), "", 0
    for c in n:
        if c.isnumeric():
            temp += c
            continue
        elif c == "H":
            duration += int(temp) * 60**2
            temp = ""
        elif c == "M":
            duration += int(temp) * 60
            temp = ""
        elif c == "S":
            duration += int(temp)
            temp = ""
    return duration

def secondsTo(n):
    n = int(n)
    if n < 60:
        return f"{n} Seconds"
    if n >= 60:
        min,sec  = n//60, n%60
        if n < 60*60:
            if min < 10:
                min = "0" + str(min)
            if sec < 10:
                sec = "0" + str(sec)
            return f"{min} Minutes, {sec} Seconds"
    if min >= 60:
        hours = min//60
        min = min %60
        if min < 10:
            min = "0" + str(min)
        if sec < 10:
            sec = "0" + str(sec)
        if hours >= 24:
            days = hours // 24
            hours = hours % 24
            if hours < 10:
                hours = "0" + str(hours)
            return f"{days}:{hours}:{min}:{sec}"
        else:
            return f"{hours}:{min}:{sec}"

def getlength(p):
    api_key = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    # get videoID with pytube as youtube API only gets you the first 50-100 IDs...
    vid_ids = [YouTube(url).video_id for url in p]

    # total duration, number of videos, divisor for 50 (youtubes api only allows to request information for 50 videos at once
    duration, vid_count, div = 0, len(vid_ids), len(vid_ids)//50

    # gets vid length from videos <50 or those which over lap 50/100
    # for example in a playlist with 103 videos, the code below gets the duration of video 101-103
    vid_request = youtube.videos().list(
        part="contentDetails",
        id=','.join(vid_ids[50 * div:50 * div + vid_count % 50])
    )
    vid_response = vid_request.execute()

    # adds the duration from the api response
    for item in vid_response ['items']:
        duration += getseconds(item['contentDetails']['duration'])


    # get videos from positions diviseable by 50 -> (0:50, 50:100, ..)
    for i in range(0,div):
        vid_request = youtube.videos().list(
            part="contentDetails",
            id=','.join(vid_ids[50*i:50*i+50])
        )
        vid_response = vid_request.execute()
        for item in vid_response['items']:
            duration += getseconds(item['contentDetails']['duration'])

    return secondsTo(duration)



app = Flask(__name__)
app.secret_key = "SpoilerAlert"


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        try:
            link = request.form['yt-link']
            p = Playlist(link)
            flash(Markup("<a href='https://www.youtube.com/playlist?list=" + p.playlist_id + "'>" + p.title + "</a>"))
            playlist_duration = getlength(p)
            flash("Total Playlist duration:\n" + playlist_duration)
            flash("Number of Videos: " + str(p.length))
            try:
                flash("Last updated: "+ str(p.last_updated))
            except:
                flash("Last updated: N/A")
            return render_template('yt-playlist.html')
        except:
            flash("Whoops!.. Something went wrong.")
            flash("Copy Playlist link here:")
            return render_template('index.html')

    flash("Copy Playlist link here:")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=1337, debug=False)