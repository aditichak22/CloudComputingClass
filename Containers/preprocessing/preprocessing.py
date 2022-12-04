# -*- coding: utf-8 -*-
import sys
import pandas as pd
import nltk
import re
import logging
from nltk.corpus import stopwords
import unicodedata
from flask import Flask, request, json
import requests

app = Flask(__name__)
nltk.download('stopwords')
stopwords_list=stopwords.words('english')

hasData = []

def unicode_to_ascii(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
 
def clean_data(w):
    w = unicode_to_ascii(w)
    w=w.lower()                        # Lower casing
    w=re.sub(' +', ' ', w).strip(' ')  # Remove multiple whitespaces, also leading and trailing whitespaces
    w=re.sub(r'[^\w\s]','',w)          # Remove special characters and punctuation
    w=re.sub(r"([0-9])", r" ",w)       # Remove Numerical data
    w=re.sub("(.)\\1{2,}", "\\1", w)   # Remove duplicate characters
    words = w.split()                  # Tokenization

    clean_words = [word for word in words if (word not in stopwords_list) and len(word) > 2]
    return " ".join(clean_words)

@app.route('/trainingdata', methods=['POST'])
def getData():
    logging.basicConfig(level=logging.DEBUG)
    global opinions 
    opinions = pd.DataFrame(json.loads(request.json["DATA"]))
    hasData.append(True)
    logging.debug("we have the data!")
    logging.debug(hasData)
    return "200 OK"

@app.route('/datasink', methods=['POST'])
def preprocess():
    logging.basicConfig(level=logging.DEBUG)     
    logging.debug("do we have the data?")   
    logging.debug(hasData)
    if hasData and hasData[0]:
        logging.debug("in the IF")  
        opinions['text'] = opinions['text'].apply(clean_data)
        opinionsDict = {}
        opinionsDict["WFID"] = request.json["WFID"]
        logging.debug("WFID")
        logging.debug(request.json["WFID"])
        opinionsDict["PORT"] = sys.argv[1]
        logging.debug("PORT")
        logging.debug(str(sys.argv[1]))
        address = sys.argv[2]
        opinionsDict["DATA"] = opinions.to_json()
        requests.post(address, json=opinionsDict)
        logging.debug("container preprocessing complete")
        return "200 OK"
    else:
        logging.debug("I don't have data")
        return "200 NOTOK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)