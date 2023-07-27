from string import punctuation
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re

def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    return_string = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(resource_manager, return_string, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(resource_manager, device)
    with open(pdf_path, 'rb') as pdf_file:
        for page in PDFPage.get_pages(pdf_file):
            interpreter.process_page(page)
        text = return_string.getvalue()
    device.close()
    return_string.close()
    return text

# Step 3: Preprocess the text
def preprocess_text(text):
    # replace multiple whitespace with " "
    cleaned_text = re.sub(r"\s+", " ", text).strip()
    return cleaned_text

def preprocess_text_V2(sentences):
    output = []
    for sent in sentences:
        single_quotes_present = len(re.findall(r"['][\w\s.:;,!?\\-]+[']",sent))>0
        double_quotes_present = len(re.findall(r'["][\w\s.:;,!?\\-]+["]',sent))>0
        question_present = "?" in sent
        if single_quotes_present or double_quotes_present or question_present :
            continue
        else:
            output.append(sent.strip(punctuation))
    return output