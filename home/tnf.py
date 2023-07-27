# import torch
# from transformers import T5ForConditionalGeneration,T5Tokenizer

def set_seed(seed):
  # torch.manual_seed(seed)
  # if torch.cuda.is_available():
  #   torch.cuda.manual_seed_all(seed)
  pass

# set_seed(42)

# model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_boolean_questions')
# tokenizer = T5Tokenizer.from_pretrained('t5-base')

# # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# device = torch.device("cpu")
# # print ("device ",device)
# model = model.to(device)

def greedy_decoding (inp_ids,attn_mask):
  # greedy_output = model.generate(input_ids=inp_ids, attention_mask=attn_mask, max_length=256)
  # Question =  tokenizer.decode(greedy_output[0], skip_special_tokens=True,clean_up_tokenization_spaces=True)
  # return Question.strip().capitalize()
  pass

def beam_search_decoding (inp_ids,attn_mask):
  # beam_output = model.generate(input_ids=inp_ids,
  #                                attention_mask=attn_mask,
  #                                max_length=256,
  #                              num_beams=10,
  #                              num_return_sequences=3,
  #                              no_repeat_ngram_size=2,
  #                              early_stopping=True
  #                              )
  # Questions = [tokenizer.decode(out, skip_special_tokens=True, clean_up_tokenization_spaces=True) for out in
  #              beam_output]
  # return [Question.strip().capitalize() for Question in Questions]
  pass

def topkp_decoding (inp_ids,attn_mask):
  # topkp_output = model.generate(input_ids=inp_ids,
  #                                attention_mask=attn_mask,
  #                                max_length=256,
  #                              do_sample=True,
  #                              top_k=40,
  #                              top_p=0.80,
  #                              num_return_sequences=3,
  #                               no_repeat_ngram_size=2,
  #                               early_stopping=True
  #                              )
  # Questions = [tokenizer.decode(out, skip_special_tokens=True,clean_up_tokenization_spaces=True) for out in topkp_output]
  # return [Question.strip().capitalize() for Question in Questions]
  pass

def tnf(passage):
    
    # text1 = "truefalse: %s passage: %s </s>" % (passage, 'yes')
    # text2 = "truefalse: %s passage: %s </s>" % (passage, 'no')

    # # max_len = 256

    # # # True
    # encoding = tokenizer.encode_plus(text1, return_tensors="pt")
    # input_ids, attention_masks = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)

    # print ("Context: ",passage)
    # # print ("\nGenerated Question: ",truefalse)

    # # output = greedy_decoding(input_ids,attention_masks)
    # # print ("\nGreedy decoding:: ",output)

    # # final_questions = 'Beam decoding [Most accurate questions]'
    # final_questions = []
    # output = beam_search_decoding(input_ids,attention_masks)
    # # print ("\nBeam decoding [Most accurate questions] ::\n")
    # for out in output:
    #     # print(out)
    #     final_questions.append(out)

    # # final_questions += '\nTopKP decoding [Not very accurate but more variety in questions]'
    # output = topkp_decoding(input_ids,attention_masks)
    # # print ("\nTopKP decoding [Not very accurate but more variety in questions] ::\n")
    # for out in output:
    #     # print (out)
    #     final_questions.append(out)


    # # torch.cuda.empty_cache()

    # # # false
    # # encoding = tokenizer.encode_plus(text2, return_tensors="pt")
    # # input_ids, attention_masks = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)



    # # print ("Context: ",passage)
    # # # print ("\nGenerated Question: ",truefalse)

    # # # output = greedy_decoding(input_ids,attention_masks)
    # # # print ("\nGreedy decoding:: ",output)

    # # output = beam_search_decoding(input_ids,attention_masks)
    # # print ("\nBeam decoding [Most accurate questions] ::\n")
    # # for out in output:
    # #     print(out)


    # # output = topkp_decoding(input_ids,attention_masks)
    # # print ("\nTopKP decoding [Not very accurate but more variety in questions] ::\n")
    # # for out in output:
    # #     print (out)

    # return final_questions
    pass