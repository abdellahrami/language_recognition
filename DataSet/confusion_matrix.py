from keras.models import Sequential
from keras.layers import Dense
import numpy as np 
from sklearn.model_selection import train_test_split
from keras.models import model_from_json 
from sklearn.metrics import confusion_matrix
import itertools
import matplotlib.pyplot as plt


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

while(1):
    # fix random seed for reproducibility
    seed = 7
    np.random.seed(seed)



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
    langs_keys = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
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
    # dataset = np.loadtxt("pima-indians-diabetes.csv", delimiter=",")
    dataset = np.array(Data)
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


    rounded_predictions = loaded_model.predict_classes(X_test,batch_size=10,verbose=0)

    # print( langs_keys.index(list(Y_train[0])) )
    # print(len(rounded_predictions))
    # print(len(test_labels))

    test_labels = []
    for i in Y_test:
    	test_labels.append(langs_keys.index(list(i)))



    test_labels = np.array(test_labels)

    cm = confusion_matrix(test_labels,rounded_predictions)

    cm_plot_labels = ['français','espagnole','portuguais','italien']

    plot_confusion_matrix(cm, cm_plot_labels,title='Confusion matrix')

    plt.show()


# # evaluate loaded model on test data
# loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# score = loaded_model.evaluate(X, Y, verbose=0)
# print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
