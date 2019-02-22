import os
import re

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

for folder in ['fr'+path_plus,'es'+path_plus,'pt'+path_plus,'it'+path_plus]:
	filenames = os.listdir('./Ngrams/'+folder)
	filenames.sort()
	cpt = 0
	lines_out = []
	for filename in filenames :
		if '.txt' not in filename:
			continue
		try:
			df = open('./Ngrams/'+folder+'/'+filename,'r',encoding='utf-8')
			lines = [ line.replace('\n','').split(':')[1] for line in df]
			lines_out.append(':'.join(lines))
			df.close()
		except:
			continue
	lines_out_joined = '\n'.join(lines_out)
	df_output = open('./'+folder+'_data'+'.txt','w',encoding='utf-8')
	df_output.write(lines_out_joined)
	df_output.close()
	print("Finished.....",folder)



