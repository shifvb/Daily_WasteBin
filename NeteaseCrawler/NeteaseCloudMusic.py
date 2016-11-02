import os
from api import *
from pprint import pprint

__all__ = ["NeteaseCloudMusic", "NeteaseCloudMusicUtils"]

__version__ = (0, 0, 1)

SEARCH_TYPE = {
    "songs": 1,
    "albums": 10,
    "artists": 100,
    "playlists": 1000,
    "userprofiles": 1002,
    "mvs": 1004,
    "lyric": 1006,
    "djprograms": 1008,
    "djRadios": 1009,
}

SONG_QUALITIES = ["hMusic", "nMusic", "lMucic", "bMusic"]


class NeteaseCloudMusic(object):
    @property
    def api(self):
        return api

    @classmethod
    def search_songs(cls, song_name: str, total_songs_limit=10, song_offset=0) -> dict:
        """return result of searched songs"""
        return generic_search(song_name, SEARCH_TYPE["songs"],
                              total_songs_limit, song_offset)

    @classmethod
    def search_albums(cls, album_name: str, total_albums_limit=10, album_offset=0) -> dict:
        """return result of searched albums"""
        return generic_search(album_name, SEARCH_TYPE["albums"],
                              total_albums_limit, album_offset)

    @classmethod
    def search_artists(cls, artist_name: str, total_artists_limit=10, artist_offset=0) -> dict:
        """return result of searched artists"""
        return generic_search(artist_name, SEARCH_TYPE["artists"],
                              total_artists_limit, artist_offset)

    # todo: query playlists details
    @classmethod
    def search_playlists(cls, playlist_name, total_playlists_limit=10, playlist_offset=0) -> dict:
        """return result of searched playlists"""
        return generic_search(playlist_name, SEARCH_TYPE["playlists"],
                              total_playlists_limit, playlist_offset)

    # todo : query user's playlists
    # followeds
    # 10
    # playlistBeSubscribedCount
    # 0
    # playlistCount
    # 25
    # eventCount
    # 0
    # follows
    # 26
    @classmethod
    def search_userprofiles(cls, userprofile_name, total_userprofile_limit=10, userprofile_offset=0) -> dict:
        """return result of searched user profiles"""
        return generic_search(userprofile_name, SEARCH_TYPE["userprofiles"],
                              total_userprofile_limit, userprofile_offset)

    # todo: query movie's details
    @classmethod
    def search_movies(cls, movie_name, total_movies_limit=10, movie_offset=0) -> dict:
        """return result of searched movies"""
        return generic_search(movie_name, SEARCH_TYPE["mvs"],
                              total_movies_limit, movie_offset)

    @classmethod
    def search_lyrics(cls, lyric_str, total_songs_limit=10, song_offset=10) -> dict:
        """return result of lyric searched songs"""
        return generic_search(lyric_str, SEARCH_TYPE["lyric"],
                              total_songs_limit, song_offset)

    @classmethod
    def search_djprograms(cls, djprogram_str, total_djprograms_limit=10, djprogram_offset=0) -> dict:
        """return result of searched djprograms"""
        return generic_search(djprogram_str, SEARCH_TYPE["djprograms"],
                              total_djprograms_limit, djprogram_offset)

    @classmethod
    def search_djradios(cls, djradio_str, total_djradios_limit=10, djradio_offset=0) -> dict:
        """return result of searched djradios"""
        return generic_search(djradio_str, SEARCH_TYPE["djRadios"],
                              total_djradios_limit, djradio_offset)

    @classmethod
    def query_song(cls, song_id: int) -> dict:
        """query the detail of song by song id"""
        return get_song_detail_by_song_id(song_id)

    @classmethod
    def query_album(cls, album_id: int) -> dict:
        """query the detail of album by album id"""
        return get_album_details_by_album_id(album_id)

    @classmethod
    def query_artist(cls, artist_id: int) -> dict:
        """query the detail of artist by artist id"""
        return get_artist_details_and_top_hot_songs_by_artist_id(artist_id)["artist"]

    @classmethod
    def query_artist_top_songs(cls, artist_id) -> list:
        """query top songs of artist by aritst id"""
        return get_artist_details_and_top_hot_songs_by_artist_id(artist_id)["hotSongs"]

    @classmethod
    def query_artist_hot_albums(cls, artist_id) -> list:
        """query top albums of artist by artist id"""
        return get_artist_details_and_top_albums_by_artist_id(artist_id)["hotAlbums"]

    @classmethod
    def query_user_profile(cls, user_id: int) -> dict:
        """query user details"""
        return get_user_detail_from_user_id(user_id)

    @classmethod
    def download_song(cls, song_id: int, filepath="."):
        song_details = cls.query_song(song_id)
        song_name = song_details["name"]
        dfsid = song_details["hMusic"]["dfsId"]
        with open(os.path.join(filepath, song_name + ".mp3"), "wb") as f:
            f.write(download_song_by_dfsid(dfsid))


class NeteaseCloudMusicUtils(object):
    def __init__(self, ncm=None):
        if ncm is None:
            self._ncm = NeteaseCloudMusic()
        else:
            self._ncm = ncm

    def search_songs_interactive(self, song_name: str, total_songs_limit=10, song_offset=0):
        """like NeteaseCloudMusic.search_songs, but interactive, not return, show the name and id of song"""
        songs = self._ncm.search_songs(song_name, total_songs_limit, song_offset)["songs"]
        for index, song in enumerate(songs):
            print("{:^5} {} ".format(index, song["name"], song["id"]))
        index = int(input("Please input the index of song you want to query: "))
        print(songs[index]["id"])
