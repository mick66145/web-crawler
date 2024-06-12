from flask import jsonify
from flask_restful import Resource

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
        result = []
        result = self.computextaipeiWebCrawler.getBatchInfos(
            [
                "https://www.computextaipei.com.tw/en/exhibitor/CE1F519AF8152C413B18EC96FA84DD5D/info.html?lt=data&vt=country-list&cr=1&cate=TW"
            ],
            True,
        )
        return jsonify(result)
