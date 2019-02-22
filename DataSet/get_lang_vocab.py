import os
import re
from sklearn.feature_extraction.text import CountVectorizer
import sys
# c_vec = CountVectorizer(ngram_range=(3, 3),encoding='utf-8',analyzer='char',max_features=100)



cmd_args = sys.argv

if(len(cmd_args) == 1 ):
	print("enter command line args")
	exit()

# print("Ngrams char[0] or word [1]:",end='')
# ht = int(input())
# if(ht==0):
# 	ngrams_type = 'char'
# else:
# 	ngrams_type = 'word'

ngrams_type = cmd_args[1]

# print("Enter min ngrams :",end='')
# minNgrams = int(input())
# print("Enter max ngrams :",end='')
# maxNgrams = int(input())

minNgrams = int(cmd_args[2])
maxNgrams = int(cmd_args[3])

c_vec = CountVectorizer(ngram_range=(minNgrams, maxNgrams),encoding='utf-8',analyzer=ngrams_type,max_features=400)

# print("Enter folder name :",end='')
# folder = input()

folder = cmd_args[4]

filenames = os.listdir('./Cleaned/'+folder+'_top')
filenames.sort()
# cpt = 0
lines_output = []
files_cpt = 0
for filename in filenames :
	if(files_cpt%20==0):
		print(files_cpt)
	files_cpt+=1
	if '.txt' not in filename:
		continue
	# if cpt > 10 :
	# 	break
	# cpt+=1
	try :
		df = open("./Cleaned/"+folder+"_top/"+filename,'r',encoding='utf-8')
		lines = [line.replace('\n','') for line in df]
		# ngrams = c_vec.fit_transform(lines)
		ngrams = c_vec.fit_transform(lines)
		vocab = c_vec.vocabulary_
		count_values = ngrams.toarray().sum(axis=0)
		# N = sum(count_values)
		out_lines = []
		# cpt_lines = 100
		for ng_count, ng_text in sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True):
			out_lines.append([ng_count,ng_text])
			# if(cpt_lines <= 0):
			# 	break
			# cpt_lines-=1 
		df.close()
		cpt = 0
		for line in out_lines:
			lines_output.sort(reverse=True)
			# s = line.replace('\n','').split(':')
			i,ngram = line
			if(cpt<=500):
				if(ngram not in [n for _,n in lines_output]):
					lines_output.append([i,ngram])
					cpt+=1
				else:
					for a,b in lines_output:
						if b == ngram and a<i:
							lines_output.remove([a,b])
							lines_output.append([i,ngram])
				min_lines = min([a for a,_ in lines_output])

			elif ( i > min_lines):
				if(ngram not in [n for _,n in lines_output]):
					del lines_output[-1]
					lines_output.append([i,ngram])
				else:
					for a,b in lines:
						if b == ngram and a<i:
							lines_output.remove([a,b])
							lines_output.append([i,ngram])
				min_lines = min([a for a,_ in lines_output])
	except:
		continue
lines_output.sort(reverse=True)
df_output = open("./Ngrams/"+folder+"_"+str(minNgrams)+"_"+str(maxNgrams)+"_"+ngrams_type+".txt",'w',encoding='utf-8')
l = '\n'.join([ ':'.join([str(float(i)),k]) for i,k in lines_output[:500]])
df_output.write(l)
df_output.close()
# df_output2 = open("./Ngrams/features",'w',encoding='utf-8')
# l2 = '\n'.join([ k for _,k in lines[:500]])
# df_output2.write(l2)
# df_output2.close()

print("finished..................")


