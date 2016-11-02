import requests

__all__ = ["get_album_details_by_album_id"]


def get_album_details_by_album_id(album_id: int) -> dict:
    url = "http://music.163.com/api/album/{album_id}".format(album_id=album_id)
    headers = {
        'Referer': 'http://music.163.com',
    }
    r = requests.get(url=url, headers=headers).json()
    return r["album"] if r["code"] == 200 else None


def test():
    from pprint import pprint
    r = get_album_details_by_album_id(2786226)
    pprint(r)
    assert r["album"]["company"] == "ワーナー・ホーム・ビデオ"


if __name__ == '__main__':
    test()
