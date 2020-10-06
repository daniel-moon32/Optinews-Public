from flask import Flask 
import requests
from newsapi import NewsApiClient
from monkeylearn import MonkeyLearn

ml = MonkeyLearn('4c67b4c62c390c6c14cde310bda788b0a3fe0639')
modelid = "cl_pi3C7JiL"
newsapi = NewsApiClient(api_key='***REMOVED***')
top_headlines = newsapi.get_top_headlines(country='us',
                                          language='en')

articles = []
data = []


for i in range(len(top_headlines["articles"])):
    data = [top_headlines["articles"][i]["content"]]
    if data == [None]:
        data = [top_headlines["articles"][i]["description"]]
    if data == [None]:
        data = [top_headlines["articles"][i]["title"]]
    result = ml.classifiers.classify(modelid, data)
    if(result.body[0]["classifications"][0]["tag_name"] == "Positive" and result.body[0]["classifications"][0]["confidence"] >= .7):
        articles.append(top_headlines["articles"][i])

print(articles)

app = Flask(__name__)

@app.route('/')
def firstarticle():
    return articles[0]