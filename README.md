## ETF SEARCH ENGINE
This is search engine for etfsearch.info

### INDEX FOR SEARCH ENGINE
```
{
  "etf-search-v4" : {
    "aliases" : {
      "etf-search-latest" : { }
    },
    "mappings" : {
      "runtime" : {
        "pbrAvg" : {
          "type" : "double",
          "script" : {
            "source" : """
            def pbrAvg = null;
            if (params['_source']['etfElements'].size() > 0){
              float totalPortion = 0;
              float pbrSum = 0;
              
              for (int i = 0; i < params['_source']['etfElements'].size(); i++){
                if (params['_source']['etfElements'][i]['stockPortion'] != null && params['_source']['etfElements'][i]['pbr'] != null){
                  if (params['_source']['etfElements'][i]['pbr'] > 0) {
                  pbrSum += (params['_source']['etfElements'][i]['stockPortion'] * params['_source']['etfElements'][i]['pbr']);
                  totalPortion += params['_source']['etfElements'][i]['stockPortion'];
                  }
                }
              }
              pbrAvg = pbrSum/totalPortion;
            }
            emit(pbrAvg);
          """,
            "lang" : "painless"
          }
        },
        "perAvg" : {
          "type" : "double",
          "script" : {
            "source" : """
            def perAvg = null;
            if (params['_source']['etfElements'].size() > 0) {
              float totalPortion = 0;
              float perSum = 0;
              
              for (int i = 0; i < params['_source']['etfElements'].size(); i++){
                if (params['_source']['etfElements'][i]['stockPortion'] != null && params['_source']['etfElements'][i]['per'] != null){
                  if (params['_source']['etfElements'][i]['per'] > 0) {
                    perSum += (params['_source']['etfElements'][i]['stockPortion'] * params['_source']['etfElements'][i]['per']);
                    totalPortion += params['_source']['etfElements'][i]['stockPortion'];
                  }
                }
              }
              perAvg = perSum/totalPortion;
            }
            emit(perAvg);
            // params['_source']['etfElements'].size()
          """,
            "lang" : "painless"
          }
        },
        "roeAvg" : {
          "type" : "double",
          "script" : {
            "source" : """
            def roeAvg = null;
            if (params['_source']['etfElements'].size() > 0){
              float totalPortion = 0;
              float roeSum = 0;
              
              for (int i = 0; i < params['_source']['etfElements'].size(); i++){
                if (params['_source']['etfElements'][i]['stockPortion'] != null && params['_source']['etfElements'][i]['roe'] != null){
                  if (params['_source']['etfElements'][i]['roe'] > 0) {
                  roeSum += (params['_source']['etfElements'][i]['stockPortion'] * params['_source']['etfElements'][i]['roe']);
                  totalPortion += params['_source']['etfElements'][i]['stockPortion'];
                  }
                }
              }
              roeAvg = roeSum/totalPortion;
            }
            emit(roeAvg);
          """,
            "lang" : "painless"
          }
        }
      },
      "properties" : {
        "etfDescription" : {
          "type" : "text",
          "analyzer" : "nori_analyzer"
        },
        "etfElements" : {
          "type" : "nested",
          "properties" : {
            "code" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "pbr" : {
              "type" : "float"
            },
            "per" : {
              "type" : "float"
            },
            "roe" : {
              "type" : "float"
            },
            "stockMarketCap" : {
              "type" : "long"
            },
            "stockName" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              },
              "analyzer" : "nori_analyzer"
            },
            "stockNetIncome" : {
              "type" : "long"
            },
            "stockPortion" : {
              "type" : "float"
            },
            "stockQuant" : {
              "type" : "long"
            }
          }
        },
        "etfName" : {
          "type" : "text",
          "analyzer" : "nori_analyzer"
        },
        "etfProfits" : {
          "type" : "nested",
          "properties" : {
            "etfProfit12M" : {
              "type" : "float"
            },
            "etfProfit1M" : {
              "type" : "float"
            },
            "etfProfit3M" : {
              "type" : "float"
            },
            "etfProfit6M" : {
              "type" : "float"
            }
          }
        },
        "etfTypes" : {
          "type" : "nested",
          "properties" : {
            "etfType" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              },
              "analyzer" : "nori_analyzer"
            }
          }
        },
        "timestamp" : {
          "type" : "date"
        }
      }
    },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "1",
        "provided_name" : "etf-search-v4",
        "creation_date" : "1624199261636",
        "analysis" : {
          "analyzer" : {
            "nori_analyzer" : {
              "type" : "custom",
              "tokenizer" : "korean_nori_tokenizer"
            }
          },
          "tokenizer" : {
            "korean_nori_tokenizer" : {
              "type" : "nori_tokenizer",
              "decompound_mode" : "mixed"
            }
          }
        },
        "number_of_replicas" : "1",
        "uuid" : "7EigMlIESkO3eLayzycZBQ",
        "version" : {
          "created" : "7120099"
        }
      }
    }
  }
}



{
  "stock-data-v1" : {
    "aliases" : {
      "stock-data-latest" : { }
    },
    "mappings" : {
      "properties" : {
        "code" : {
          "type" : "keyword"
        },
        "pbr" : {
          "type" : "float"
        },
        "per" : {
          "type" : "float"
        },
        "price" : {
          "type" : "long"
        },
        "roe" : {
          "type" : "float"
        },
        "stockMarketCap" : {
          "type" : "long"
        },
        "stockName" : {
          "type" : "keyword",
          "fields" : {
            "text" : {
              "type" : "text"
            }
          }
        },
        "stockNetIncome" : {
          "type" : "long"
        },
        "stockQuant" : {
          "type" : "long"
        },
        "timestamp" : {
          "type" : "date"
        }
      }
    },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "1",
        "provided_name" : "stock-data-v1",
        "creation_date" : "1624032827966",
        "number_of_replicas" : "1",
        "uuid" : "aEKZYqCjQFaSQl-1AtHKlw",
        "version" : {
          "created" : "7120099"
        }
      }
    }
  }
}
```

### ETF SEARCH CRAWLER
```
etf.py : get etf information and update document to elasticsearch
stock.py : get stock information and update document to elasticsearch
scripts/init.py : get etf, stock information and create document to elasticsearch
```
