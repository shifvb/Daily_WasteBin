# The MIT License
#
# Copyright 2018 shifvb
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, # and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
__author__ = 'shifvb'
__email__ = 'shifvb@gmail.com'
__last_modified__ = 1523239141
__version__ = (1, 0, 0)

import copy

# permuted choice key 1
_PC_1 = (56, 48, 40, 32, 24, 16, 8, 0, 57, 49, 41, 33, 25, 17,
         9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35,
         62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21,
         13, 5, 60, 52, 44, 36, 28, 20, 12, 4, 27, 19, 11, 3)

# number of left rotations in _pc_1(one bit in 1, 2, 9, 16 stage, two bits in other stages)
_left_rotations = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# permuted choice key 2
_PC_2 = (13, 16, 10, 23, 0, 4, 2, 27, 14, 5, 20, 9,
         22, 18, 11, 3, 25, 7, 15, 6, 26, 19, 12, 1,
         40, 51, 30, 36, 46, 54, 29, 39, 50, 44, 32, 47,
         43, 48, 38, 55, 33, 52, 45, 41, 49, 35, 28, 31)

# initial transposition (IT)
_IT = (57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
       61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7,
       56, 48, 40, 32, 24, 16, 8, 0, 58, 50, 42, 34, 26, 18, 10, 2,
       60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6)

# Expansion box (32 bits -> 48 bits)
_EBox = (31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8,
         7, 8, 9, 10, 11, 12, 11, 12, 13, 14, 15, 16,
         15, 16, 17, 18, 19, 20, 19, 20, 21, 22, 23, 24,
         23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0)

# SBox
_SBox = (
    # Box1
    (14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
     0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
     4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
     15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13),

    # Box2
    (15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
     3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
     0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
     13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9),

    # Box3
    (10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
     13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
     13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
     1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12),

    # Box4
    (7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
     13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
     10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
     3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14),

    # Box5
    (2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
     14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
     4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
     11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3),

    # Box6
    (12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
     10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
     9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
     4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13),

    # Box7
    (4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
     13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
     1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
     6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12),

    # Box8
    (13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
     1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
     7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
     2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11),
)

# PBox
_PBox = (15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9,
         1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24)

# Final Transposition
_FP = (39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30,
       37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28,
       35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26,
       33, 1, 41, 9, 49, 17, 57, 25, 32, 0, 40, 8, 48, 16, 56, 24)


class MyDES(object):
    def __init__(self, key: str, padding_char: str):
        assert len(padding_char) == 1
        self.K1 = MyDES._get_K1(key)
        self.pad = padding_char.encode('ascii')

    @staticmethod
    def _get_K1(key: str):
        _64_bit_key = MyDES._bytes_to_bit_list(key.encode('ascii'))  # 首先经过ascii编码, get 64 bit key
        _56_bit_key = MyDES._permute(_PC_1, _64_bit_key)  # discarding, get 56 bit key
        _28_bit_C0, _28_bit_D0 = _56_bit_key[:28], _56_bit_key[28:]  # split key
        _K1 = [[0 for j in range(48)] for i in range(16)]  # 16 sub-keys, 48 bits per sub key
        for i in range(16):
            for j in range(_left_rotations[i]):
                _28_bit_C0.append(_28_bit_C0[0])  # left shift C0 (respect to _left_rotations)
                del _28_bit_C0[0]
                _28_bit_D0.append(_28_bit_D0[0])  # left shift D0 (respect to _left_rotations)
                del _28_bit_D0[0]
            _K1[i] = MyDES._permute(_PC_2, _28_bit_C0 + _28_bit_D0)  # get sub-keys
        return _K1

    def encrypt(self, data: bytes):
        # padding
        _block_size = 8
        _new_len = (len(data) // _block_size + 1) * _block_size
        data = data.ljust(_new_len, self.pad)
        return self._crypt(data, mode="encrypt")

    def decrypt(self, data: bytes):
        return self._crypt(data, mode="decrypt").rstrip(self.pad)

    def _crypt(self, data: bytes, mode: str):
        # encrypting
        result = []
        for d_idx in range(0, len(data), 8):
            _block_data = MyDES._bytes_to_bit_list(data[d_idx: d_idx + 8])  # get one single byte of the data(bit list)
            _block_data = MyDES._permute(_IT, _block_data)  # permute (Initial Transposition)
            _LP, _RP = _block_data[:32], _block_data[32:]  # get left part & right part
            for i in range(16):
                temp_RP = copy.deepcopy(_RP)  # make a copy os _RP[i-1], it will become LP[i] later
                # EBox (32 bits -> 48 bits)
                _RP = MyDES._permute(_EBox, _RP)
                # SBox
                _RP = [_x ^ _y for _x, _y in zip(_RP, self.K1[i])] if mode == 'encrypt' else \
                    [_x ^ _y for _x, _y in zip(_RP, self.K1[15 - i])]  # 做按位XOR运算
                _boxes = [_RP[:6], _RP[6:12], _RP[12:18], _RP[18:24], _RP[24:30], _RP[30:36], _RP[36:42], _RP[42:]]
                _boxes_n = [0 for _ in range(32)]
                for j in range(8):
                    # Work out the offsets
                    m = (_boxes[j][0] << 1) + _boxes[j][5]
                    n = (_boxes[j][1] << 3) + (_boxes[j][2] << 2) + (_boxes[j][3] << 1) + _boxes[j][4]
                    # Find the permutation value
                    v = _SBox[j][(m << 4) + n]
                    # Turn value into bits
                    _boxes_n[4 * j] = (v & 8) >> 3
                    _boxes_n[4 * j + 1] = (v & 4) >> 2
                    _boxes_n[4 * j + 2] = (v & 2) >> 1
                    _boxes_n[4 * j + 3] = v & 1
                # PBox
                _RP = MyDES._permute(_PBox, _boxes_n)
                # XOR
                _RP = [_x ^ _y for _x, _y in zip(_RP, _LP)]
                # _LP becomes _RP[i - 1]
                _LP = temp_RP
            # final transposition
            result.append(MyDES._bit_list_to_bytes(MyDES._permute(_FP, _RP + _LP)))
        return b"".join(result)

    @staticmethod
    def _bytes_to_bit_list(data: bytes):
        """从bytes序列生成一个含有0或者是1的list"""
        _bit_list = bytearray()
        for c in data:
            _single_bit_list = "{:>08}".format(bin(c)[2:])
            _bit_list.extend([int(_) for _ in _single_bit_list])
        return _bit_list

    @staticmethod
    def _bit_list_to_bytes(bit_list: list):
        """从含有0或1的list生成一个bytes序列"""
        _b = bytearray()
        for i in range(0, len(bit_list), 8):
            _s = "".join([str(_) for _ in bit_list[i:i + 8]])
            _b.append(eval("int(0b{})".format(_s)))
        return bytes(_b)

    @staticmethod
    def _permute(permute_table: tuple, block: list):
        """用来替换的"""
        return [block[_] for _ in permute_table]


if __name__ == '__main__':
    my_des = MyDES(key="8e1b855c", padding_char="*")
    plain_text = "DEMOCRACY and FREEDOM are indispensable when building modern community."
    encrypted_text = my_des.encrypt(plain_text.encode('utf-8'))
    decrypted_text = my_des.decrypt(encrypted_text).decode('utf-8')
    print(decrypted_text)
