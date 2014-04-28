import nltk
from nltk.tokenize.punkt import PunktWordTokenizer
Dictionary = open('SmallDictionary.txt','r')
import json
import codecs
import simplejson
import unicodedata
from bisect import bisect_left
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

setDictionary = set()
arrayDictionary = []
for line in Dictionary:
    line = eval(line)
    arrayDictionary.append(line)
    setDictionary.add(line[0])


in_file = "Coke_Tweets.txt"
f =  open(in_file,"r")
tweet_data = {}
i=0
for line in f:
    if i ==0:
        tweet_data = json.loads(line)
    else:
        tweets_to_add = json.loads(line)
        tweet_data.update(tweets_to_add)
    i += 1


f.close()


positiveTermsToCheck = [':-)',':-D',':D','=D','xD','(^_^)',':)','I love','I really like', 'I really love']
negativeTermsToCheck = [':-(',':(','=(',':[',":'-(",":'(",'I hate','I really hate']

count = 0
numTweets = len(tweet_data.keys())
                
for id in tweet_data.keys():

    count = count+1
    unicodeTweet = tweet_data[id]['text']
    tweet = tweet_data[id]['text']
    tweet = tweet.encode('utf-8')
    tweet = tweet.lower()    

    if count % 500  == 0:
        percent = round(float(count)/float(numTweets)*100,2)
        print ("progress:  " + str(count) + " of " + str(numTweets) + " gives " + str(percent) +"% " ) 

    tweet = (sent_detector.tokenize(tweet.strip()))
    text = []
    
    for i in range(0,len(tweet)):
        text.append(nltk.word_tokenize(tweet[i]))

    goodScoreTotal = 0
    badScoreTotal = 0
    adjList = []

    """
    for sentence in text:
        taggedText = nltk.pos_tag(sentence)
        for x in range(0,len(taggedText)):
            temp = taggedText[x]
            if temp[1] == "JJ":
                adjList.append(taggedText[x])
    """
    
    for sentence in text:
        for eachWord in sentence:
            adjList.append(eachWord)

    lenWord = len(adjList)

    for word in adjList:
        goodScore = 0
        badScore = 0

        if (word in setDictionary):
            element = filter(lambda x: word in x,arrayDictionary)
            if len(element)>0:
                goodScore = float(element[0][1])
                badScore = float(element[0][2])
            goodScoreTotal = goodScoreTotal + goodScore
            badScoreTotal = badScoreTotal + badScore
               
        tweet_data[id]['pos_score'] = goodScoreTotal
        tweet_data[id]['neg_score'] = badScoreTotal

        

    ispos = 0
    isneg = 0

    if any(emoticons in unicodeTweet for emoticons in positiveTermsToCheck): 
        ispos = 1
    if any(emoticons in unicodeTweet for emoticons in negativeTermsToCheck): 
        isneg = 1

    if ispos == 1 and isneg == 0:
        tweet_data[id]['identifier'] = 1
    elif ispos == 0 and isneg == 1:
        tweet_data[id]['identifier'] = -1        

           
out_file = 'Coke_Tweets_With_Sentiment_Full.txt'
outfile = open(out_file,'w')
json.dump(tweet_data, outfile)
outfile.close()


    

        
    
