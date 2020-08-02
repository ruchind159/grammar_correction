from flask import Flask           # import flask
from flask import jsonify
from main_file import load_model
from main_file import predict_for_sentence
from main_file import convert_to_dict


app = Flask(__name__)             # create an app instance

#loading model
model=load_model()				  #loading model from main_file

@app.route("/")                   # at the end point /
def hello():                      # call method hello
    return "Hello World!"         # which returns "hello world"

# @app.route("/<name>")
# def greet(name):
# 	return "hello "+name

@app.route("/<sentence>")              
def correct_sent(sentence):
	corrected_sent,cnt_corrections,info_for_change = predict_for_sentence(sentence, model)

	org_sent_word=[]                   #changed here
	org_sent_word=sentence.split()  #changed here

	word_info=[]

	for info in info_for_change:
	    word=[info[0],info[1]]
	    if "APPEND" in word[0]:
	        if word[1]-1 > -1 :
	            word[1]=org_sent_word[word[1]-1]
	            word[0]+="_after"
	        else:
	            word[1]="<BEG>"
	            word[0]+="_after"
	            continue
	    elif "REPLACE" in word[0]:
	        word[1]=org_sent_word[word[1]]
	        word[0]+=" with "
	    else:
	        word[1]=org_sent_word[word[1]]
	        word[0]+=" on "

	    word_info.append(word)

	info_dict=convert_to_dict(word_info,corrected_sent)
	return jsonify(info_dict)

if __name__ == "__main__":        # on running python app.py
    app.run(debug=True)
