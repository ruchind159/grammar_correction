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
min_error_probability=0.66
min_probability=0.0
lowercase_tokens=0
model_name='xlnet'
special_tokens_fix=0
confidence=0.35
is_ensemble=0
weigths=None


#sentence predictor
def predict_for_sentence(inp_sent, model):
    predictions = []
    cnt_corrections = 0
    batch = []
    batch.append(inp_sent.split())
    if batch:
        preds, cnt, info_for_change = model.handle_batch(batch)
        predictions.extend(preds)
        cnt_corrections += cnt

    after_correction=("\n".join([" ".join(x) for x in predictions]) + '\n')
    return after_correction, cnt_corrections, info_for_change


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

#function used for converting inoformation into respective dict
def convert_to_dict(info_list,corrected):
    dictionary={
        'corrected':corrected,
        'errors':{
                    i:info_list[i] for i in range(len(info_list))
                 }
                }
    return dictionary


#function to be used in this file
def check_grammar(my_sentence):
    corrected_sent,cnt_corrections,info_for_change = predict_for_sentence(my_sentence, model)

    org_sent_word=[]                   #changed here
    org_sent_word=my_sentence.split()  #changed here

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
    return info_dict


#implementing the code here

# model=load_model() #loading model 

# while True:
#     my_sentence=input("Enter sentence for grammar check: ")
#     print(check_grammar(my_sentence)) 
#     again=input("Wanna do it again? (y/n) : ")
#     if(again=='n'):
#         break



#for downloading xlnet follow https://grammarly-nlp-data-public.s3.amazonaws.com/gector/xlnet_0_gector.th
