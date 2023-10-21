import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup


SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
USERNAME = os.getenv("SPOTIFY_USERNAME")


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt",
                                               username=USERNAME))
user_id = sp.current_user()['id']
date = input("Enter your date in the format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}"

request = requests.get(url=URL)
request.raise_for_status()
response = request.text


soup = BeautifulSoup(response, "lxml")
all_titles_list = soup.find_all(name="h3", id="title-of-a-story", class_="c-title")[6:-13:4]

all_song_titles = [{h3.text.strip()} for h3 in all_titles_list]
all_song_uris = []
year = date.split("-")[0]
for song in all_song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        all_song_uris.append(uri)
    except IndexError:
        pass

my_playlist = sp.user_playlist_create(user=user_id, name=f"{date} Top 100 Billboard songs Playlist", public=False)
sp.playlist_add_items(playlist_id=my_playlist["id"], items=all_song_uris)
