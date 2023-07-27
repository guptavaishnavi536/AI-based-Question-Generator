import os
from pdf2image import convert_from_path
import cv2
import pytesseract

# pdfs = r"D:\Study\extra books and journals\new books\why-i-am-an-atheist.pdf"
poppler_path = r"C:\Users\singh\Downloads\ibm_qb\Models\New\poppler-23.05.0\Library\bin"

def pdf_to_image(pdfs):
    pages = convert_from_path(pdfs, 350, poppler_path=poppler_path)
    

    # Create the Images subdirectory if it doesn't exist
    output_dir = r"C:\Users\singh\Downloads\ibm_qb\Models\New\Images"
    os.makedirs(output_dir, exist_ok=True)

    i = 1
    for page in pages:
        image_name = f"{output_dir}/Page_{i}.jpg"
        page.save(image_name, "JPEG")
        i += 1

    return i

def mark_region(image_path):
    
    im = cv2.imread(image_path)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    line_items_coordinates = []
    for c in cnts:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)

        if y >= 600 and x <= 1000:
            if area > 10000:
                image = cv2.rectangle(im, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
                line_items_coordinates.append([(x,y), (2200, y+h)])

        if y >= 2400 and x<= 2000:
            image = cv2.rectangle(im, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
            line_items_coordinates.append([(x,y), (2200, y+h)])


    return image, line_items_coordinates

def ocr_im(im_path, line_items_coordinates):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

    # load the original image
    img = cv2.imread(im_path)

    # convert the image to black and white for better OCR
    ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)

    # pytesseract image to string to get results
    text = str(pytesseract.image_to_string(thresh1, config='--psm 6'))
    print(text)

    return text