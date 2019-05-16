

import ad
from preprocessing import *
import ast
import json  
import os
#import requests
from elasticsearch import Elasticsearch
import numpy as np
import math
import statistics
import operator
#def indexing(path):
    

#return descriptions


def relevance_score(ad, query, color):

    """
    depends on color - 0.2 , similarity measure - 0.4 , date posted - 0.1 , condition - 0.1, match with size 0.2

    If color matches, then get 1. otherwise zero
    similarity measure - dot product divided by number of words in query
    date posted - less than a month = 1
                  less than 4 month = 0.5
                  more than 4 month = 0
    condition = 0 to 1
    size match will get another 1
    """
    if len([c for c in color if c in ad['color']]) > 0:
        c_score = 1
    else:
        c_score = 0
    if ad['num_days'] < 31:
        d_score = 1
    elif ad['num_days'] < 121:
        d_score = 0.6
    else:
        d_score = 0.1
    condition_score = ad['condition']
    #similarity measure
    s_score = 0
    for k in query:
        for j in ad['info']:
            if k == j:
                """ Update this command """
                hits = es.search(index='clothes',doc_type='item',body={'query':k})['hits']['total']
                s_score  = s_score + (n_items/float(math.log10(hits)))^2
    
    s_score = s_score/len(query)
    score = float(0.2*c_score + 0.5*s_score + 0.2*condition_score + 0.1*d_score)
    return score



es = Elasticsearch()
path = 'data/'
#indexing(path)
##get query from frontend
descriptions = []
for filename in os.listdir(path):
    #read json file
    i = 0
    
    file = open(filename, "r")
    content = json.load(file)
    content = ast.literal_eval(content)
    content['description'] = content['description'].replace('\t','')
    content['description'] = content['description'].replace('\n','')
    #add code to initiate the id class
    item = ad(content['price'], content['size'], content['title'], content['description'], content['place'], content['indate'])
    descriptions.append(' '.join(item.tokens))
    #add the condition, number of days and color to json file
    content['condition'] = item.condition 
    content['color'] = item.colors
    content['num_days'] = item.days
    content['info'] = descriptions[i]
    content['id'] = i
    content['score'] = 0
    es.index(index="clothes", doc_type='item', id=i, body=content)
    i = i+1
    file.close()

n_items = len(descriptions)

while (getting_queries):
    queries = queries.split(',')
    num_q = len(queries)
    ##preprocessing of queries
    colors = []
    processed_queries = []
    
    for i in num_q:
        processed_queries[i], colors[i] = find_color(queries[i])
        #processed_queries[i] = ' '.join(processed_queries[i])
    results = []
    for n in range(num_q):
        
        #q = ' '.join(processed_queries[n])
        list_ids = []
        for k in processed_queries[n]:
        list_ids = list_ids + es.search(index='clothes',doc_type='item',body={'query':k})
        
        for i in range(len(descriptions)):
            """ Update this command """
            ad = es.get(index = 'clothes', doc_type = 'item', id = i)["_source"]
            score = relevance_score(ad, processed_queries[n], colors[n])
            es.update(index='clothes', doc_type = 'item', id = ad['id'], body={"doc": {"score" : score}})
        
        """ Update this search function """
        
        res = es.search(index='clothes', doc_type = 'item', id = ad['id'], body={' '.join(processed_queries[n])}, size = 10)
        results.append(res)
    
    #now bundling
    
    if num_q > 1:
        bundling_score = []
        sizes = []
        for i in range(num_q):
            sizes.append(len(results[i]))
        scores = np.zeros(tuple(sizes))
        scores1 =  {} #np.zeros(tuple(sizes))
        it = np.nditer(scores, flags = ['multi_index'])
        while not it.finished:
            current_index = it.multi_index
            """ update this line properly to get score from results  """
            scores1[current_index] = [0.6*statistics.mean([results[i]['hits'][current_index[i]]['score'] for i in range(num_q)])]
            dist = least_distance([results[i]['hits'][current_index[i]]['location'] for i in range(num_q)])
            scores1[current_index].append(dist)
            it.iternext()
        dist_list = [float(scores1[key][1]) for key in scores1.keys()]
        dist_list.sort()
        lenth = len(dist_list)
        n1 = dist_list[int(lenth/4)]
        n2 = dist_list[int(lenth/2)]
        n3 = dist_list[int(3*lenth/4)]
        for key in scores1.keys():
            if float(scores1[key][1]) < n1:
                scores1[key][1] = 1
            elif n1 < float(scores1[key][1]) < n2:
                scores1[key][1] = 0.6
            elif n2 < float(scores1[key][1]) < n3:
                scores1[key][1] = 0.4
            elif float(scores1[key][1]) > n3:
                scores1[key][1] = 0.1
            scores1[key][2] = scores1[key][0] + 0.4*scores1[key][1]
            
        bundle_ids = sorted(scores1.items(), key = lambda k:k[1][2])
        
                            
        

































