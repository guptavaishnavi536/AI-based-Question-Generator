import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import random
import numpy as np
from nltk.tokenize import sent_tokenize
import spacy

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# device = torch.device("cpu")

summarize = pipeline("summarization", model='facebook/bart-large-cnn')

def summarizer(text, summarize=summarize):
  
  summary = ''

  comp_text = text.split()
  i = 0

  # print("Summarizing... ")
  while(i+256<len(comp_text)):
      # print(len(comp_text[i:i+256]))
      
      article = ' '.join(comp_text[i:i+256])
      i+=256
      # summary += summarize(article, max_length=500, min_length=100, do_sample=False)
      sum = summarize(article, do_sample=False)
      summary += sum[0]['summary_text']

  else:
      article = ' '.join(comp_text[i:])
      sum = summarize(article, do_sample=False)
      summary += sum[0]['summary_text']


  return summary

question_tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
question_model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")


question_model = question_model.to(device)



def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

set_seed(42)

def postprocesstext (content):
  final=""
  for sent in sent_tokenize(content):
    sent = sent.capitalize()
    final = final +" "+sent
  return final

# uncomment if using spacy for NER
nlp = spacy.load('en_core_web_sm')

def get_nouns_multipartite(summary, nlp=nlp):
  doc = nlp(summary)
  answers = []
  for ent in doc.ents:
    answers.append(ent.text)

  return answers

# uncomment for mrm8488/t5-base-finetuned-question-generation-ap model
def gen(context, answer, max_length=32, question_tokenizer= question_tokenizer, question_model=question_model):
  input_text = "answer: %s  context: %s </s>" % (answer, context)
  features = question_tokenizer([input_text], return_tensors='pt').to(device)

  output = question_model.generate(input_ids=features['input_ids'], 
               attention_mask=features['attention_mask'],
               max_length=max_length)
  torch.cuda.empty_cache()
  return question_tokenizer.decode(output[0])

from similarity.normalized_levenshtein import NormalizedLevenshtein
normalized_levenshtein = NormalizedLevenshtein()

def filter_same_sense_words(original,wordlist):
  filtered_words=[]
  base_sense =original.split('|')[1] 
  print (base_sense)
  for eachword in wordlist:
    if eachword[0].split('|')[1] == base_sense:
      filtered_words.append(eachword[0].split('|')[0].replace("_", " ").title().strip())
  return filtered_words

def get_highest_similarity_score(wordlist,wrd):
  score=[]
  for each in wordlist:
    score.append(normalized_levenshtein.similarity(each.lower(),wrd.lower()))
  return max(score)

def sense2vec_get_words(word,s2v,topn,question):
    output = []
    print ("word ",word)
    try:
      sense = s2v.get_best_sense(word, senses= ["NOUN", "PERSON","PRODUCT","LOC","ORG","EVENT","NORP","WORK OF ART","FAC","GPE","NUM","FACILITY"])
      most_similar = s2v.most_similar(sense, n=topn)
      # print (most_similar)
      output = filter_same_sense_words(sense,most_similar)
      print ("Similar ",output)
    except:
      output =[]

    threshold = 0.6
    final=[word]
    checklist =question.split()
    for x in output:
      if get_highest_similarity_score(final,x)<threshold and x not in final and x not in checklist:
        final.append(x)
    
    return final[1:]

import numpy as np
from sense2vec import Sense2Vec
s2v = Sense2Vec().from_disk(r"C:\Users\singh\Downloads\ibm_qb\Models\New\s2v_reddit_2015_md\s2v_old")

from sentence_transformers import SentenceTransformer
# paraphrase-distilroberta-base-v1
sentence_transformer_model = SentenceTransformer('msmarco-distilbert-base-v3')

from collections import OrderedDict
from sklearn.metrics.pairwise import cosine_similarity

def mmr(doc_embedding, word_embeddings, words, top_n, lambda_param):

    # Extract similarity within words, and between words and the document
    word_doc_similarity = cosine_similarity(word_embeddings, doc_embedding)
    word_similarity = cosine_similarity(word_embeddings)

    # Initialize candidates and already choose best keyword/keyphrase
    keywords_idx = [np.argmax(word_doc_similarity)]
    candidates_idx = [i for i in range(len(words)) if i != keywords_idx[0]]

    for _ in range(top_n - 1):
        # Extract similarities within candidates and
        # between candidates and selected keywords/phrases
        candidate_similarities = word_doc_similarity[candidates_idx, :]
        target_similarities = np.max(word_similarity[candidates_idx][:, keywords_idx], axis=1)

        # Calculate MMR
        mmr = (lambda_param) * candidate_similarities - (1-lambda_param) * target_similarities.reshape(-1, 1)
        mmr_idx = candidates_idx[np.argmax(mmr)]

        # Update keywords & candidates
        keywords_idx.append(mmr_idx)
        candidates_idx.remove(mmr_idx)

    return [words[idx] for idx in keywords_idx]

def get_distractors (word,origsentence,sense2vecmodel=s2v,sentencemodel=sentence_transformer_model,top_n=4,lambdaval=0.2):
  distractors = sense2vec_get_words(word,sense2vecmodel,top_n,origsentence)
  # print ("distractors ",distractors)
  if len(distractors) ==0:
    return distractors
  distractors_new = [word.capitalize()]
  distractors_new.extend(distractors)
  # print ("distractors_new .. ",distractors_new)

  embedding_sentence = origsentence+ " "+word.capitalize()
  # embedding_sentence = word
  keyword_embedding = sentencemodel.encode([embedding_sentence])
  distractor_embeddings = sentencemodel.encode(distractors_new)

  # filtered_keywords = mmr(keyword_embedding, distractor_embeddings,distractors,4,0.7)
  max_keywords = min(len(distractors_new),5)
  filtered_keywords = mmr(keyword_embedding, distractor_embeddings,distractors_new,max_keywords,lambdaval)
  # filtered_keywords = filtered_keywords[1:]
  final = [word.capitalize()]
  for wrd in filtered_keywords:
    if wrd.lower() !=word.lower():
      final.append(wrd.capitalize())
  final = final[1:]
  # print(final)
  return final