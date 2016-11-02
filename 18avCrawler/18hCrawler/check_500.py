import os


def main():
    s1 = set((str(x) for x in (range(5000, 5501))))
    s2 = set()

    os.chdir(BASE_DIR)
    dirs = os.listdir(os.curdir)
    for dir in dirs:
        s2.add(dir.split("_")[0])
    L = s1 - s2
    L = sorted(L)
    L = [int(x) for x in L]
    print(L)


if __name__ == '__main__':
    BASE_DIR = r"E:\H\cache"
    main()
