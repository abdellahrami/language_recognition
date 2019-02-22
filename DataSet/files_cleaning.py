import os
import re
print("Enter folder name :",end='')
folder = input()
filenames = os.listdir('./'+folder)
filenames.sort()
cpt = 0
for filename in filenames :
	if '.txt' not in filename:
		continue

	# if cpt > 50 :
	# 	break;
	# cpt+=1

	# print("filename = ",filename," continue ?[y/n]")
	# s = input()
	# if(s!='y'):
	# 	continue
	try :
		df = open('./'+folder+'/'+filename,'r',encoding='utf-8')
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
 
		lines = ''.join(lines)
		df.close()
		df_cleaned = open("./Cleaned/"+folder+"/Cleaned_"+filename,"w",encoding='utf-8');
		df_cleaned.write(lines)
		df_cleaned.close()
	except:
		continue
print("finished..................")



