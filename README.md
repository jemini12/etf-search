## ETF SEARCH ENGINE
This is search engine for etfsearch.info

### INDEX FOR SEARCH ENGINE
```
{
  "etf-search-v4" : {
    "mappings" : {
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
            "stockPortion" : {
              "type" : "float"
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
        "stockName" : {
          "type" : "keyword"
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
