import os


def main():
    warnings = []
    dirs = os.listdir(HOME_DIR)
    for index, dir in enumerate(dirs):
        os.chdir(HOME_DIR + os.path.sep + dir)
        photos = os.listdir(os.curdir)
        for photo in photos:
            photo_size = os.path.getsize(photo)
            if photo_size < 1024:
                warnings.append("{}*{}*{}".format(photo, photo_size, dir))
                os.remove(photo)
    for warning in warnings:
        print(warning)


if __name__ == '__main__':
    # home dir
    HOME_DIR = r"E:\H\cache"
    main()
