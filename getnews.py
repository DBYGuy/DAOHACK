from graphene import ObjectType, Field
import spacy
import requests
import json
import pandas as pd
from __future__ import print_function
import time
import aylien_news_api
from aylien_news_api.rest import ApiException
from pprint import pprint
import re
from newsapi import NewsApiClient
import random


# Create an instance of the API class
sl = ["apecoin.eth"]

def parseCollection(col):

    x = json.loads(col)
    print (x)
    y = str(x['data']['space']['id'])
    print (y)
    qText = """query Proposals {
    proposals (where:{space: "apecoin.eth"}) {
    id
    title
    body
    start
    end
    author
    choices
    snapshot
    state
  }
}"""

    url = "https://hub.snapshot.org/graphql"
    r = requests.post(url, json={"query": qText})
    sickness = r.text
    return sickness




def getCollection(spaceList):

    for space in spaceList:
        qText = """query
                     Spaces {space (id: "apecoin.eth") {
                            id
                            name}}"""
        url = "https://hub.snapshot.org/graphql"
        r = requests.post(url, json={'query': qText})
        sickness = r.text

        return sickness



def keywordProposal(proposalText):

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(proposalText)
    processed = doc.ents
    rssKeywords = processed

    return rssKeywords

def userCollections(address):
    xx = getCollection(sl)
    yy = parseCollection(xx)
    bb = json.loads(yy)
    print(bb)

    return bb

def grabNews(proposals):
    print(proposals)
    for thing in proposals:
        wordTown = []
        dank = keywordProposal(prop['body'])
        dank = re.sub(r'(a|A)pe', ' ', str(dank)).split()

        wordTown.append([str(x) for x in dank])
    newsapi = NewsApiClient(api_key='02cab9231fe64ab2ac076688bf0be90f')

    all_articles = newsapi.get_everything(q='{}'.format(random.choice(wordTown[0][0:5])),
                                      from_param='2022-11-01',
                                      to='2022-12-12',
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)
    return all_articles

def main():

    slizzle = userCollections(sl)
    z = getCollection(slizzle)



    theNews = grabNews(z)

    return theNews
