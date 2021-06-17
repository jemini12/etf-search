import requests
import datetime
import json
import logging

from elasticsearch import Elasticsearch, helpers
from config import Config 
from bs4 import BeautifulSoup

def get_stock_list(url):
    #?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn%3Fsosok%3D0&fieldIds=quant&fieldIds=market_sum&fieldIds=per&fieldIds=roe&fieldIds=frgn_rate&fieldIds=pbr
    #https://finance.naver.com/sise/field_submit.nhn?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn%3F%26page%3D2&fieldIds=quant&fieldIds=market_sum&fieldIds=per&fieldIds=roe&fieldIds=frgn_rate&fieldIds=pbr
    for i in range(0,100):
        #res = requests.get(f"https://finance.naver.com/sise/field_submit.nhn?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn%3F%26page%3D2&fieldIds=quant&fieldIds=market_sum&fieldIds=per&fieldIds=roe&fieldIds=frgn_rate&fieldIds=pbr")
        res = requests.get(f"{url}?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn%3F%26page%3D{i}&fieldIds=quant&fieldIds=market_sum&fieldIds=per&fieldIds=roe&fieldIds=frgn_rate&fieldIds=pbr")
        data = BeautifulSoup(res.text,"lxml")
        #contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child(2) > td:nth-child(2) > a
        #contentarea > div.box_type_l > table.type_2 > tbody > tr
        tableHead = data.select("#contentarea > div.box_type_l > table.type_2 > thead")
        tableBody = data.select("#contentarea > div.box_type_l > table.type_2 > tbody > tr")
        
        if tableBody is None:
            break
        
        for row in tableBody:
            tableCell = row.find_all("td")
            if (not "blank" in str(tableCell)) and (not "division_line" in str(tableCell)):
                document = {
                    "stockName" : tableCell[1].getText(),
                    "code": tableCell[1].find("a")["href"].split("=")[1],
                    "price":  tableCell[2].getText(),
                    "per":  tableCell[9].getText(),
                    "roe":  tableCell[10].getText(),
                    "pbr":  tableCell[11].getText(),
                }
                print(document)
        
    
    #https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1&page=1

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
    get_stock_list("https://finance.naver.com/sise/field_submit.nhn")
    # es = Elasticsearch(
    # hosts=[{'host': "localhost", 'port': "9200"}])
    
    # for etf in etfTargets:
    #     try:
    #         documents = []
    #         etfData = get_etf_info(etf)
    #         document = {
    #            '_index': "etf-search-latest",
    #            '_source': etfData,
    #            '_id': etf
    #         }
    #         documents.append(document)
    #         helpers.bulk(es, documents)
    #     except Exception as e:
    #         logging.info(e)
    
if __name__ == "__main__":
    # execute only if run as a script
    main()
