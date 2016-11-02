from .albums import *
import requests

__all__ = ["get_artist_details_and_top_hot_songs_by_artist_id", "get_artist_details_and_top_albums_by_artist_id"]


def get_artist_details_and_top_hot_songs_by_artist_id(artist_id: int) -> dict:
    url = "http://music.163.com/api/artist/{artist_id}".format(artist_id=artist_id)
    headers = {
        'Referer': 'http://music.163.com',
    }
    return requests.get(url=url, headers=headers).json()


def test():
    from pprint import pprint
    r = get_artist_details_and_top_hot_songs_by_artist_id(19780)
    pprint(r)
    assert r["artist"]["id"] == 19780
    assert r["artist"]["name"] == "Halozy"


if __name__ == '__main__':
    test()
