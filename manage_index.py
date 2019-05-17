import requests
import json

def check_if_index_is_present(url):
    response = requests.request("GET", url, data="")
    json_data = json.loads(response.text)
    return json_data


if __name__ == "__main__":
    # url = "http://localhost:9200/_template/search_engine_template/"
    # response = requests.request("GET", url, data="")
    # if(len(response.text)>2):
    #     print("1. Deleted template: search_engine_template")
    #     response_delete = requests.request("DELETE", url)
    # payload = {
    #       "template": "blocket",
    #       "settings": {
    #         "number_of_shards": 1
    #       },
    #       "mappings": {
    #         "items":{
    #             "_source": {
    #                 "enabled": True
    #             },
    #             "properties":{
    #                 "title":{
    #                     "type":"text"
    #                 },
    #                 "description":{
    #                     "type":"text"
    #                 },
    #                 "size":{
    #                     "type":"text"
    #                 },
    #                 "gender":{
    #                     "type":"text"
    #                 },
    #                 "color":{
    #                     "type":"text"
    #                 },
    #                 "price":{
    #                     "type":"text"
    #                 },
    #                 "localtion":{
    #                     "type":"text"
    #                 }
    #             }
    #         }

    #       }
    # }
    # payload = json.dumps(payload)
    # headers = {
    #         'Content-Type': "application/json",
    #         'cache-control': "no-cache"
    #     }
    # response = requests.request("PUT", url, data=payload, headers=headers)
    # if (response.status_code == 200):
    #     print("2. Created a new template: search_engine_template")

    # url = "http://localhost:9200/blocket"
    # json_data = check_if_index_is_present(url)

    # if(not 'error' in json_data):
    #     print("3. Deleted an index: blocket")
    #     response = requests.request("DELETE", url)

    # response = requests.request("PUT", url)
    # if (response.status_code == 200):
    #     print("4. Created an index: blocket")
    
    url = "http://localhost:9200/_template/search_engine_template/"
    response = requests.request("GET", url, data="")
    if(len(response.text)>2):
        print("1. Deleted template: search_engine_template")
        response_delete = requests.request("DELETE", url)
    payload = {
          "template": "blocket2",
          "settings": {
            "number_of_shards": 1
          },
          "mappings": {
            "items":{
                "_source": {
                    "enabled": True
                },
                "properties":{
                    "title":{
                        "type":"text"
                    },
                    "description":{
                        "type":"text"
                    },
                    "size":{
                        "type":"text"
                    },
                    "gender":{
                        "type":"text"
                    },
                    "color":{
                        "type":"text"
                    },
                    "price":{
                        "type":"float"
                    },
                    "localtion":{
                        "type":"text"
                    },
                    "condition":{
                        "type":"text"
                    },
                    "num_days":{
                        "type":"text"
                    },
                    "info":{
                        "type":"text"
                    },
                    "id":{
                        "type":"text"
                    },
                    "score":{
                        "type":"float"
                    }
                }
            }

          }
    }
    payload = json.dumps(payload)
    headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
    response = requests.request("PUT", url, data=payload, headers=headers)
    if (response.status_code == 200):
        print("2. Created a new template: search_engine_template")

    url = "http://localhost:9200/blocket2"
    json_data = check_if_index_is_present(url)

    if(not 'error' in json_data):
        print("3. Deleted an index: blocket2")
        response = requests.request("DELETE", url)

    response = requests.request("PUT", url)
    if (response.status_code == 200):
        print("4. Created an index: blocket2")




