import requests
import hashlib
from random import randint
import base64

__all__ = ["download_song_by_dfsid"]


# todo : sometimes valid, sometimes invalid
def download_song_by_dfsid(dfsid: int):
    url = "http://m{}.music.126.net/{}/{}.mp3".format(2, _encrypt(dfsid), dfsid)
    print(url)
    headers = {
        'Referer': 'http://music.163.com',
    }
    return requests.get(url, headers=headers).content


def _encrypt(dfsid: int):
    byte1 = bytearray('3go8&$8*3*3h0k(2)2', 'utf8')
    byte2 = bytearray(str(dfsid), 'utf8')
    byte1_len = len(byte1)
    for i in range(len(byte2)):
        byte2[i] = byte2[i] ^ byte1[i % byte1_len]
    m = hashlib.md5(byte2).digest()
    return base64.b64encode(m).decode('utf8').replace('/', '_').replace('+', '-')





def test():
    r = download_song_by_dfsid(2058285767198191)
    print(r)
    # for id in (2024200906764550,):
    #     a = _encrypt(id)
    #     b = encrypted_id(id)
    #     print(a)
    #     print(b)
    #     assert a == b

if __name__ == '__main__':
    test()
