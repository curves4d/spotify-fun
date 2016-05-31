import sys
import spotify
import os
import time

# Setting up configuration and getting a logged in session
session = spotify.Session()
username = os.getenv('SPOTIFY_USER')
password = os.getenv('SPOTIFY_PASS')
session.login(username, password)

while session.connection.state is not spotify.ConnectionState.LOGGED_IN:
    time.sleep(1)
    session.process_events()
print session.connection.state
print "Setup done. Logged in"
# Setup done

def gen_load(obj):
    while not obj.is_loaded:
        try:
            obj.load()
        except:
            pass

def basic_playlist_stats(query):
    '''
    This function takes a search query and generates a frequency distribution
    of the songs and artists from those playlists
    '''
    search = spotify.Search(session, query)
    gen_load(search)

    # Getting the playlists from the search result
    playlists = [session.get_playlist(i.uri) for i in search.playlists]
    map(gen_load, playlists)
    for i in playlists:
        print i

    songs = {}
    artists = {}
    # Get the tracks from playlists
    for playlist in playlists:
        print "Processing playlist {0:20} with {1} tracks".format(playlist.owner, len(playlist.tracks))
        sys.stdout.flush()
        map(gen_load, playlist.tracks)
        for track in playlist.tracks:
            # print track.name
            try:
                dict_key = track.name.decode(encoding='utf-8', errors='ignore')
                dict_key_artist = track.artists[0].load().name.decode(encoding='utf-8', errors='ignore')
                artists[dict_key_artist] = artists.get(dict_key_artist, 0) + 1
                songs[dict_key] = songs.get(dict_key, 0) + 1
            except:
                continue

    print "All done"
    return songs,artists

def print_dict(d):
    d = sorted(d.items(), key=lambda x: x[1])
    for i in d:
        print "{0:5}\t{1}".format(i[1],i[0])

if __name__ == '__main__':
    basic_playlist_stats('rap classics')


