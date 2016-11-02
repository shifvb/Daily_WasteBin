import os


def main():
    os.chdir(HOME_DIR)
    dirs = os.listdir(os.curdir)
    for dir in dirs:
        # gather data
        temp_names = dir.split("_")
        temp_length = len(os.listdir(dir))
        difference = int(temp_names[1][:-1]) - temp_length
        # show dir
        if difference > SHOW_THRESHOLD:
            print("{} {}".format(temp_names, difference))
        # delete dir
        if difference > DEL_THRESHOLD:
            for x in os.listdir(dir):
                os.remove(os.path.join(HOME_DIR, dir, x))
            os.removedirs(dir)


if __name__ == '__main__':
    HOME_DIR = r"E:\H\cache"
    # dirs in `HOME_DIR`: lost photo count display threshold
    SHOW_THRESHOLD = 0
    # dirs in `HOME_DIR`: lost photo count delete threshold
    DEL_THRESHOLD = 20
    main()
