import requests
import datetime
import json
import logging

import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from elasticsearch import Elasticsearch, helpers

from config import Config 


def get_etf_list(url):
    # get etf full list
    etfTargets = []
    response = requests.get(url).json()
    etfLists = response['result']['etfItemList']
    
    for etf in etfLists:
        etfTargets.append(etf['itemcode'])

    logging.info(f"ETF lists gathered from NAVER stock (count:{len(etfTargets)})")
    
    return etfTargets

def get_etf_info(id):
    # get etf info 
    target_source = f"https://wisefn.finance.daum.net/v1/ETF/index.aspx?cmp_cd={id}"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # options.add_argument('window-size=1200x600')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    logging.info(f"ETF ID [{id}] info start gathering from DAUM stock")
    driver = webdriver.Chrome(options=options, executable_path="/usr/lib/chromium-browser/chromedriver")
    driver.implicitly_wait(time_to_wait=1)
    driver.get(url=target_source)

    # get etf information
    etfName = driver.find_element_by_class_name('nm_k').get_attribute('innerText')
    description = driver.find_element_by_class_name('dot_cmp')
    etfDescription = description.get_attribute('innerText')
    etfTypeInfo = driver.find_element_by_xpath('//*[@id="comInfo"]/tbody/tr[3]/td/span[5]')
    etfTypeInfo = etfTypeInfo.get_attribute('innerText').split(":")[1]
    etfTypeList = []
    for etfType in etfTypeInfo.split(","):
        etfTypeList.append(
            {
                "etfType": etfType
            })
        

    # get etf profit information
    profits = driver.find_element_by_class_name("num.pd_bot_20")
    etfProfits = profits.find_elements_by_tag_name("span")
    etfProfit1M = etfProfits[0].get_attribute('innerText')
    etfProfit3M = etfProfits[1].get_attribute('innerText')
    etfProfit6M = etfProfits[2].get_attribute('innerText')
    etfProfit12M = etfProfits[3].get_attribute('innerText')
    etfProfits = {
                    "etfProfit1M": etfProfit1M,
                    "etfProfit3M": etfProfit3M,
                    "etfProfit6M": etfProfit6M, 
                    "etfProfit12M": etfProfit12M
                }

    # get etf elements
    etfElements = []
    table = driver.find_element_by_id("tbl-index0")
    tbody = table.find_element_by_tag_name("tbody")
    rows = tbody.find_elements_by_tag_name("tr")
    for row in rows:
        #//*[@id="tbl-index0"]/tbody/tr[1]/td[1]
        stockName = row.find_element_by_class_name("c1").get_attribute('innerText')
        stockPortion = row.find_element_by_class_name("c3").get_attribute('innerText')
        etfElements.append(
                {
                    "stockName": stockName, 
                    "stockPortion": stockPortion
                })

    etfData = {
        "etfName": etfName,
        "etfDescription": etfDescription,
        "etfElements": etfElements,
        "etfProfits": etfProfits,
        "etfTypes": etfTypeList
    }
    #print(json.dumps(etfData,indent=4,ensure_ascii=False))
    logging.info(f"ETF ID [{id}] info gathered from DAUM stock")
    driver.close()
    return etfData


def main():
    logging.basicConfig(
        filename='etf-search.log',
        format = '%(asctime)s:%(levelname)s:%(message)s',
        datefmt = '%m/%d/%Y %I:%M:%S %p',
        level = logging.INFO,
        filemode="w"
    )
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__name__)
    etfTargets = get_etf_list(Config.URL_NAVER_STOCK)
    #etfTargets = ["069500"] #for test
    es = Elasticsearch(
    hosts=[{'host': "localhost", 'port': "9200"}])
    
    for etf in etfTargets:
        try:
            documents = []
            etfData = get_etf_info(etf)
            document = {
               '_index': "etf-search-latest",
               '_source': etfData,
               '_id': etf
            }
            documents.append(document)
            helpers.bulk(es, documents)
        except Exception as e:
            logging.info(e)
    
if __name__ == "__main__":
    # execute only if run as a script
    main()
