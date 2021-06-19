# scripts for data initialization
# etf.py initialization script
# stock.py initialization script

import requests
import datetime
import json
import logging

import sys
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


def get_stock_data(url,sosok):
    documents = []
    for i in range(0,100):
        res = requests.get(f"{url}?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn%3F%26sosok%3D{sosok}%26page%3D{i}&fieldIds=quant&fieldIds=market_sum&fieldIds=per&fieldIds=roe&fieldIds=frgn_rate&fieldIds=pbr")
        data = BeautifulSoup(res.text,"lxml")
        tableHead = data.select("#contentarea > div.box_type_l > table.type_2 > thead")
        tableBody = data.select("#contentarea > div.box_type_l > table.type_2 > tbody > tr")
        
        if tableBody is None:
            break
        
        for row in tableBody:
            tableCell = row.find_all("td")
            if (not "blank" in str(tableCell)) and (not "division_line" in str(tableCell)):
                code = tableCell[1].find("a")["href"].split("=")[1]
                stockData = {
                    "stockName" : tableCell[1].getText() if tableCell[1].getText() != "N/A" else None,
                    "code": code,
                    "price": int(tableCell[2].getText().replace(",","")) if tableCell[2].getText() != "N/A"  else None,
                    "per":  float(tableCell[9].getText().replace(",","")) if tableCell[9].getText() != "N/A"  else None,
                    "roe":  float(tableCell[10].getText().replace(",","")) if tableCell[10].getText() != "N/A" else None,
                    "pbr":  float(tableCell[11].getText().replace(",","")) if tableCell[11].getText() != "N/A" else None,
                    "timestamp": datetime.datetime.now()
                }
                document = {
                    "index" : {
                        '_index': "stock-data-latest",
                        '_source': stockData,
                        '_id': code
                    }
                }
                logging.info(f"STOCK ID [{code}] info gathered from NAVER stock")
                logging.info(document)
                documents.append(document)
    return documents

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
    etfProfit1M = float(etfProfits[0].get_attribute('innerText')) if etfProfits[0].get_attribute('innerText') else None
    etfProfit3M = float(etfProfits[1].get_attribute('innerText')) if etfProfits[1].get_attribute('innerText') else None
    etfProfit6M = float(etfProfits[2].get_attribute('innerText')) if etfProfits[2].get_attribute('innerText') else None
    etfProfit12M = float(etfProfits[3].get_attribute('innerText')) if etfProfits[3].get_attribute('innerText') else None
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
        stockPortion = float(row.find_element_by_class_name("c3").get_attribute('innerText')) if row.find_element_by_class_name("c3").get_attribute('innerText') != "-" else None
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
        "etfTypes": etfTypeList,
        "timestamp": datetime.datetime.now()
    }
    #print(json.dumps(etfData,indent=4,ensure_ascii=False))
    logging.info(f"ETF ID [{id}] info gathered from DAUM stock")
    driver.close()
    return etfData


def etf():
    logging.basicConfig(
        filename='etf.log',
        format = '%(asctime)s:%(levelname)s:%(message)s',
        datefmt = '%m/%d/%Y %I:%M:%S %p %Z',
        level = logging.INFO,
        filemode="w"
    )
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__name__)
    #etfTargets = get_etf_list(Config.URL_NAVER_STOCK)
    etfTargets = ["069500"] #for test
    es = Elasticsearch(
    hosts=[{'host': "localhost", 'port': "9200"}])
    logging.info("etf crawling initialize start")
    documents = []
    for etf in etfTargets:
        etfData = get_etf_info(etf)
        document = {
            "index" : {
                '_index': "etf-search-latest",
                '_source': etfData,
                '_id': etf
            }
        }
        logging.info(document)
        documents.append(document)
        
    try:      
        helpers.bulk(es, documents)
    except Exception as e:
        logging.info(e)
        
    logging.info("etf crawling initialize end")
    
def stock():
    logging.basicConfig(
        filename='stock.log',
        format = '%(asctime)s:%(levelname)s:%(message)s',
        datefmt = '%m/%d/%Y %I:%M:%S %p %Z',
        level = logging.INFO,
        filemode="w"
    )
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__name__)
    logging.info("stock crawling initialize start")
    #https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0
    #https://finance.naver.com/sise/field_submit.nhn?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn%3Fsosok%3D1%26page%3D3&fieldIds=quant&fieldIds=market_sum&fieldIds=per&fieldIds=roe&fieldIds=listed_stock_cnt&fieldIds=pbr
    es = Elasticsearch(
    hosts=[{'host': "localhost", 'port': "9200"}])
    try: 
        documents = get_stock_data("https://finance.naver.com/sise/field_submit.nhn",0)
        helpers.bulk(es, documents)
        documents = get_stock_data("https://finance.naver.com/sise/field_submit.nhn",1)
        helpers.bulk(es, documents)
        logging.info("stock crawling initialize end")
    except Exception as e:
        logging.info(e)

    
if __name__ == "__main__":
    # execute only if run as a script
    if sys.args[1] == "etf":
        etf()
    elif sys.args[1] == "stock":
        stock()
    else:
        print("init.py [etf|stock]")
        
