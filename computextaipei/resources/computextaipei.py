from flask import jsonify
from flask_restful import Resource

import csv
from computextaipei.computextaipei_web_crawler import ComputextaipeiWebCrawler


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

    def get(self):
        urls = []
        with open("new-project.csv", newline="", encoding="ISO-8859-1") as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                urls.append(row[1])

        result = []
        result = self.computextaipeiWebCrawler.getBatchInfos(
            urls,
            True,
        )
        return jsonify(result)
