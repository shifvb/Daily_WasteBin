def to_hex(data: bytes):
    for i in range(0, len(data), 16):
        s = data[i:i + 16]
        s_left = '{:0>4}'.format(hex(i)[2:].upper())
        s_right = ''.join([chr(b) if 0x20 < b < 0x7F else '.' for b in s])
        s_middle = ' '.join(['{:0<2}'.format(hex(b)[2:].upper()) for b in s])
        yield ('{:<8} {} {:>20}\n'.format(s_left, s_middle, s_right))


def main():
    f = open('日常デコレーション.mp3', 'rb')
    f2 = None
    MAX_LINE = 1024 * 32
    line_counter = MAX_LINE
    file_counter = 0
    for line in to_hex(f.read()):
        if line_counter == 1024 * 32:
            if f2:
                f2.close()
            f2 = open('日常デコレーション_hexdata_{}.log'.format(file_counter), 'w')
            file_counter += 1
            line_counter = 0
        line_counter += 1
        f2.write(line)

    f2.close()
    f.close()


if __name__ == '__main__':
    main()
