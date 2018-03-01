import configparser

cfg = None


def load_config():
    """load config.ini file(lazt)"""
    global cfg
    if cfg is not None:
        return cfg
    # load config.ini file
    parser = configparser.ConfigParser()
    parser.read("../config.ini")
    d = dict()
    for section in parser.sections():
        d[section] = dict()
        for option in parser.options(section):
            d[section][option] = parser[section][option]
    return d


if __name__ == '__main__':
    print(load_config())
