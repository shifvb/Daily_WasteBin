import requests

__all__ = ["generic_search"]


def generic_search(p_name: str, p_type: int, total_p_limit=10, p_offset=0) -> dict:
    url = "http://music.163.com/api/search/get"
    headers = {
        "Referer": "http://music.163.com"
    }
    data = {
        "s": p_name,
        "type": p_type,
        "limit": total_p_limit,
        "offset": p_offset
    }
    r = requests.post(url=url, data=data, headers=headers).json()
    return r["result"] if r.get("code", -1) == 200 else None


def test():
    from pprint import pprint

    # test searching songs -> http://music.163.com/song?id=789106
    r = generic_search("Love Colors", 1)
    assert r["songs"][0]["id"] == 789106
    assert (r["songs"][0]["alias"][0] == "原曲：恋色マスタースパーク")

    # test searching albums -> http://music.163.com/album?id=2786226
    r = generic_search("accel", 10)
    assert r["albums"][0]["id"] == 2786226
    assert r["albums"][0]["name"] == "Accel World Original Soundtrack feat.ONOKEN"

    # test searching artists -> http://music.163.com/artist?id=18473
    r = generic_search("Sound Online", 100)
    assert r["artists"][0]["id"] == 18473
    assert r["artists"][0]["name"] == "Sound Online"


if __name__ == '__main__':
    test()
