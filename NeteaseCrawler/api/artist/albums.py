import requests

__all__ = ["get_artist_details_and_top_albums_by_artist_id"]


def get_artist_details_and_top_albums_by_artist_id(artist_id: int) -> dict:
    url = "http://music.163.com/api/artist/albums/{artist_id}".format(artist_id=artist_id)
    headers = {
        'Referer': 'http://music.163.com',
    }
    return requests.get(url=url, headers=headers).json()


def test():
    from pprint import pprint
    r = get_artist_details_and_top_albums_by_artist_id(19780)
    pprint(r)
    assert r["artist"]["id"] == 19780
    assert r["artist"]["name"] == "Halozy"
    print(len(r["hotAlbums"]))


if __name__ == '__main__':
    test()
