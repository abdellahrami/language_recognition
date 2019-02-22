from tkinter import *
from tkinter.ttk import Progressbar, Labelframe, Combobox, Style
from tkinter.filedialog import askopenfilename
from time import sleep
from sklearn.feature_extraction.text import CountVectorizer
import numpy
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from keras.models import model_from_json 

window = Tk()
window.tk.call('encoding','system','utf-8')
window.title("Language recognition")
window.configure(background='#99ccff')
s = Style(window)

#window.resizable(0, 0)
w = 750 
h = 450 
ws = window.winfo_screenwidth() 
hs = window.winfo_screenheight() 
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
window.geometry('%dx%d+%d+%d' % (w, h, x, y))

X_vector = None

dict_model = {"2-grams":0,"2-3-grams":1, "3-grams":2,"3-4-grams":3,"4-grams":4,"1-word":5,"1-2-3-words":6}
dict_path = {0:['char',2,2],1:['char',2,3],2:['char',3,3],3:['char',3,4],4:['char',4,4],5:['word',1,1],6:['word',1,3]}
langs_out = {'fr':[1,0,0,0],'es':[0,1,0,0],'it':[0,0,0,1],'pt':[0,0,1,0]}


models = ["_2_2_char","_2_3_char","_3_3_char","_3_4_char","_4_4_char","_1_1_word","_1_3_word"]
loaded_models = []
for model in models:
	json_file = open('model'+model+'.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	# load weights into new model
	loaded_model.load_weights("model"+model+".h5")
	loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	loaded_models.append(loaded_model)



# C = Canvas(window, bg="blue", height=450, width=700)
# filename = PhotoImage(file = "/home/fatimaezzahrae/Pictures/99.png")
# background_label = Label(window, image=filename)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)
# C.pack()

# background_image= PhotoImage(file="./background.gif")
# # background_label = Label(window, image=background_image)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)

headerFrame = Frame(window)
headerFrame.configure(background='#99ccff')##
headerFrame['bg'] = headerFrame.master['bg']
headerFrame.pack(side = "top")

centerFrame = Frame(window)
centerFrame.configure(background='#99ccff')##
centerFrame['bg'] = centerFrame.master['bg']
centerFrame.pack()

resultFrame = LabelFrame(window, text="Prediction result", font =("Arial", 16, "bold"))
resultFrame.configure(background='#99ccff')##
resultFrame.pack( fill = "x",  side="bottom", padx = 10, pady = 5)


req1 = Label(centerFrame, text = "Insert the text here :", font =("Arial", 16, "bold"))
req1.configure(background='#99ccff')##
req1.grid(row = 0, column = 0, sticky = W)
req2 = Label(centerFrame, text = "Or :", font =("Arial", 16, "bold"))
req2.configure(background='#99ccff')##
req2.grid(row = 1, column = 1)

textFrame = Frame(centerFrame)
text = Text(textFrame, height = 8, width = 50, borderwidth = 0, padx = 10, pady = 10, wrap = WORD, font = ("Courier", 12))
scroll = Scrollbar(textFrame, orient = VERTICAL, command = text.yview)
text['yscroll'] = scroll.set

scroll.pack(side = "right", fill = "y")
text.pack(side = "left", fill = "both", expand = True)

#textFrame.place(x = 10, y = 75)
#textFrame.pack( anchor = "center")
textFrame.grid(row = 1, column = 0)

def retrieveInput():
    input1 = text.get("1.0",'end-1c')
    # print(input)
    # print("0000000000000")
    return input1
path_choisi = ''
def OpenFile():
	global path_choisi
	name = askopenfilename(initialdir = "./",filetypes = (("Text File", "*.txt"),("All Files","*.*")),title = "Choose a file")
	path_choisi = name
    # print (name)
	try:
	    with open(name,'r',encoding='utf-8') as f:
	        textFile = f.read()
	        text.delete('1.0', END)
	        text.insert(END, textFile)
	        text.pack()

	except:
	    print("No file exists")
listValDef = [10, 10, 10, 10]

def displayBars(listVal=listValDef):
	progressFr = Progressbar(resultFrame, orient = HORIZONTAL, length = 100, mode = 'determinate', variable = listVal[0], style = "LabeledProgressbarFr")
	progressFr.grid(column = 6, row = 2, padx = 8)
	progressEs = Progressbar(resultFrame, orient = HORIZONTAL, length = 100, mode = 'determinate', variable = listVal[1], style = "LabeledProgressbarEs")
	progressEs.grid(column = 6, row = 3)
	progressIt = Progressbar(resultFrame, orient = HORIZONTAL, length = 100, mode = 'determinate', variable = listVal[3], style = "LabeledProgressbarIt")
	progressIt.grid(column = 6, row = 4)
	progressPt = Progressbar(resultFrame, orient = HORIZONTAL, length = 100, mode = 'determinate', variable = listVal[2], style = "LabeledProgressbarPt")
	progressPt.grid(column = 6, row = 5)


	for i in range(int(progressFr["value"]),0,-1):
		progressFr.step(-1)
	for i in range(int(progressEs["value"]),0,-1):
		progressEs.step(-1)
	for i in range(int(progressIt["value"]),0,-1):
		progressIt.step(-1)
	for i in range(int(progressPt["value"]),0,-1):
		progressPt.step(-1)

	for i in range(-1, int(listVal[0]/5)-1  if int(listVal[0]/5)-1>0 else int(listVal[0]/5)):
	    sleep(0.07)
	    progressFr.step(5)
	    s.configure("LabeledProgressbarFr", text="{0} %      ".format(listVal[0]))
	    window.update_idletasks()
	for i in range(-1, int(listVal[1]/5)-1 if int(listVal[1]/5)-1>0 else int(listVal[1]/5)):
	    sleep(0.07)
	    progressEs.step(5)
	    s.configure("LabeledProgressbarEs", text="{0} %      ".format(listVal[1]))
	    window.update_idletasks()
	for i in range(-1, int(listVal[3]/5)-1 if int(listVal[3]/5)-1>0 else int(listVal[3]/5)):
	    sleep(0.07)
	    progressIt.step(5)
	    s.configure("LabeledProgressbarIt", text="{0} %      ".format(listVal[3]))
	    window.update_idletasks()
	for i in range(-1, int(listVal[2]/5)-1 if int(listVal[2]/5)-1>0 else int(listVal[2]/5)):
	    sleep(0.07)
	    progressPt.step(5)
	    s.configure("LabeledProgressbarPt", text="{0} %      ".format(listVal[2]))
	    window.update_idletasks()

	# print(progressFr["value"])
	# print(progressEs["value"])
	# print(progressPt["value"])
	# print(progressIt["value"])
	# window.update_idletasks()


def model_predict(X,index):
	# loaded_models[index].compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	prediction_vct = loaded_models[index].predict(X,steps=None)
	langs = list(langs_out.keys())
	list_out = []
	for i in range(len(langs_out)):
	    # lang = langs[i]
	    score = prediction_vct[0][i]
	    # print(lang + ': ' + str(round(100*score, 2)) + '%')
	    # print(score)
	    list_out.append(round(100*score, 2))
	return list_out



def get_score(mylist, ngram,N):
    for sub_list in mylist:
        if ngram in sub_list:
        	value = sub_list[0]/N
        	if(value>0.0001):
        		return value
        	else:
        		return 0

lines_cleaned = ''
def processInput(index=0,newText=False):
	global X_vector,lines_cleaned
	ngrams_type,minNgrams,maxNgrams=dict_path[index]
	if(newText):
		input1 = retrieveInput()

		# df = open("predict_text.txt",'r',encoding='utf-8')
		lines = input1.split('\n')
		# df = open(path_choisi,'r',encoding='utf-8')
		# lines = [line for line in df]
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
		lines_cleaned = lines
	#df.close()
	
	c_vec = CountVectorizer(ngram_range=(minNgrams, maxNgrams),encoding='utf-8',analyzer=ngrams_type)
	path_plus = '_'+str(minNgrams)+'_'+str(maxNgrams)+'_'+ngrams_type
	lang_ngrams = []

	fd_ngram = open("Ngrams/dict"+path_plus+".txt",'r',encoding='utf-8')
	lang_ngrams = [line.replace('\n','') for line in fd_ngram]

	# script : calculate ngrams scores
	ngrams = c_vec.fit_transform(lines_cleaned)

	vocab = c_vec.vocabulary_

	count_values = ngrams.toarray().sum(axis=0)

	N = sum(count_values)

	ngrams_file = sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True)
	X_pred = []
	vec = []
	for ngram in lang_ngrams:
		if any(ngram in sl for sl in ngrams_file):
			vec.append(get_score(ngrams_file,ngram,N))
		else:
			vec.append(0)
	if(len(vec)<400):
		vec += ['0']*(400-len(vec))
	X_pred.append(vec)
	X = numpy.array(X_pred)
	X_vector = X



	model_val = model_predict(X,index)

	displayBars(model_val)




listLetter = [" ","2-grams", "3-grams","4-grams","2-3-grams","3-4-grams"]

listWord = [" ","1-word","1-2-3-words"]



combobox = Combobox(resultFrame, values = listWord, width = 10)
def chooseCombo():
	state = var.get()
	combobox.config(textvariable = choice)
	choice1 = choice.get()

	if state == 1:
		combobox.config(values = listWord)
		combobox.grid(row = 4 , column = 0, columnspan = 2, ipadx = 30, ipady = 5)
		combobox.current(0)
	elif state == 2:
		combobox.config(values = listLetter)
		combobox.grid(row = 4 , column = 0, columnspan = 2, ipadx = 30, ipady = 5)
		combobox.current(0)
	return state, choice1

choice = StringVar()
def chooseModel():
	# typeM, choice1 = chooseCombo()
	state = var.get()
	combobox.config(textvariable = choice)
	model_choice = choice.get()
	#combobox.config(textvariable = choice)
	#combobox.bind('<<ComboboxSelected>>', lambda _ : print(typeM, choice.get()))
	# print(state, choice1)
	# print("###################\n",dict_model[model_choice])
	# model_val = model_predict(X_vector,index=dict_model[model_choice])
	processInput(index=dict_model[model_choice])

	# displayBars(model_val)




uploadButton = Button(centerFrame, text = "Upload a file",relief=GROOVE, fg = "blue", command = OpenFile) #foreground bg:background
uploadButton.grid(row = 1, column = 4)
detecteButton = Button(centerFrame, text = "Detecte language",relief=GROOVE, fg = "blue",command=lambda:processInput(newText=True)) #
detecteButton.grid(row = 3, column = 0)
showButton = Button(resultFrame, text = "Show Result",relief=GROOVE, fg = "blue", command = chooseModel)
showButton.grid(row = 4, column = 3)

note3 = Label(centerFrame, text = "             ")
note3.configure(background='#99ccff')##
note3.grid(row = 2, column = 0)



note = Label(resultFrame, text = "You are welcome to try predicting the language using \n a method custumized by the following parameters:", font = ("Gourmand", 10))
note.grid(row = 0, columnspan = 3)
note.configure(background='#99ccff')##


	

var = IntVar()
radioWord = Radiobutton(resultFrame, text = "Words", variable = var, value = 1, font = ("Courier", 10, "bold"), command = lambda : chooseCombo())
radioWord.grid(row = 2, column = 0, ipadx = 5, ipady = 5)
radioWord.configure(background='#99ccff')##

radioLetter = Radiobutton(resultFrame, text = "Letters", variable = var, value = 2, font = ("Courier", 10, "bold"), command = lambda : chooseCombo())
radioLetter.grid(row = 2, column = 1, ipadx = 5, ipady = 5)
radioLetter.configure(background='#99ccff')##


# combobox = Combobox(resultFrame, values = listLetter, width = 10)
# combobox.grid(row = 4 , column = 0, columnspan = 2, ipadx = 30, ipady = 5)
#combobox.current(0)

# note = Label(resultFrame, text = "  \n ")
# note.grid(row = 6, columnspan = 6)

note1 = Label(resultFrame, text = "             ")
note1.configure(background='#99ccff')##
note1.grid(column = 3, rowspan = 6)

note2 = Label(resultFrame, text = "             ")
note2.configure(background='#99ccff')##
note2.grid(column = 4, rowspan = 6)

# note3 = Label(resultFrame, text = "             ")
# note3.grid(column = 5, rowspan = 6)

s.layout("LabeledProgressbarFr",
         [('LabeledProgressbar.trough',
           {'children': [('LabeledProgressbar.pbar',
                          {'side': 'left', 'sticky': 'ns'}),
                         ("LabeledProgressbar.label",
                          {"sticky": ""})],
           'sticky': 'nswe'})])
s.configure("LabeledProgressbarFr", background='#00ff80')
s.layout("LabeledProgressbarIt",
         [('LabeledProgressbar.trough',
           {'children': [('LabeledProgressbar.pbar',
                          {'side': 'left', 'sticky': 'ns'}),
                         ("LabeledProgressbar.label",
                          {"sticky": ""})],
           'sticky': 'nswe'})])
s.configure("LabeledProgressbarIt", background='#00ff80')
s.layout("LabeledProgressbarEs",
         [('LabeledProgressbar.trough',
           {'children': [('LabeledProgressbar.pbar',
                          {'side': 'left', 'sticky': 'ns'}),
                         ("LabeledProgressbar.label",
                          {"sticky": ""})],
           'sticky': 'nswe'})])
s.configure("LabeledProgressbarEs", background='#00ff80')
s.layout("LabeledProgressbarPt",
         [('LabeledProgressbar.trough',
           {'children': [('LabeledProgressbar.pbar',
                          {'side': 'left', 'sticky': 'ns'}),
                         ("LabeledProgressbar.label",
                          {"sticky": ""})],
           'sticky': 'nswe'})])
s.configure("LabeledProgressbarPt", background='#00ff80')

fr = Label(resultFrame, text = "French", font = ("Helventica", 10, "bold"))
fr.configure(background='#99ccff')##
fr.grid(column = 5, row = 2, sticky = E)
es = Label(resultFrame, text = "Spanish", font = ("Helventica", 10, "bold"))
es.configure(background='#99ccff')##
es.grid(column = 5, row = 3, sticky = E)
it = Label(resultFrame, text = "Italien", font = ("Helventica", 10, "bold"))
it.configure(background='#99ccff')##
it.grid(column = 5, row = 4, sticky = E)
pt = Label(resultFrame, text = "Portuguese", font = ("Helventica", 10, "bold"))
pt.configure(background='#99ccff')##
pt.grid(column = 5, row = 5, sticky = E)



def frange(start, stop, step):
	x = start
	while x < stop:
		yield x
		x += step

window.mainloop() 