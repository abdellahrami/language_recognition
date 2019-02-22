from keras.models import Sequential
from keras.layers import Dense
import numpy 
from sklearn.model_selection import train_test_split
from keras.models import model_from_json 
import os
import re
from sklearn.feature_extraction.text import CountVectorizer

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# Training parameters
batch_size = 1000
num_epochs = 35
val_split = 0.25

# load dataset
max_ngrams = 100;
while(True):
	print("Ngrams char[0] or word [1]:",end='')
	ht = int(input())
	if(ht==0):
		ngrams_type = 'char'
	else:
		ngrams_type = 'word'
	print("Enter min ngrams :",end='')
	minNgrams = int(input())
	print("Enter max ngrams :",end='')
	maxNgrams = int(input())

	path_plus = '_'+str(minNgrams)+'_'+str(maxNgrams)+'_'+ngrams_type


	# c_vec = CountVectorizer(ngram_range=(3, 3),encoding='utf-8',analyzer='char',max_features=100)

	c_vec = CountVectorizer(ngram_range=(minNgrams, maxNgrams),encoding='utf-8',analyzer=ngrams_type)


	def get_score(mylist, ngram,N):
	    for sub_list in mylist:
	        if ngram in sub_list:
	        	value = sub_list[0]/N
	        	if(value>0.0001):
	        		return value
	        	else:
	        		return 0


	lang_ngrams = []

	fd_ngram = open("./Ngrams/dict"+path_plus+".txt",'r',encoding='utf-8')
	lang_ngrams = [line.replace('\n','') for line in fd_ngram]


	df = open("predict_text.txt",'r',encoding='utf-8')
	lines = [line for line in df]
	to_rmv = []
	for i in range(len(lines)) :
		lines[i] = re.sub(r'^<[^*]*','',lines[i])
		lines[i] = re.sub(r'[^a-zA-Z0-9\s àâäæçèéêëîïôœùûüÀÂÄÆÇÈÉÊËÎÏÔŒÙÛÜö\'àèéìòùÀÈÉÌÒùáÁéÉíÍñÑóÓúÚüÜ¿¡«»€’"«»-ãáàâçéêíõóôúü]', '', lines[i])
		lines[i] = re.sub(r' +', ' ', lines[i])
		lines[i] = re.sub(r'^[^a-zA-Z0-9]+', '', lines[i])
		# lines[i] = lines[i].replace('\n','')
	for j in to_rmv:
		if j < len(lines):
			lines.pop(j)

	while '' in lines:
		lines.remove('')
	while ' ' in lines:
		lines.remove(' ')
	while '\n' in lines:
		lines.remove('\n')
	df.close()


	# script : calculate ngrams scores
	ngrams = c_vec.fit_transform(lines)

	vocab = c_vec.vocabulary_

	count_values = ngrams.toarray().sum(axis=0)

	N = sum(count_values)

	ngrams_file = sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True)
	X_pred = []
	vec = []
	for ngram in lang_ngrams:
		if any(ngram in sl for sl in ngrams_file):
			vec.append(get_score(ngrams_file,ngram,N))
		else:
			vec.append(0)
	if(len(vec)<400):
		vec += ['0']*(400-len(vec))
	X_pred.append(vec)
	X = numpy.array(X_pred)


	# load json and create model
	json_file = open('model'+path_plus+'.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	# load weights into new model
	loaded_model.load_weights("model"+path_plus+".h5")
	print("Loaded model from disk")
	 
	# evaluate loaded model on test data
	loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	langs_out = {'fr':[1,0,0,0],'es':[0,1,0,0],'pt':[0,0,1,0],'it':[0,0,0,1]}
	prediction_vct = loaded_model.predict(X)
	langs = list(langs_out.keys())
	for i in range(len(langs_out)):
	    lang = langs[i]
	    score = prediction_vct[0][i]
	    print(lang + ': ' + str(round(100*score, 2)) + '%')
	print('\n')