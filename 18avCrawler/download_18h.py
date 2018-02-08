import requests
import bs4
import os
from concurrent.futures import ThreadPoolExecutor


class Download18HPage(object):
    def __init__(self, index: int, url: str, save_folder: str):
        self._url = url.format(index)
        # 索引号
        self._index = index
        # 本子名称
        self._title = ""
        # 本子图片数目
        self._num_page = -1
        # 本子图片url列表
        self._img_url_list = []
        # 存储路径
        self._save_folder = save_folder

    def run(self):
        _act_num_img = self.parse_and_download()
        # 判断下载是否完全
        if _act_num_img == self._num_page:
            print("[INFO] Completely Downloaded {} ({}/{}).".format(self._url, _act_num_img, self._num_page))
        else:
            print("[WARN] Incomplete Download! {} ({}/{})".format(self._url, _act_num_img, self._num_page))

    def parse_and_download(self):
        """解析网页 & 下载本子"""
        try:
            print("[INFO] Downloading {}...".format(self._url))
            # 抓取html网页
            html = requests.get(self._url, proxies={"http": "http://127.0.0.1:1080"}).content.decode("utf-8")
            soup = bs4.BeautifulSoup(html, "html5lib")
            # 获得图片数目
            self._num_page = int(soup.div.center.h1.text.split(" ")[-1].strip("[]p"))
            # 获得本子名称
            self._title = soup.title.text
        except:
            return
        # 获得图片url列表
        _img_list = [_ for _ in soup.text.split("\n") if "Large_cgurl[" in _][:self._num_page]
        _img_list = [_.strip("\t;").split("=")[-1].strip("\" ") for _ in _img_list]
        self._img_url_list = _img_list
        # 一种激进的方法，如果无效请禁用
        self._img_url_list = [
            'http://hahost2.imgscloud.com/fileshort/1{}/1{}_{:>03}.jpg'.format(self._index, self._index, _img_index + 1)
            for _img_index in range(self._num_page)]
        # 生成存储文件夹
        save_folder = os.path.join(self._save_folder, "{}_{}p_{}".format(self._index, self._num_page, self._title))
        if not os.path.isdir(save_folder):
            os.makedirs(save_folder)
        self._save_folder = save_folder
        # 创建线程池
        _succeed_counter = 0
        with ThreadPoolExecutor(max_workers=8) as executor:
            for result in executor.map(self.download_image, self._img_url_list):
                if result is True:
                    _succeed_counter += 1
        return _succeed_counter

    def download_image(self, image_url: str) -> bool:
        """
        下载本子里的单张图片
        :param image_url: 图片url
        :return: True -> 成功，False -> 失败
        """
        img_name = os.path.split(image_url)[-1]
        timeout_counter = 0
        while timeout_counter < 3:  # 连续尝试3次
            try:
                img_data = requests.get(image_url, timeout=10).content
                with open(os.path.join(self._save_folder, img_name), "wb") as f:
                    f.write(img_data)
                return True
            except:
                timeout_counter += 1
        return False


if __name__ == '__main__':
    # url = r"http://18h.mm-cg.com/18H_{}.html"
    for i in range(5552, 7500):
        Download18HPage(index=i,
                        url=r"http://18h.mm-cg.com/doujin_{}.html",
                        save_folder=r"d:\doujin").run()
