import requests

__all__ = ["get_user_detail_from_user_id"]


def get_user_detail_from_user_id(user_id: int):
    url = "http://music.163.com/api/user/profile/{}".format(user_id)
    headers = {
        'Referer': 'http://music.163.com',
    }
    r = requests.get(url=url, headers=headers).json()
    return r["profile"] if r.get("code", -1) == 200 else None


def test():
    from pprint import pprint
    r = get_user_detail_from_user_id(96208282)
    pprint(r)
    pass


if __name__ == '__main__':
    test()
