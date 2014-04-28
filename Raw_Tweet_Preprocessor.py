import math
import random
import json
import pprint
import sys
import string

"""
Instructions:
	1.) Split input into c.100MB files in order to enable easy file open/close - using 'split -b 100m filename' in the command line. Files will be titled in ascending alphabetical order, starting at xaa.
	2.) Uncomment appropriate key words option depending on target company
	3.) Run Raw_Tweet_Preprocessor with the following arguments:
		1: Address of directory containing split files.
		2: Output file name / address
		3: The last file in the directory + 1. i.e. if last file is called xbe, enter xbf.
"""

# Select key words to filter tweets:

key_words = ['Coca-Cola','Coca Cola','Coke']
"""
key_words = ['McDonalds','McDonald','McDonal','McD']

key_words = ['Nike']
"""

# Function reads in raw_twitter data and outputs just the text characteristic of the english tweets only
def twitter_read(in_file,remainder):
	print "Reading in raw twitter data."
	f =  open(in_file,"r")
	raw_data = f.read()
	f.close()
	tweets = raw_data.split("}{")
	i = 0
	data = []
	for tweet in tweets:	
		if i == 0:
			tweet = remainder + tweet + "}"
			tweet = unicode(tweet,errors='ignore')
			data.append(json.loads(tweet))
		elif i == (len(tweets) - 1):
			tweet = "{" + tweet
			remainder = tweet
		else:
			tweet = "{" + tweet + "}"
			tweet = unicode(tweet,errors='ignore')
			data.append(json.loads(tweet))
		i += 1
	
	print "Extracting text data from English tweets."
	en_tweets = {}
	tweet_count = 0
	en_tweet_count = 0
	for i in data:
		tweet_count += 1
  		if 'lang' in i.keys() and i['lang'] == 'en' and 'text' in i.keys():
			id = i['id']
			en_tweets[id] = {}
			en_tweets[id]['timestamp'] = i['created_at']
			en_tweets[id]['text'] = i['text']
			en_tweets[id]['followers'] = i['user']['followers_count']
			en_tweets[id]['pos_score'] = 0.0
			en_tweets[id]['neg_score'] = 0.0
			en_tweets[id]['inf_score'] = 0.0
			en_tweets[id]['identifier'] = 0
			en_tweet_count += 1

	print "Total Tweets: ", tweet_count
	print "English Tweets: ", en_tweet_count

	print "counting key words."	
	key_words_count = 0
	unmapped = []
	unmapped_count = 0

	for x in en_tweets.keys():
		unmapped_Flag = True
		for word in key_words:
			if word.lower() in en_tweets[x]['text'].lower():
				key_words_count += 1
				unmapped_Flag = False
				break
		if unmapped_Flag == True:
			unmapped.append(en_tweets[x]['text'])
			del en_tweets[x]
			unmapped_count += 1

	# Uncomment to view / check unmapped tweets
	# pprint.pprint(unmapped)

	# Uncomment to view / check selected tweets
	# pprint.pprint(en_tweets)
	print "key words count: ", key_words_count
	
	print "saving to file:"
 	json.dump(en_tweets, outfile)
	
	return remainder

in_directory = sys.argv[1]
out_file = sys.argv[2]
end_file = sys.argv[3]

outfile = open(out_file,'w')
tr = ""
alphabet = list(string.ascii_lowercase)
for letter_1 in alphabet:
	for letter_2 in alphabet:
		file_id = 'x' + letter_1 + letter_2
		print "File ID: ", file_id
		if file_id == end_file:
			break
		if file_id != 'xaa':
			outfile.write('\n')
		tr = twitter_read(in_directory + '/' + file_id,tr)
	if file_id == end_file:
		break

outfile.close()
