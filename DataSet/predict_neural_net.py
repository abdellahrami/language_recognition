from keras.models import Sequential
from keras.layers import Dense
import numpy 
from sklearn.model_selection import train_test_split
from keras.models import model_from_json 

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# Training parameters
batch_size = 1000
num_epochs = 35
val_split = 0.25

# load dataset
max_ngrams = 100;

langs_out = {'fr':[1,0,0,0],'es':[0,1,0,0],'pt':[0,0,1,0],'it':[0,0,0,1]}
X_pred = []

fd = open('To_predict.txt','r',encoding='utf-8')
for line in fd:
	line = line.replace('\n','')
	vec = []
	for i in line.split(":"):
		vec.append(i)
	X_pred.append(vec)
# print(len(Data),len(Data[0]))
#print(Data[0])
# dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
X = numpy.array(X_pred)
# print(dataset[0])



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
# loaded_model.predict_classes(X,verbose=1)
# print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
# print(s)
# Xnew = X
# ynew = loaded_model.predict_classes(Xnew)
# # show the inputs and predicted outputs
# for i in range(len(Xnew)):
# 	print("Predicted=%s" % (ynew[i]))

prediction_vct = loaded_model.predict(X)
langs = list(langs_out.keys())
for i in range(len(langs_out)):
    lang = langs[i]
    score = prediction_vct[0][i]
    print(lang + ': ' + str(round(100*score, 2)) + '%')
print('\n')