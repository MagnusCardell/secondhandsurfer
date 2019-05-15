from flask import Blueprint,render_template,request,jsonify
import requests,json

# creating a Blueprint class
search_blueprint = Blueprint('search',__name__,template_folder="templates")
search_term = ""


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
        print("-----------------Calling search Result----------")
        search_term = request.form["input"]
        print("Search Term:", search_term)
        payload = {
          "query": {
            "query_string": {
              "analyze_wildcard": True,
              "query": str(search_term),
              "fields": ["topic", "title", "url", "labels"]
            }
          },
          "size": 50,
          "sort": [ ]
        }
        payload = json.dumps(payload)
        url = "http://elasticsearch:9200/hacker/tutorials/_search"
        response = requests.request("GET", url, data=payload, headers=headers)
        response_dict_data = json.loads(str(response.text))
        return json.dumps(response_dict_data)



