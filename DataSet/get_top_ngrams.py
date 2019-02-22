import os
import re
from sklearn.feature_extraction.text import CountVectorizer
# c_vec = CountVectorizer(ngram_range=(3, 3),encoding='utf-8',analyzer='char',max_features=100)
c_vec_unlim = CountVectorizer(ngram_range=(3, 3),encoding='utf-8',analyzer='char',max_features=100)

print("Enter folder name :",end='')
folder = input()
filenames = os.listdir('./'+folder)
filenames.sort()
cpt = 0
for filename in filenames :
	if '.txt' not in filename:
		continue
	# if cpt > 10 :
	# 	break
	# cpt+=1
	try :
		df = open("./Cleaned/"+folder+"/Cleaned_"+filename,'r',encoding='utf-8')
		lines = [line.replace('\n','') for line in df]
		# ngrams = c_vec.fit_transform(lines)
		ngrams = c_vec_unlim.fit_transform(lines)
		vocab = c_vec_unlim.vocabulary_
		count_values = ngrams.toarray().sum(axis=0)
		# N = sum(count_values)
		out_lines = []
		# cpt_lines = 100
		for ng_count, ng_text in sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True):
			out_lines.append("{:.5f}".format(ng_count)+":"+ng_text)
			# if(cpt_lines <= 0):
			# 	break
			# cpt_lines-=1

		df.close()
		df_out = open("./Ngrams/"+folder+"/Ngrams_"+filename,"w",encoding='utf-8');
		out_lines = '\n'.join(out_lines)
		df_out.write(out_lines)
		df_out.close()
	except:
		continue
print("finished..................")


