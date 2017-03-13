from django.http import HttpResponse
from django.shortcuts import render_to_response, render, redirect
from elasticsearch import Elasticsearch
import json
from django.http import JsonResponse
import requests
from django.core import serializers

def index(request):
    return render(request, 'index.html')

def search(request):
    reqid = request.GET.get('q', '')
    r = requests.get('http://search-tweetproject-rfj3fbaymnut5knm7e7apux344.us-west-2.es.amazonaws.com/tweetmap/tweetdata/_search?size=10000&q='+str(reqid))
    parsed_json = json.loads(r.content)
    hits = parsed_json['hits']['total']
    outarray = [[]]
    i = 1
    while i<hits:
        outarray.append([parsed_json['hits']['hits'][i]['_source']['geo']['coordinates'][0],parsed_json['hits']['hits'][i]['_source']['geo']['coordinates'][1],parsed_json['hits']['hits'][i]['_source']['text'],parsed_json['hits']['hits'][i]['_source']['user']['name']])
        i = i+1
    # es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    # reqid = request.GET.get('q', '')
    # res = es.search(index = 'tweetmap', size=1, body={"query": {"match_all": {}}})

    # print(" response: '%s'" % (res))
    # print(reqid)
    # jsondata = json.loads(json.dumps(es.get(index='tweetmap', doc_type='tweetdata', id=reqid)))
    jsondata = json.dumps(outarray)
    # # print(jsondata)
    # # response = HttpResponse(jsondata, content_type="application/json")
    # # print(response)
    return JsonResponse(outarray, safe=False)

    # return render('a')
    # return render(request, 'index1.html')
    # d = json.dumps(outarray)
    # data = {'d':d}
    # return render_to_response('index.html',data)
    # print(jsondata)
    # return render_to_response('index.html', {'array1': outarray})
