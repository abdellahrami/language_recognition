import os
import re
from sklearn.feature_extraction.text import CountVectorizer
# c_vec = CountVectorizer(ngram_range=(3, 3),encoding='utf-8',analyzer='char',max_features=100)

# print("Ngrams char->0 or word->1 :",end='')
# ht = int(input())
# if(ht==0):
# 	ngrams_type = 'char'
# else:
# 	ngrams_type = 'word'
# print("Enter min ngrams :",end='')
# minNgrams = int(input())
# print("Enter max ngrams :",end='')
# maxNgrams = int(input())

import sys

cmd_args = sys.argv

if(len(cmd_args) == 1 ):
	print("enter command line args ngrams_type minNgrams maxNgrams folder")
	exit()

ngrams_type = cmd_args[1]

minNgrams = int(cmd_args[2])
maxNgrams = int(cmd_args[3])

folder = cmd_args[4]

# minNgrams,maxNgrams,ngrams_type = 2,3,'char'

# print("for : ",minNgrams,maxNgrams,ngrams_type)


c_vec = CountVectorizer(ngram_range=(minNgrams, maxNgrams),encoding='utf-8',analyzer='char',max_features=1000)

def get_score(mylist, ngram,N):
    for sub_list in mylist:
        if ngram in sub_list:
        	value = sub_list[0]/N
        	if(value>0.0001):
        		return value
        	else:
        		return 0

# print("Enter folder name :",end='')
# folder = input()


filenames = os.listdir('./Cleaned/'+folder)

newpath = "./Ngrams/"+folder+"_"+str(minNgrams)+"_"+str(maxNgrams)+"_"+ngrams_type 
if not os.path.exists(newpath):
    os.makedirs(newpath)

filenames_done = os.listdir(newpath)
for i in filenames_done:
	try:
		filenames.remove(i)
	except:
		continue
filenames.sort()
cpt = 0
if("dict_"+str(minNgrams)+"_"+str(maxNgrams)+"_"+ngrams_type+".txt" not in os.listdir("./Ngrams")):
	fd_ngrams1 = open("./Ngrams/"+"fr"+"_"+str(minNgrams)+"_"+str(maxNgrams)+"_"+ngrams_type+".txt",'r',encoding='utf-8')
	fd_ngrams2 = open("./Ngrams/"+"es"+"_"+str(minNgrams)+"_"+str(maxNgrams)+"_"+ngrams_type+".txt",'r',encoding='utf-8')
	fd_ngrams3 = open("./Ngrams/"+"pt"+"_"+str(minNgrams)+"_"+str(maxNgrams)+"_"+ngrams_type+".txt",'r',encoding='utf-8')
	fd_ngrams4 = open("./Ngrams/"+"it"+"_"+str(minNgrams)+"_"+str(maxNgrams)+"_"+ngrams_type+".txt",'r',encoding='utf-8')
	lang_ngrams = [line.replace('\n','').split(':')[1] for line in fd_ngrams1][:300]
	lang_ngrams += [line.replace('\n','').split(':')[1] for line in fd_ngrams2][:300]
	lang_ngrams += [line.replace('\n','').split(':')[1] for line in fd_ngrams3][:300]
	lang_ngrams += [line.replace('\n','').split(':')[1] for line in fd_ngrams4][:300]
	lang_ngrams = list(set(lang_ngrams))
	lang_ngrams = lang_ngrams[:400]
	df = open("./Ngrams/dict_"+str(minNgrams)+"_"+str(maxNgrams)+"_"+ngrams_type+".txt",'w',encoding='utf-8')
	df.write('\n'.join(lang_ngrams))
	df.close()
else:
	fd_ngram = open("./Ngrams/dict_"+str(minNgrams)+"_"+str(maxNgrams)+"_"+ngrams_type+".txt",'r',encoding='utf-8')
	lang_ngrams = [line.replace('\n','') for line in fd_ngram]
# exit()
for filename in filenames:
	if '.txt' not in filename:
		continue
	# if(cpt>5):
	# 	break;
	# cpt+=1
	try:
		df = open("./Cleaned/"+folder+"/"+filename,'r',encoding='utf-8')
		lines = [line.replace('\n','') for line in df]
		ngrams = c_vec.fit_transform(lines)
		vocab = c_vec.vocabulary_
		count_values = ngrams.toarray().sum(axis=0)
		N = sum(count_values)
		ngrams_file = sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True)
		out_lines = []
		for ngram in lang_ngrams:
			if any(ngram in sl for sl in ngrams_file):
				out_lines.append(ngram+":"+str(get_score(ngrams_file,ngram,N)))
			else:
				out_lines.append(ngram+":0")
		df.close()

		df_out = open("./Ngrams/"+folder+"_"+str(minNgrams)+"_"+str(maxNgrams)+"_"+ngrams_type+"/"+filename,"w",encoding='utf-8');
		out_lines = '\n'.join(out_lines)
		df_out.write(out_lines)
		df_out.close()
	except:
		continue
print("finished..................",folder)

