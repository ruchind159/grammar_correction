from flask import Flask           # import flask
from main_file import predict_for_sentence
from main_file import load_model


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
def check_grammar(sentence):
	corrected_sent,cnt_corrections = predict_for_sentence(sentence, model)
	return(f"corrected sentence = {corrected_sent} ########\n Produced overall corrections: {cnt_corrections}")         

if __name__ == "__main__":        # on running python app.py
    app.run(debug=True)
