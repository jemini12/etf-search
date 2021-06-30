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

from conf.config import Config 
import module.etfModule as etfmodule
import module.stockModule as stockmodule

def etfInit():
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
    etfTargets = etfmodule.get_etf_list(Config.URL_NAVER_ETF_LIST)
    #etfTargets = ["105780"] #for test
    es = Elasticsearch(
        hosts=[{'host': Config.ES_HOST, 'port': "9200"}])
    logging.info("etf crawling initialize start")
    documents = etfmodule.get_etf_info(etfTargets,es,"index")
    try:      
        helpers.bulk(es, documents)
    except Exception as e:
        logging.info(e)
        
    logging.info("etf crawling initialize end")
    
def stockInit():
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
        hosts=[{'host': Config.ES_HOST, 'port': "9200"}])
    try: 
        # 0 = KOSPI
        documents = stockmodule.get_stock_data(Config.URL_NAVER_STOCK_LIST,0,"index")
        helpers.bulk(es, documents)
        # 1 = KOSDAQ
        documents = stockmodule.get_stock_data(Config.URL_NAVER_STOCK_LIST,1,"index")
        helpers.bulk(es, documents)
        logging.info("stock crawling initialize end")
    except Exception as e:
        logging.info(e)
    
if __name__ == "__main__":
    # execute only if run as a script
    if len(sys.argv) < 2:
        print("init.py [etf|stock]")
        sys.exit()
        
    if sys.argv[1] == "etf":
        etfInit()
    elif sys.argv[1] == "stock":
        stockInit()
    else:
        print("init.py [etf|stock]")
        
