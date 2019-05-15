from elasticsearch import Elasticsearch
from flask import Blueprint,render_template,request,jsonify
import requests,json

# creating a Blueprint class
search_blueprint = Blueprint('search',__name__,template_folder="templates")
search_term = ""
es = Elasticsearch(hosts=[{"host":'elasticsearch'}]) 

headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Access-Control-Allow-Origin': '*'
}

@search_blueprint.route("/",methods=['GET','POST'],endpoint='index')
def index():
  return connect_elasticsearch()

@search_blueprint.route("/search",methods=['POST'],endpoint='search')
def search():
    if request.method == 'POST':
        req_data = request.get_json()
        search_data = req_data["params"]
        search_term = search_data["term"]
        print("Search Term:", search_term)
        payload = {
          "query": {
            "query_string": {
              "analyze_wildcard": True,
              "query": str(search_term),
              "fields": ["title", "description", "size", "gender", "color", "price", "location"]
            }
          },
          "size": 50,
          "sort": [ ]
        }
        payload = json.dumps(payload)
        url = "http://localhost:9200/blocket/items/_search"
        response = requests.request("GET", url, data=payload, headers=headers)
        #Filtering/sorting/ and all that novelty stuff here?
        
        response_dict_data = json.loads(str(response.text))
        return json.dumps(response_dict_data)


#This should not exist in production settings
@search_blueprint.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
    response.headers['Access-Control-Expose-Headers'] = '*'
    return response