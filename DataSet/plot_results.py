import matplotlib.pyplot as plt

df = []
df.append(open("results_2_2_char.txt",'r'))
df.append(open("results_2_3_char.txt",'r'))
df.append(open("results_3_3_char.txt",'r'))
df.append(open("results_3_4_char.txt",'r'))
df.append(open("results_4_4_char.txt",'r'))
df.append(open("results_1_1_word.txt",'r'))
df.append(open("results_1_3_word.txt",'r'))

all_lines = []
for i in range(7):
	all_lines.append([list(map(float,line.replace('\n','').split(':'))) for line in df[i] ])

# print(len(all_lines[0][1]))

for i in range(7):
	plt.plot(all_lines[i][0])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(["2_2_char","2_3_char","3_3_char","3_4_char","4_4_char","1_1_word","1_3_word",], loc='upper left')
plt.show()

for i in range(7):
	plt.plot(all_lines[i][1])
plt.title('validation accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(["2_2_char","2_3_char","3_3_char","3_4_char","4_4_char","1_1_word","1_3_word",], loc='upper left')
plt.show()

for i in range(7):
	plt.plot(all_lines[i][2])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(["2_2_char","2_3_char","3_3_char","3_4_char","4_4_char","1_1_word","1_3_word",], loc='upper left')
plt.show()

for i in range(7):
	plt.plot(all_lines[i][2])
plt.title('validation loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(["2_2_char","2_3_char","3_3_char","3_4_char","4_4_char","1_1_word","1_3_word",], loc='upper left')
plt.show()

