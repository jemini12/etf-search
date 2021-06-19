import requests
import datetime
import json
import logging

from elasticsearch import Elasticsearch, helpers
from config import Config 
from bs4 import BeautifulSoup

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
                    '_index': "stock-data-latest",
                    '_source': stockData,
                    '_id': code
                }
                logging.info(f"STOCK ID [{code}] info gathered from NAVER stock")
                logging.info(document)
                documents.append(document)
    return documents
        
def main():
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
    logging.info("stock crawling start")
    #https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0
    #https://finance.naver.com/sise/field_submit.nhn?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn%3Fsosok%3D1%26page%3D3&fieldIds=quant&fieldIds=market_sum&fieldIds=per&fieldIds=roe&fieldIds=listed_stock_cnt&fieldIds=pbr
    es = Elasticsearch(
    hosts=[{'host': "localhost", 'port': "9200"}])
    try: 
        documents = get_stock_data("https://finance.naver.com/sise/field_submit.nhn",0)
        helpers.bulk(es, documents)
        documents = get_stock_data("https://finance.naver.com/sise/field_submit.nhn",1)
        helpers.bulk(es, documents)
        logging.info("stock crawling end")
    except Exception as e:
        logging.info(e)
    
if __name__ == "__main__":
    # execute only if run as a script
    main()
