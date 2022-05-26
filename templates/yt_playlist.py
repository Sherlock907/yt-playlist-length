from pytube import Playlist, YouTube

# ytPlaylist = "https://www.youtube.com/watch?v=P4F3PzCMrtk&list=PLqXS1b2lRpYTC04DA9J8hta6oYEKOd91N"
ytPlaylist ="https://youtu.be/P4F3PzCMrtk?list=PLqXS1b2lRpYTC04DA9J8hta6oYEKOd91N"
# check for youtube /youtu.be
# search for list= + 34 zeichen
ytPlaylist = "www.youtube.com/watch?v=P4F3PzCMrtk&"

p = Playlist(ytPlaylist)

exit()


def secondsTo(n):
    if n < 60:
        return f"{n} Sekunden"
    if n >= 60:
        min,sec  = n//60, n%60
        if n < 60*60:
            return f"{min} Minuten, {sec} Sekunden"
    if min >= 60:
        hours = min//60
        min = min %60
        return f"{hours} Stunden, {min} Minuten, {sec} Sekunden"


p = Playlist(ytPlaylist)
playlist_duration = 0 # in seconds
print(f"""Playlist Title: {p.title}
Numbers of Videos: {p.length}
Last updated: {p.last_updated}
Playlist-link: https://www.youtube.com/playlist?list={p.playlist_id}
Total Playlist Views: {p.views}""")

for url in p:
    playlist_duration += YouTube(url).length

print("Total Playlist duration: ",secondsTo(playlist_duration))
print("Total Playlist duration at 1.25x speed: ",secondsTo(playlist_duration//1.25))
print("Total Playlist duration at 1.5 speed: ",secondsTo(playlist_duration//1.5))


# Youtube() Objekte: channel_id, channel_url, video descriptions,publish-dates (published between), rating-<avg,title->übersicht,views-1-bis ende
# Playlist Objekte: number of videos, last_updated, playlist_url, title