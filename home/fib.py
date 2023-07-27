import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from . import mcq

# nltk.download('punkt')
# nltk.download('stopwords')
from nltk.tokenize import sent_tokenize

def break_into_sentences(paragraph):
    sentences = sent_tokenize(paragraph)
    return sentences

def replace_keyword_with_blank(sentence):

    keywords = mcq.get_nouns_multipartite(sentence)
    if len(keywords) == 0:

        # Tokenize the sentence into words
        words = word_tokenize(sentence)

        # Remove stopwords
        stopwords_list = set(stopwords.words('english'))
        words = [word for word in words if word.casefold() not in stopwords_list]

        # Find the keywords (non-stopwords)
        keywords = [word for word in words if word.isalpha()]
        keyword = ''

        # Choose a random keyword
        if keywords:
            keyword = random.choice(keywords)
            # Replace the keyword with an empty blank
            modified_sentence = sentence.replace(keyword, '____')
        else:
            modified_sentence = sentence

    elif len(keywords) == 1:
        keyword = keywords[0]
        modified_sentence = sentence.replace(keyword, '____')

    else:
        keyword = random.choice(keywords)
        # Replace the keyword with an empty blank
        modified_sentence = sentence.replace(keyword, '____')



    return keyword, modified_sentence

def generate_qa_pairs(content):

    sentences = break_into_sentences(content)

    answers = []
    mod_sentences = []
    for sentence in sentences:
        answer, mod_sentence = replace_keyword_with_blank(sentence)
        answers.append(answer)
        mod_sentences.append(mod_sentence)
        # torch.cuda.empty_cache()
    
    return answers, mod_sentences