import math
import random
import json
import pprint
import sys
import pandas
import numpy as np
import copy

"""
This Function applies the linear classifier generated in matlab using the identifier based training set to the broader dataset. The output is consolidated on a daily basis and saved to a csv file. Before using, ensure that the linear classifier coefficients are correct for the particular company you are studying. Then just run the function with the input file as the first argument and the output file as the second.
"""

# Linear classifier coefficients (MAKE SURE CORRECT FOR TARGET COMPANY!):
coeff_1 = -0.809903851
coeff_2 = 2.011053658
Intercept = -1.8853791
Threshold = 0.689265296

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
			print 'done ' + str(i)
		del tweet_data[id]['text']
		tweet_data[id]['timestamp'] = tweet_data[id]['timestamp'][4:10]

		if tweet_data[id]['identifier'] != 0:
			tweet_data[id]['pos_identifier'] = 0
			tweet_data[id]['neg_identifier'] = 0			
			if tweet_data[id]['identifier'] == 1:
				tweet_data[id]['pos_identifier'] = 1
			if tweet_data[id]['identifier'] == -1:
				tweet_data[id]['neg_identifier'] = 1
		
		elif tweet_data[id]['pos_score'] != 0 or tweet_data[id]['neg_score'] != 0:
			tweet_data[id]['pos_identifier'] = 0
			tweet_data[id]['neg_identifier'] = 0			
			log_r = 1/(1+math.exp(Intercept + coeff_1 * tweet_data[id]['pos_score'] + coeff_2 * tweet_data[id]['neg_score']))
			if log_r > Threshold:
				tweet_data[id]['pos_identifier'] = 1
			else:
				tweet_data[id]['neg_identifier'] = 1
		else:
			del tweet_data[id]
		i += 1
		
	print 'Building Dataframe.'
	df = pandas.DataFrame.from_dict(tweet_data,orient='index')
	
	print 'Building Output.'
	output = pandas.DataFrame({'count_of_scored' : df.groupby('timestamp').count()['timestamp']})
	print 'totals.'	
	output = output.join(pandas.DataFrame({'total_pos' : df.groupby('timestamp').sum()['pos_score']}))
	output = output.join(pandas.DataFrame({'total_neg' : df.groupby('timestamp').sum()['neg_score']}))
	print 'mean'
	output = output.join(pandas.DataFrame({'mean_pos' : df.groupby('timestamp').mean()['pos_score']}))
	output = output.join(pandas.DataFrame({'mean_neg' : df.groupby('timestamp').mean()['neg_score']}))
	print 'Identifiers.'
	output = output.join(pandas.DataFrame({'pos_identifier' : df.groupby('timestamp').sum()['pos_identifier']}))
	output = output.join(pandas.DataFrame({'neg_identifier' : df.groupby('timestamp').sum()['neg_identifier']}))

	print 'Saving Output.'
	output['Adj_Days'] = output.index
	output['Adj_Days'] = output['Adj_Days'].apply(day_Label)
	output.set_index('Adj_Days',drop = True,inplace=True)
	output.sort_index(axis=0,ascending=True,inplace=True)
	output.to_csv(out_file)
		
in_file = sys.argv[1]
out_file = sys.argv[2]
tweet_read(in_file,out_file)
