from pprint import pprint
import requests
import random
import pymysql
import json
import time
import threading
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import choice
from NeteaseCloudMusic import *
import NetEaseMusicApi
import logging


def main_multi_threads(p_start_id, p_end_id, prefer_list=None):
    def jobs():
        if prefer_list is not None and isinstance(prefer_list, list):
            for _ in prefer_list:
                yield _
        for _ in range(p_start_id, p_end_id):
            # if _ % 1000 == 0:
            # time.sleep(10)
            yield _

    result_stubs = set()
    conn_pools = [pymysql.connect(host="127.0.0.1", user="root", password="97033925", database="netease", port=3306,
                                  use_unicode=True, charset='utf8') for _ in range(17)]

    def fn(i):  # worker function
        try:
            conn = conn_pools[int(threading.current_thread().getName().split("-")[1])]
            cursor = conn.cursor()
            r = ncm.query_song(i)
            if r:
                rstr = json.dumps(r, sort_keys=True).replace("\\", "\\\\").replace('"', r'\"')
                sql = insert_sql.format((i // 1000000 + 1), r["id"], rstr)
                cursor.execute(sql)
            conn.commit()
            cursor.close()
        except Exception as e:
            # if not str(e)[8:17] == "Duplicate":
            return False, "{} {}: {}".format(i, time.ctime(), str(e))
        return True, i

    with ThreadPoolExecutor(max_workers=16) as executor:
        for job in jobs():
            result_stub = executor.submit(fn, job)
            result_stubs.add(result_stub)
        for result_stub in as_completed(result_stubs):
            result = result_stub.result()
            if result[0] is False:
                global total_fails_count
                total_fails_count += 1
                logging.warning(result)

    # close connections
    [conn.close() for conn in conn_pools]


if __name__ == '__main__':
    ncm = NeteaseCloudMusic()
    logging.basicConfig(format="%(message)s", level=logging.WARNING, filename="test.log")
    total_fails_count = 0
    insert_sql = """INSERT INTO `testsong{}` VALUES({}, "{}");"""
    start_id = 25500000
    end_id = 25501000
    prefer_list = []
    start_time = time.time()
    main_multi_threads(start_id, end_id, prefer_list)
    # main_random()
    end_time = time.time()
    print("time elapsed: {}s".format(end_time - start_time))
    print("avg {} req per second.".format((end_id - start_id + len(prefer_list)) / (end_time - start_time)))
    print("total fails count: {}".format(total_fails_count))
