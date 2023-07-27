from . import pdf_read
from . import ocr
from . import mcq
from . import fib
from . import to_doc
from . import tnf
from . import fib
from . import tnf_v2
import torch

def extract(path):

    complete_text = ''
        
    text = pdf_read.extract_text_from_pdf(path)

    # extract text w/o ocr
    if text!='':
        clean_text = pdf_read.preprocess_text(text)

        complete_text = str(clean_text)


    # using ocr if no text found
    else:

        num_pages = ocr.pdf_to_image(path)

        for i in range(1,num_pages):
            im_path = f"Images/Page_{i}.jpg"
            im, line_items_coordinates = ocr.mark_region(image_path=im_path)
            
            # print(im, line_items_coordinates)

            text = ocr.ocr_im(im_path, line_items_coordinates)

            clean_text = pdf_read.preprocess_text(text)

            complete_text = complete_text + "\n" + clean_text

        # print(complete_text)
        complete_text = str(complete_text)


    return complete_text

def summary_fn(complete_text):
    # uncomment for main
    processed_text = mcq.postprocesstext(complete_text)
    summarized_text = mcq.summarizer(processed_text)
    print()
    print("Summary: \n")
    print(summarized_text)
    torch.cuda.empty_cache()

    # removing digits from summarized text
    no_dig_text = ''.join([i for i in summarized_text if not i.isdigit()])

    return summarized_text, no_dig_text

def mcq_gen(summarized_text, no_dig_text):

    answers = mcq.get_nouns_multipartite(no_dig_text)

    answers = list(set(answers))

    print(answers)

    questions = []
    distractor = []
    for answer in answers:
  
        ques = mcq.gen(summarized_text,answer)

        # ques = mcq.gen(complete_text, answer)

        questions.append(ques)
        # distractor[answer] = get_distractors_wordnet(answer)
        distractor.append(mcq.get_distractors(answer, ques))
    
    content = ''

    distractor2 = []
    dist = ''
    flag = 0
    for i in distractor:
        for j in i:
            dist+=j + ", "
            flag = 1
        if flag == 1:
            distractor2.append(dist[:-1])
        else:
            distractor2.append(dist)

        flag = 0
        dist = ''

    distractor = distractor2
    print(distractor)

    for i in range(len(questions)):
        questions[i] = questions[i].replace("<pad> ", "").replace("</s>", "")
   
        content += '\n' + questions[i] + "\n Ans: " + answers[i].capitalize() + "\n" + distractor[i]

    return questions, answers, distractor

def qna_gen(summarized_text, no_dig_text):
   
    answers = mcq.get_nouns_multipartite(no_dig_text)
    
    

    answers = list(set(answers))

    print(answers)

    questions = []
    for answer in answers:
   
        ques = mcq.gen(summarized_text,answer)

        # ques = mcq.gen(complete_text, answer)

        questions.append(ques)
    
    content = ''

    for i in range(len(questions)):
        questions[i] = questions[i].replace("<pad> ", "").replace("</s>", "")
     
        content += '\n' + questions[i] + '\n Ans: ' + answers[i].capitalize()
        
    return questions, answers

def fib_gen(no_dig_text):
    

    answers, mod_sentences = fib.generate_qa_pairs(no_dig_text)

    content = ''

    for i in range(len(answers)):
        
        content += '\n\n' + mod_sentences[i] + '\n Ans: ' + answers[i].capitalize()


    return mod_sentences, answers

def tnf_gen(no_dig_text):


    questions = tnf.tnf(no_dig_text)

    return questions

def tnf_v2_gen(no_dig_text):
    cand_sents = tnf_v2.get_candidate_sents(no_dig_text)
    # filter_quotes_and_questions = tnf_v2.preprocess(cand_sents)
    filter_quotes_and_questions = cand_sents
    
    # debug
    print("filter quotes")
    print(filter_quotes_and_questions)
    
    sent_completion_dict = tnf_v2.get_sentence_completions(filter_quotes_and_questions)

    # debug
    print("sent dict")
    print(sent_completion_dict)

    index = 1
    # choice_list = ["a)","b)","c)","d)","e)","f)"]
    true_sentences = []
    false_sentences = []
    for key_sentence in sent_completion_dict:
        true_sentences.append(key_sentence)
        partial_sentences = sent_completion_dict[key_sentence]
        false_sentence =[]


        for partial_sent in partial_sentences:
            false_sents = tnf_v2.generate_sentences(partial_sent,key_sentence)
            false_sentence.extend(false_sents)

        false_sentences.append(false_sentence)
        index = index+1

    print(true_sentences)
    print(false_sentences)
    return true_sentences, false_sentences

def write_to_doc3(p1, p2, p3):
    content = ''
    for i in range(len(p1)):
        p1[i] = p1[i].replace("<pad> ", "").replace("</s>", "")


        content += '\n' + p1[i] + "\n Ans: " + p2[i].capitalize() + "\n" + p3[i] + "\n"


    return content

def write_to_doc2(p1, p2):
    content = ''
    for i in range(len(p1)):
        p1[i] = p1[i].replace("<pad> ", "").replace("</s>", "")


        content += '\n' + p1[i] + "\n Ans: " + p2[i].capitalize()


    return content

def write_to_doc_lol(p1, p2):
    content = ''
    for i in range(len(p1)):
        p1[i] = p1[i].replace("<pad> ", "").replace("</s>", "")

        content += '\n\nTrue: \n' + p1[i] + '\nFalse: '
        for j in range(len(p2[i])):
            content +=  '\n' + p2[i][j].capitalize()

    return content

def write_to_doc(p1):
    content = ''
    for i in range(len(p1)):
        p1[i] = p1[i].replace("<pad> ", "").replace("</s>", "")
        # print("Question: ", questions[i])
        # print("Ans: ", answers[i].capitalize())
        # print("Distractor: ", distractor[i])

        content += '\n' + p1[i]


    # to_doc.todoc(content, string)
    # print("Doc exported.")

    return content

def generate(path, option):
    text = extract(path)
    content = summary = no_dig_text = ''
    summary, no_dig_text = summary_fn(text)
    string = option
    if option=='mcq':
        # mcq generation
        questions, answers, distractors = mcq_gen(summary, no_dig_text)
        content += write_to_doc3(questions, answers, distractors)

    elif option == 'qna':
        # # qna generation
        questions, answers = qna_gen(summary, no_dig_text)
        content += write_to_doc2(questions, answers)
    
    elif option == 'tnf':
        # tnf generation
        questions = tnf_gen(no_dig_text)
        content += write_to_doc(questions)

    elif option == 'tnf_v2':
        true_sentences, false_sentences = tnf_v2_gen(no_dig_text)
        content += write_to_doc_lol(true_sentences, false_sentences)

    elif option =='fib':
        # # fib generation
        mod_sentences, answers = fib_gen(no_dig_text)
        content += write_to_doc2(mod_sentences, answers)

    elif option == 'combined':
        # mcq generation
        questions, answers, distractors = mcq_gen(summary, no_dig_text)
        content += '\n MCQ:\n' + write_to_doc3(questions, answers, distractors) + '\n'
        # # qna generation
        questions, answers = qna_gen(summary, no_dig_text)
        content += '\n QnA:\n' + write_to_doc2(questions, answers) + '\n'

        mod_sentences, answers = fib_gen(no_dig_text)
        content += '\n FIB:\n' + write_to_doc2(mod_sentences, answers) + '\n'
        # tnf v2 generation
        true_sentences, false_sentences = tnf_v2_gen(no_dig_text)
        content += '\n TnF:\n' + write_to_doc_lol(true_sentences, false_sentences) + '\n'

    to_doc.todoc(content, string)


if __name__ == "__main__":

    
    text = 'sample text'


    # uncomment for main
    summary, no_dig_text = summary_fn(text)   
    
    content = ''

    option = input("Enter choice: ")

    if option=='mcq':
        # mcq generation
        questions, answers, distractors = mcq_gen(summary, no_dig_text)
        content += write_to_doc3(questions, answers, distractors)

    elif option == 'qna':
        # # qna generation
        questions, answers = qna_gen(summary, no_dig_text)
        content += write_to_doc2(questions, answers)
    
    elif option == 'tnf':
        # tnf generation
        questions = tnf_gen(no_dig_text)
        content += write_to_doc(questions)

    elif option == 'tnf_v2':
        true_sentences, false_sentences = tnf_v2_gen(no_dig_text)
        content += write_to_doc_lol(true_sentences, false_sentences)

    elif option =='fib':
        # # fib generation
        mod_sentences, answers = fib_gen(no_dig_text)
        content += write_to_doc2(mod_sentences, answers)

    elif option == 'combined':
        # mcq generation
        questions, answers, distractors = mcq_gen(summary, no_dig_text)
        content += '\n MCQ:\n' + write_to_doc3(questions, answers, distractors) + '\n'
        # # qna generation
        questions, answers = qna_gen(summary, no_dig_text)
        content += '\n QnA:\n' + write_to_doc2(questions, answers) + '\n'
        # tnf generation
        # questions = tnf_gen(no_dig_text)
        # content += write_to_doc(questions)
        # # fib generation
        mod_sentences, answers = fib_gen(no_dig_text)
        content += '\n FIB:\n' + write_to_doc2(mod_sentences, answers) + '\n'
        # tnf v2 generation
        true_sentences, false_sentences = tnf_v2_gen(no_dig_text)
        content += '\n TnF:\n' + write_to_doc_lol(true_sentences, false_sentences) + '\n'

    string = input("Enter filename: ")

    to_doc.todoc(content, string)
    print("Doc exported.")