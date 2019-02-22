# Create first network with Keras
from keras.models import Sequential
from keras.layers import Dense
import numpy 
from sklearn.model_selection import train_test_split
from keras.models import model_from_json 
import matplotlib.pyplot as plt
import sys



cmd_args = sys.argv

if(len(cmd_args) == 1 ):
	print("enter command line args")
	exit()

ngrams_type = cmd_args[1]

minNgrams = int(cmd_args[2])
maxNgrams = int(cmd_args[3])

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# Training parameters
batch_size = 10000
num_epochs = 130
val_split = 0.25

# load dataset
max_ngrams = 100;


# print("Ngrams char[0] or word [1]:",end='')
# ht = int(input())
# if(ht==0):
# 	ngrams_type = 'char'
# else:
# 	ngrams_type = 'word'
# print("Enter min ngrams :",end='')
# minNgrams = int(input())
# print("Enter max ngrams :",end='')
# maxNgrams = int(input())

path_plus = '_'+str(minNgrams)+'_'+str(maxNgrams)+'_'+ngrams_type

langs_out = {'fr':[1,0,0,0],'es':[0,1,0,0],'pt':[0,0,1,0],'it':[0,0,0,1]}
Data = []
flag_leg_len = 0
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
# create model
model = Sequential()
model.add(Dense(4*max_ngrams, input_dim=4*max_ngrams, activation='sigmoid', kernel_initializer="uniform"))
model.add(Dense(400,  activation='sigmoid', kernel_initializer="uniform"))
model.add(Dense(4,  activation='softmax', kernel_initializer="uniform")) #init='uniform',
# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
history = model.fit(X_train, Y_train, epochs=num_epochs, batch_size=batch_size, verbose=2, validation_split=val_split)
#, validation_data=(X_test,Y_test)


print("Training completed succesfully...........")




# evaluate the model
# scores = model.evaluate(X_test, Y_test)
# print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

#///////////////////////////////////////////////////
#print plot results

# df = open("results"+path_plus+".txt","w")
# # df.write(path_plus)
# df.write(':'.join([str(i) for i in history.history['acc']])+'\n')
# df.write(':'.join([str(i) for i in history.history['val_acc']])+'\n')
# df.write(':'.join([str(i) for i in history.history['loss']])+'\n')
# df.write(':'.join([str(i) for i in history.history['val_loss']])+'\n')

# plt.plot(history.history['acc'])
# plt.plot(history.history['val_acc'])
# plt.title('model accuracy')
# plt.ylabel('accuracy')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.show()
# # summarize history for loss
# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.show()



#/////////////////////////////////////////////////

# model_json = model.to_json()
# with open("model_project.json", "w") as json_file:
#     json_file.write(model_json)
# # saving  weights into HDF5
# model_rnn.save_weights("model.h5")
# print("Saved model to disk")

#//////////////////////////////////////////////

# serialize model to JSON
model_json = model.to_json()
with open("model"+path_plus+".json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model"+path_plus+".h5")
print("Saved model to disk")
 
# later...
 
# # load json and create model
# json_file = open('model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# # load weights into new model
# loaded_model.load_weights("model.h5")
# print("Loaded model from disk")
 
# # evaluate loaded model on test data
# loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# score = loaded_model.evaluate(X, Y, verbose=0)
# print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
