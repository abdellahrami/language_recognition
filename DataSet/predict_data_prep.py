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

# c_vec = CountVectorizer(ngram_range=(3, 3),encoding='utf-8',analyzer='char',max_features=100)
c_vec = []
c_vec.append(CountVectorizer(ngram_range=(3, 3),encoding='utf-8',analyzer='char'))
c_vec.append(CountVectorizer(ngram_range=(4, 4),encoding='utf-8',analyzer='char'))
c_vec.append(CountVectorizer(ngram_range=(3, 4),encoding='utf-8',analyzer='char'))
c_vec.append(CountVectorizer(ngram_range=(1, 1),encoding='utf-8',analyzer='word'))



def get_score(mylist, ngram,N):
    for sub_list in mylist:
        if ngram in sub_list:
        	value = sub_list[0]/N
        	if(value>0.0001):
        		return value
        	else:
        		return 0



lang_ngrams = []

fd_ngram = open("./Ngrams/dict_3_3_char.txt",'r',encoding='utf-8')
lang_ngrams.append([line.replace('\n','') for line in fd_ngram])

fd_ngram = open("./Ngrams/dict_4_4_char.txt",'r',encoding='utf-8')
lang_ngrams.append([line.replace('\n','') for line in fd_ngram])

fd_ngram = open("./Ngrams/dict_3_4_char.txt",'r',encoding='utf-8')
lang_ngrams.append([line.replace('\n','') for line in fd_ngram])

fd_ngram = open("./Ngrams/dict_1_1_word.txt",'r',encoding='utf-8')
lang_ngrams.append([line.replace('\n','') for line in fd_ngram])

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
ngrams = []
for i in range(4):
	ngrams.append(c_vec[i].fit_transform(lines))
# ngrams.append(c_vec[1].fit_transform(lines))
# ngrams.append(c_vec[2].fit_transform(lines))
# ngrams.append(c_vec[3].fit_transform(lines))
vocab = []
for i in range(4):
	vocab.append(c_vec[i].vocabulary_)
# vocab.append(c_vec[1].vocabulary_)
# vocab.append(c_vec[2].vocabulary_)
# vocab.append(c_vec[3].vocabulary_)
count_values = []
for i in range(4):
	count_values.append(ngrams[i].toarray().sum(axis=0))
# count_values.append(ngrams[1].toarray().sum(axis=0))
# count_values.append(ngrams[2].toarray().sum(axis=0))
# count_values.append(ngrams[3].toarray().sum(axis=0))
N = []
for i in range(4):
	N.append(sum(count_values[i]))
# N.append(sum(count_values[1]))
# N.append(sum(count_values[2]))
# N.append(sum(count_values[3]))
ngrams_file = []
for i in range(4):
	ngrams_file.append(sorted([(count_values[i][i],k) for k,i in vocab[i].items()], reverse=True))
# ngrams_file.append(sorted([(count_values[1][i],k) for k,i in vocab[1].items()], reverse=True))
# ngrams_file.append(sorted([(count_values[2][i],k) for k,i in vocab[2].items()], reverse=True))
# ngrams_file.append(sorted([(count_values[3][i],k) for k,i in vocab[3].items()], reverse=True))
X_pred = [[],[],[],[]]
for i in range(4):
	for ngram in lang_ngrams[i]:
		if any(ngram in sl for sl in ngrams_file[i]):
			X_pred[i].append(get_score(ngrams_file[i],ngram,N))
		else:
			X_pred[i].append(i)

X = [[],[],[],[]]
for i in range(4):
	X[i] = numpy.array(X_pred[i])


# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")
 
# evaluate loaded model on test data
loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])



