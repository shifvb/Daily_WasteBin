import requests

__all__ = ["get_song_detail_by_song_id"]


def get_song_detail_by_song_id(song_id: int) -> dict:
    url = "http://music.163.com/api/song/detail/?id={song_id}&ids=%5B{song_id}%5D".format(song_id=song_id)
    headers = {
        'Referer': 'http://music.163.com',
    }
    r = requests.get(url=url, headers=headers).json()
    return r["songs"][0] if len(r["songs"]) > 0 else None


def test():
    from pprint import pprint
    r = get_song_detail_by_song_id(789106)
    pprint(r)


if __name__ == '__main__':
    test()
