from flask import Flask, redirect, render_template, jsonify, request          # import flask
from main_file import load_model, predict_for_sentence, convert_to_dict, add_tokens


app = Flask(__name__)             # create an app instance

#loading model
model=load_model()				  #loading model from main_file

@app.route("/")                   # at the end point /
def hello():                      # call method hello
    return "Hello World!"         # which returns "hello world"


@app.route("/text",methods=["POST","GET"])
def get_text():
	if request.method=="POST":
		sent=request.form['sent']
		return redirect(f'/check?sentence={sent}')
	else:
		return render_template("grammar_text.html")


@app.route("/check")              #this is same as the grammar check function in main file
def correct_sent():
	sentence=request.args.get('sentence')
	corrected_sent,cnt_corrections,info_for_change = predict_for_sentence(sentence, model)

	word_info=add_tokens(sentence,info_for_change)

	info_dict=convert_to_dict(word_info,corrected_sent)
	return jsonify(info_dict)

if __name__ == "__main__":        # on running python app.py
    app.run(debug=True)
