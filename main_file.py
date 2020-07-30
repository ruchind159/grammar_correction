from gector.gec_model import GecBERTModel
from spellchecker import SpellChecker
import os


#all arguments for model
current_dir=os.getcwd()
vocab_path=os.path.join(current_dir,"data/output_vocabulary/")
model_path=os.path.join(current_dir,"model/xlnet_0_gector.th")#,"/content/gector/roberta_1_gector.th"]
max_len=50
min_len=3
batch_size=128
iterations=5
min_error_probability=0.50
min_probability=0.0
lowercase_tokens=0
model_name='xlnet'
special_tokens_fix=0
confidence=0.20
is_ensemble=0
weigths=None


#sentence predictor
def predict_for_sentence(inp_sent, model):
    predictions = []
    cnt_corrections = 0
    batch = []
    batch.append(inp_sent.split())
    if batch:
        preds, cnt = model.handle_batch(batch)
        predictions.extend(preds)
        cnt_corrections += cnt

    after_correction=("\n".join([" ".join(x) for x in predictions]) + '\n')
    return after_correction, cnt_corrections


#for loading model
def load_model():
	model = GecBERTModel(vocab_path=vocab_path,
    	                  model_paths=[model_path],
        	             min_error_probability=0.66,
            	         model_name='xlnet'
                	      )
	return model


#function for spell checking
def check_spell(sent):
  spell = SpellChecker()

  misspelled = sent.split()
  corrected=[]

  for word in misspelled:
    corrected.append(spell.correction(word))
  sent=" "
  return sent.join(corrected)


#function to be used in this file
def check_grammar():
    my_sentence=input("Enter sentence for grammar check: ")
    corrected_sent,cnt_corrections = predict_for_sentence(my_sentence, model)
    return(f"corrected sentence = {corrected_sent} ########\n Produced overall corrections: {cnt_corrections}") 


#implementing the code here

# model=load_model() #loading model 
# print(check_grammar()) 



#for downloading xlnet follow https://grammarly-nlp-data-public.s3.amazonaws.com/gector/xlnet_0_gector.th
