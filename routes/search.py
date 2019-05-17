from elasticsearch import Elasticsearch
from flask import Blueprint,render_template,request,jsonify
import requests,json
from .algorithms import manager as manager
from elasticsearch_dsl import connections, Search
from elasticsearch import Elasticsearch

# creating a Blueprint class
search_blueprint = Blueprint('search',__name__,template_folder="templates")
search_term = ""
#es = Elasticsearch(hosts=[{"host":'elasticsearch'}]) 
es=Elasticsearch([{'host':'localhost','port':9200}])


headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Access-Control-Allow-Origin': '*'
}

@search_blueprint.route("/",methods=['GET','POST'],endpoint='index')
def index():
  return

@search_blueprint.route("/search",methods=['POST'],endpoint='search')
def search():
    if request.method == 'POST':
        req_data = request.get_json()
        search_data = req_data["params"]
        search_term = search_data["term"]

        """ all_res = []
        for q in format_query(search_term):
          res= es.search(index='blocket2', body={ "query": {
            "function_score": {
                "functions": [
                    {
                    "field_value_factor": {
                        "field": "price",
                        "factor": 1,
                        "missing": 1
                    }
                    }
                ],
                "query": {
                    "match": {"_all": q}
                },
                "boost_mode": "replace"
                }
            }} )
        all_res.append(res) """



        res2 = manager.new_query(es, search_term, headers)

        #response_dict_data = json.loads(res)
        return json.dumps(res2)


def format_query(query):
  q = query.split(',')
  return q

#This should not exist in production settings
@search_blueprint.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
    response.headers['Access-Control-Expose-Headers'] = '*'
    return response