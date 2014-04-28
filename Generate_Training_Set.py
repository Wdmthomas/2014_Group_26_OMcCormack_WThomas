import math
import random
import json
import pprint
import sys
import pandas
import numpy as np
import copy

"""
Function reads scored tweets from a json format, selecting tweets that have both an identifier and a sentiment lexicon score.
The selected tweets are then saved in a dataframe format, ready to be used in matlab as a training set to train a better tweet classifier.
To use this program, simply run it using the input data .txt file as the first argument and the desired output.csv file as the second argument.
"""

def tweet_read(in_file,out_file):

	print 'Reading file'
	f =  open(in_file,"r")
	tweet_data = {}
	i = 0
	for line in f:
		if i == 0:
			tweet_data = json.loads(line)
		else:
			tweets_to_add = json.loads(line)
			tweet_data.update(tweets_to_add)
		i += 1

	f.close()
	
	i = 0
	print 'Iterating through keys'	
	for id in tweet_data.keys():
		if i%200000 == 0:
			print 'done ' + str(i)
		if tweet_data[id]['identifier'] == 0:
			del tweet_data[id]
		elif tweet_data[id]['pos_score'] == 0 and tweet_data[id]['neg_score'] == 0:
			del tweet_data[id]
		else:
			tweet_data[id]['timestamp'] = tweet_data[id]['timestamp'][4:13]
			del tweet_data[id]['text']
			tweet_data[id]['pos_identifier'] = 0
			tweet_data[id]['neg_identifier'] = 0			
			if tweet_data[id]['identifier'] == 1:
				tweet_data[id]['pos_identifier'] = 1
			if tweet_data[id]['identifier'] == -1:
				tweet_data[id]['neg_identifier'] = 1
			if tweet_data[id]['followers'] > 0:
				tweet_data[id]['inf_score'] = math.log10(tweet_data[id]['followers'])
		i += 1
	
	print 'Building Dataframe.'
	df = pandas.DataFrame.from_dict(tweet_data,orient='index')
	print 'pos_follower_weight'
	df['pos_follower_weight'] = df['pos_score'] * df['followers']
	print 'neg_follower_weight'
	df['neg_follower_weight'] = df['neg_score'] * df['followers']
	print 'norm_pos_follower_weight'
	df['norm_pos_follower_weight'] = df['pos_score'] * df['inf_score']
	print 'norm_neg_follower_weight'
	df['norm_neg_follower_weight'] = df['neg_score'] * df['inf_score']
	
	print 'Saving Output to File.'
	df.to_csv(out_file)
			
in_file = sys.argv[1]
out_file = sys.argv[2]
tweet_read(in_file,out_file)
