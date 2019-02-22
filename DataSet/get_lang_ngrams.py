import os
import re
print("Enter folder name : ./Ngrams/",end='')
folder = input()
filenames = os.listdir('./Ngrams/'+folder)
filenames.sort()
cpt = 0
lines = []
ngrams_all = []
for filename in filenames :
	if '.txt' not in filename:
		continue
	# try:
	df = open("./Ngrams/"+folder+"/"+filename,'r',encoding='utf-8')
	# for line in df:
	# 	s = line.replace('\n','').split(':')
	# 	i,ngram = float(s[0]),s[1]
	# 	if ngram in [ngram for _,ngram in lines]:
	# 		for a,b in lines:
	# 			if b == ngram :
	# 				if a<i :
	# 					lines.remove([a,b])
	# 					lines.append([i,ngram])
	# 	else:
	# 		lines.append([i,ngram])
	for line in df:
		lines.sort(reverse=True)
		s = line.replace('\n','').split(':')
		i,ngram = float(s[0]),s[1]
		if(cpt<=500):
			if(ngram not in [n for _,n in lines]):
				lines.append([i,ngram])
				cpt+=1
			else:
				for a,b in lines:
					if b == ngram and a<i:
						lines.remove([a,b])
						lines.append([i,ngram])
		elif ( i > min([a for a,_ in lines])):
			if(ngram not in [n for _,n in lines]):
				del lines[-1]
				lines.append([i,ngram])
			else:
				for a,b in lines:
					if b == ngram and a<i:
						lines.remove([a,b])
						lines.append([i,ngram])


	df.close()
	# except:
		# continue
lines.sort(reverse=True)
df_output = open("./Ngrams/"+folder+"_Ngrams.txt",'w',encoding='utf-8')
l = '\n'.join([ ':'.join([str(float(i)),k]) for i,k in lines[:500]])

df_output.write(l)
df_output.close()
print("finished..................")

