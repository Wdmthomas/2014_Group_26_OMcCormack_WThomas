import math
import random
import json
import pprint
import sys
import pandas
import numpy as np
import copy

"""
This Function consolidates the results from program 2 on a daily basis, providing outputs in .csv format that can then be used in matlab to attempt to predict the fluctuations in the stock market. Run the function with the input file as the first argument and the output file as the second.
"""

# Maps Timestamps onto days:
def day_Label(Text_String):
	if Text_String[0:3] == 'Jan':
		month = '1'
	elif Text_String[0:3] == 'Feb':
		month = '2'
	elif Text_String[0:3] == 'Mar':
		month = '3'
	else:
		print Text_String[0:3], 'error'

	return int(month + Text_String[4:6])

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
		if i%100000 == 0:
			print 'Done ' + str(i)
		if tweet_data[id]['pos_score'] == 0 and tweet_data[id]['neg_score'] == 0:
			del tweet_data[id]
		else:
			tweet_data[id]['timestamp'] = tweet_data[id]['timestamp'][4:10]
			del tweet_data[id]['text']
			del tweet_data[id]['identifier']
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
	
	print 'Building Output.'
	output = pandas.DataFrame({'count_of_scored' : df.groupby('timestamp').count()['timestamp']})
	print 'totals.'	
	output = output.join(pandas.DataFrame({'total_pos' : df.groupby('timestamp').sum()['pos_score']}))
	output = output.join(pandas.DataFrame({'total_neg' : df.groupby('timestamp').sum()['neg_score']}))
	print 'weighted totals'
	output = output.join(pandas.DataFrame({'total_pos_weighted' : df.groupby('timestamp').sum()['pos_follower_weight']}))
	output = output.join(pandas.DataFrame({'total_neg_weighted' : df.groupby('timestamp').sum()['neg_follower_weight']}))
	print 'weighted + normalised totals'
	output = output.join(pandas.DataFrame({'total_pos_weighted_norm' : df.groupby('timestamp').sum()['norm_pos_follower_weight']}))
	output = output.join(pandas.DataFrame({'total_neg_weighted_norm' : df.groupby('timestamp').sum()['norm_neg_follower_weight']}))
	print 'mean'
	output = output.join(pandas.DataFrame({'mean_pos' : df.groupby('timestamp').mean()['pos_score']}))
	output = output.join(pandas.DataFrame({'mean_neg' : df.groupby('timestamp').mean()['neg_score']}))
	print 'weighted mean'
	output = output.join(pandas.DataFrame({'mean_pos_weighted' : df.groupby('timestamp').mean()['pos_follower_weight']}))
	output = output.join(pandas.DataFrame({'mean_neg_weighted' : df.groupby('timestamp').mean()['neg_follower_weight']}))
	print 'weighted + normalised mean'
	output = output.join(pandas.DataFrame({'mean_pos_weighted_norm' : df.groupby('timestamp').mean()['norm_pos_follower_weight']}))
	output = output.join(pandas.DataFrame({'mean_neg_weighted_norm' : df.groupby('timestamp').mean()['norm_neg_follower_weight']}))
	
	print 'Saving Output.'
	output['Adj_Days'] = output.index
	output['Adj_Days'] = output['Adj_Days'].apply(day_Label)
	output.set_index('Adj_Days',drop = True,inplace=True)
	output.sort_index(axis=0,ascending=True,inplace=True)
	output.to_csv(out_file)
		
in_file = sys.argv[1]
out_file = sys.argv[2]
tweet_read(in_file,out_file)
