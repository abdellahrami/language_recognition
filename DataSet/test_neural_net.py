from keras.models import Sequential
from keras.layers import Dense
import numpy 
from sklearn.model_selection import train_test_split
from keras.models import model_from_json 

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)



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

langs_out = {'fr':[1,0,0,0],'es':[0,1,0,0],'pt':[0,0,1,0],'it':[0,0,0,1]}
Data = []
for folder in ['fr','es','pt','it']:
	fd = open(folder+path_plus+'_data.txt','r',encoding='utf-8')
	for line in fd:
		line = line.replace('\n','')
		vec = []
		valeurs = line.split(":")
		if(len(valeurs)<400):
			valeurs+= ['0']*(400-len(valeurs))
		for i in valeurs:
			vec.append(float(i))
		for j in langs_out[folder]:
			vec.append(j)
		Data.append(vec)
# print(len(Data),len(Data[0]))
#print(Data[0])
# dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
dataset = numpy.array(Data)
# print(dataset[0])


# split into input (X) and output 󰀀 variables
X = dataset[:,0:400]
Y = dataset[:,400:]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25,random_state = seed)

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
score = loaded_model.evaluate(X_test, Y_test, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
