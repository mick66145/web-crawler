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


def getArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        default="https://www.computextaipei.com.tw/en/exhibitor/CE1F519AF8152C413B18EC96FA84DD5D/info.html",
        type=str,
    )
    parser.add_argument(
        "--show-ui", default=False, action=argparse.BooleanOptionalAction
    )
    return parser


def getChromeOptions() -> Options:
    argParse = getArgParser()
    args = argParse.parse_args()
    chrome_options = Options()
    if not (args.show_ui):
        chrome_options.add_argument("--headless")  # 啟動Headless 無頭
        chrome_options.add_argument("--disable-gpu")  # 關閉GPU 避免某些系統或是網頁出錯
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    return chrome_options


# util function to clean special characters
def __filter_string(str):
    strOut = str.replace("\r", " ").replace("\n", " ").replace("\t", " ")
    return strOut


# def infoParse(info):
#     item = {}

#     # Google評論 ID
#     try:
#         info_id = info["data-review-id"]
#     except Exception as e:
#         info_id = None

#     # 評論者名稱
#     try:
#         info_user_name = info["aria-label"]
#     except Exception as e:
#         info_user_name = None

#     # 評分
#     try:
#         info_rating = float(
#             info.find("span", class_="kvMYJc")["aria-label"].split(" ")[0]
#         )
#     except Exception as e:
#         info_rating = None

#     # 評論內容
#     try:
#         info_comment = __filter_string(
#             info.find("div", class_="MyEned").find("span", class_="wiI7pd").text
#         )
#     except Exception as e:
#         info_comment = None

#     item["id"] = info_id
#     item["user_name"] = info_user_name
#     item["rating"] = info_rating
#     item["comment"] = info_comment

#     return item


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
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            # store_name = soup.find("h1", class_="DUwDvf lfPIob").text
            infoItems = self.__getPageInfos()
            for infoItem in infoItems:
                # data.append(infoItem | {"store_name": store_name})
                data.append(infoItem)

        if output_file:
            file_name = time.strftime("%Y%m%d") + "__output.csv"
            outputCsv(
                {
                    "store_name": "店家名稱",
                    "id": "ID",
                    "user_name": "使用者名稱",
                    "rating": "評分",
                    "comment": "內容",
                },
                data,
                ["store_name", "id", "user_name", "rating", "comment"],
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
        reviews = soup.find_all("div", class_="company_info")
        # info_block = self.driver.find_element(
        #     By.CSS_SELECTOR, "div[class='m6QErb DxyBCb kA9KIf dS8AEf ']"
        # )
        print(reviews)

        # time.sleep(1)

        # # 點擊切換到評論頁
        # roleButtons = self.driver.find_element(
        #     By.CSS_SELECTOR, "div[role='tablist']"
        # ).find_elements(By.TAG_NAME, "button")
        # for button in roleButtons:
        #     if button.text == "評論":
        #         button.click()
        #         break

        # time.sleep(2)

        # 滾動評論
        # i = 0
        # info_block = self.driver.find_element(
        #     By.CSS_SELECTOR, "div[class='m6QErb DxyBCb kA9KIf dS8AEf ']"
        # )

        # while i < 4 and info_block.get_attribute(
        #     "scrollTop"
        # ) != info_block.get_attribute("scrollHeight"):
        #     self.driver.execute_script(
        #         "arguments[0].scrollTop = arguments[0].scrollHeight", info_block
        #     )
        #     i += 1
        #     time.sleep(0.5)

        # time.sleep(1)

        # 點擊所有評論查看更多
        # showInfoButtons = self.driver.find_elements(
        #     By.CSS_SELECTOR, "button[jsaction='pane.info.expandInfo']"
        # )
        # for button in showInfoButtons:
        #     button.click()

        # time.sleep(3)

        # soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # infos = soup.find_all("div", class_="jftiEf fontBodyMedium")

        infos_items = []
        # for index, info in enumerate(infos):
        #     info_object = self.__infoParse(info=info)
        #     infos_items.append(info_object)

        return infos_items

    def __infoParse(self, info):
        item = {}

        # Google評論 ID
        try:
            info_id = info["data-info-id"]
        except Exception as e:
            info_id = None

        # 評論者名稱
        try:
            info_user_name = info["aria-label"]
        except Exception as e:
            info_user_name = None

        # 評分
        try:
            info_rating = float(
                info.find("span", class_="kvMYJc")["aria-label"].split(" ")[0]
            )
        except Exception as e:
            info_rating = None

        # 評論內容
        try:
            info_comment = self.__filter_string(
                info.find("div", class_="MyEned").find("span", class_="wiI7pd").text
            )
        except Exception as e:
            info_comment = None

        item["id"] = info_id
        item["user_name"] = info_user_name
        item["rating"] = info_rating
        item["comment"] = info_comment

        return item

    # util function to clean special characters
    def __filter_string(self, str):
        strOut = str.replace("\r", " ").replace("\n", " ").replace("\t", " ")
        return strOut

    pass
