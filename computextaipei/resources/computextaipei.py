from flask import jsonify
from flask_restful import Resource

import csv
import threading
from computextaipei.computextaipei_web_crawler import ComputextaipeiWebCrawler
from multiprocessing import Process, Value


class Computextaipei(Resource):
    computextaipeiWebCrawler = None

    def __init__(self, needDriver=True, debug=False) -> None:
        if needDriver:
            self.computextaipeiWebCrawler = ComputextaipeiWebCrawler(debug=debug)
        pass

    def __del__(self):
        if self.computextaipeiWebCrawler:
            del self.computextaipeiWebCrawler
        pass

    def __run_process(self):
        def runProcess():
            p = Process(
                target=self.__computextaipeiWebCrawler,
            )
            p.start()
            p.join()

        # 利用執行緒執行子進程，防止主進程停止後，子進程無法被消除變成殭屍進程
        t = threading.Thread(target=runProcess)
        t.daemon = True
        t.start()

    def __computextaipeiWebCrawler(self):
        urls = []
        with open("new-project.csv", newline="", encoding="ISO-8859-1") as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                urls.append(row[1])
        self.computextaipeiWebCrawler.getBatchInfos(
            urls,
            True,
        )

    def get(self):
        result = []
        self.__run_process()
        return jsonify(result)
