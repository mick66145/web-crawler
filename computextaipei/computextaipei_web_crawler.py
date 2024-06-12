from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from collections.abc import Iterable
import time
import argparse
import csv


def outputCsv(title, items, fieldnames, file_name="output.csv", delimiter=","):
    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter)
        writer.writerow(title)
        writer.writerows(items)
    pass


class ComputextaipeiWebCrawler:
    def __init__(self, debug=False) -> None:
        self.debug = debug
        self.driver = self.__getDriver()
        pass

    def __del__(self):
        try:
            self.driver.quit()
        except:
            return None
        pass

    def getBatchInfos(self, urls: Iterable[str], output_file=False):
        data = []
        for url in urls:
            print(url)
            self.driver.get(url)
            infoItems = self.__getPageInfos()
            for infoItem in infoItems:
                data.append(infoItem)

        if output_file:
            file_name = time.strftime("%Y%m%d") + "__output.csv"
            outputCsv(
                {
                    "info_company_name": "公司名稱",
                    "info_company_address": "公司地址",
                    "info_company_link": "公司網址",
                },
                data,
                [
                    "info_company_name",
                    "info_company_address",
                    "info_company_link",
                ],
                file_name,
            )

        return data

    def __getDriver(self):
        options = Options()

        if not self.debug:
            options.add_argument("--headless")  # 啟動Headless 無頭
            options.add_argument("--disable-gpu")  # 關閉GPU 避免某些系統或是網頁出錯
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        service = Service(executable_path=ChromeDriverManager().install())

        return webdriver.Chrome(service=service, options=options)

    def __getPageInfos(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        infos = soup.find_all("div", class_="company_info")

        infos_items = []
        for index, info in enumerate(infos):
            info_object = self.__infoParse(info=info)
            infos_items.append(info_object)

        return infos_items

    def __infoParse(self, info):
        item = {}
        # 公司名稱
        try:
            info_company_name = info.find("h2").text
        except Exception as e:
            info_company_name = None

        # 公司地址
        try:
            info_company_address = info.find_all("li")[0].text
        except Exception as e:
            info_company_address = None

        # 公司網址
        try:
            info_company_link = info.find_all("li")[1].text
        except Exception as e:
            info_company_link = None

        item["info_company_name"] = info_company_name
        item["info_company_address"] = info_company_address
        item["info_company_link"] = info_company_link

        return item

    # util function to clean special characters
    def __filter_string(self, str):
        strOut = str.replace("\r", " ").replace("\n", " ").replace("\t", " ")
        return strOut

    pass
