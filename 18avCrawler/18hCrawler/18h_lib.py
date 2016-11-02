import requests
import bs4
import re
import os
import concurrent.futures


def fetch_one_url(url: str):
    '''fetch one url return a list of all imgs'''
    title = None
    try:
        img_pattern = re.compile(r'Large_cgurl\[\d+\] = "(.*)";')
        content = requests.get(url).content
        soup = bs4.BeautifulSoup(content, "html5lib")
        title = soup.head.title.text
        picture_counts = int(soup.find_all(name="h1")[0].text.strip().split(" ")[-1].strip("[p]"))
        lines = soup.find_all(name="script", attrs={"type": None, "language": "javascript"})[0].text.split("\n")
        lines = map(lambda line: line.strip(), lines)
        lines = filter(lambda line: img_pattern.match(line), lines)
        lines = map(lambda line: img_pattern.match(line).group(1), lines)
        lines = list(lines)
        #############################
        # 请手动调节
        handle_by_human = False
        x = 78
        y = x
        y = y
        if handle_by_human:
            lines = lines[x - 1:y]
        ##############################
        else:
            assert picture_counts == len(lines)
        # 手动调节部分结束
        folder_name = str(re.match(r"http://18h.mm-cg.com/18H_(\d+?)\.html", url).group(1)) + \
                      "_" + "{}p".format(picture_counts) + "_" + title
        download_imgs(folder_name, lines)
    except Exception as e:
        return False, title, str(e)
    if title is None:
        return False, title
    return True, title


def download_imgs(folder_name: str, imgs: list):
    '''download imgs'''
    folder_name = folder_name.replace("/", "")  # fix some characters that cannot contains in folder name
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    for img in imgs:
        img_name = img.split("/")[-1]
        counter = 0
        data = b""
        while counter < 2:
            try:
                data = requests.get(img).content
            except:
                data = b""
            if len(data) > 10 * 1024:
                break
            counter += 1

        with open(os.path.join(folder_name, img_name), 'wb') as f:
            f.write(data)


def get_jobs(start_id, end_id, prefer_list):
    for x in prefer_list:
        yield "http://18h.mm-cg.com/18H_{}.html".format(x)
    for i in range(start_id, end_id):
        yield "http://18h.mm-cg.com/18H_{}.html".format(i)


def main(start_id: int, end_id: int, prefer_list: list, job_fn):
    result_stubs = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for url in job_fn(start_id, end_id, prefer_list):
            result_stub = executor.submit(fetch_one_url, url)
            result_stubs.add(result_stub)
    for result_stub in concurrent.futures.as_completed(result_stubs):
        print(result_stub.result())


if __name__ == '__main__':
    version = (0, 0, 1)
    BASE_DIR = r"E:\H\cache"
    os.chdir(BASE_DIR)
    main(5500, 5500, [5469], get_jobs)
