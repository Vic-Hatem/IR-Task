import nltk
import html2text as html2text
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#nltk.download('stopwords')
#nltk.download('punkt')
cwd = os.getcwd()
emotionalFile = open(cwd + "/eng/joy.txt", "r")
joy = nltk.word_tokenize(emotionalFile.read())

words_per_doc=[]

trustTerms = ["loyalty", "reliance", "fraud", "forgery", "trust", "confidence", "covenant", "pledge", "promise",
                  "warn", "alert", "flatter", "compliment", "periphrasis", "lie"]
punc = '''!()-[]{};:'"\, <>``''./?@#$%^&*_~=+'''

def readingfiles(docID):

    docCollectionSentencesCounter = 0
    dict = {}

    for trust in trustTerms:
        dict[trust] = []

    path = "/English/"
    for filename in os.listdir(cwd + path):
        file = open(cwd + path + filename, "r")
        h = html2text.HTML2Text()
        h.ignore_links = True
        fileText = h.handle(file.read())
        if fileText is not None:
            docCollectionSentencesCounter +=tokenizer(fileText, docID, dict)
        docID = docID + 1


    for key in dict.keys():
        if key != 'joy':
            trust_doc_counter=0
            trust_sent_counter = 0
            check_doc_duplicate=""
            check_sent_duplicate = ""
            for l in dict[key]:
                if check_doc_duplicate!=str(l).split('S')[0]:
                    trust_doc_counter+=1
                    trust_sent_counter += 1
                elif check_sent_duplicate!=str(l).split('S')[-1]:
                    trust_sent_counter += 1

                check_sent_duplicate = str(l).split('S')[1]
                check_doc_duplicate = str(l).split('S')[0]

            print("Term "+key+":")
            print("Collection Frequency is: " + str(len(dict[key])))
            print("Document Frequency: "+str(trust_doc_counter)+" Percentage for overall: "+str("{:.4f}".format((float((trust_doc_counter/docID))*100)))+"%")
            print("Sentence Frequency: "+str(trust_sent_counter)+" Percentage for overall: "+str("{:.4f}".format((float(trust_sent_counter/docCollectionSentencesCounter))*100))+"%")
            match_prob_sent,match_prob_doc = matchingPerDoc(dict, trust_term=key)
            print("Matches Sentence Frequency: "+str(match_prob_sent)+" Percentage for overall: "+str("{:.4f}".format((float((match_prob_sent/docCollectionSentencesCounter))*100)))+"%")
            print("Matches Document Frequency: " + str(match_prob_doc) + " Percentage for overall: " + str("{:.4f}".format((float((match_prob_doc/docID)) * 100))) + "%")

            print("--------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("--------------------------------------------------------------------------------------------------------------------------------------------------------")


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def tokenizer(text, docID, dict):
    ps = PorterStemmer()
    filteredWords = []
    stop_words = set(stopwords.words('english'))
    sentences = nltk.sent_tokenize(text.casefold())
    docSentencesCounter = len(sentences)
    for i in range(len(sentences)):
        words = nltk.word_tokenize(sentences[i])
        for word in words:
            if word not in stop_words and word not in punc and hasNumbers(word) == False:
                if word in joy:
                    if 'joy' in dict.keys():
                        if "D" + str(docID) + "S" + str(i) not in dict['joy']:
                            dict['joy'].append("D" + str(docID) + "S" + str(i))
                    else:
                        dict['joy'] = ["D" + str(docID) + "S" + str(i)]
                    filteredWords.append("joy")
                elif word in trustTerms:
                    if word in dict.keys():
                        if "D" + str(docID) + "S" + str(i) not in dict[word]:
                            dict[word].append("D" + str(docID) + "S" + str(i))
                    else:
                        dict[word] = ["D" + str(docID) + "S" + str(i)]

    return docSentencesCounter


def matchingPerDoc(dict,trust_term):
    joylist = set(dict['joy'])
    trustList = set(dict[trust_term])
    set1 = joylist.intersection(trustList)
    doc_counter = 0
    doc_duplicate = ""
    for s in set1:
        if doc_duplicate != str(s).split('S')[0]:
            doc_counter += 1
        doc_duplicate = str(s).split('S')[0]
    return len(set1),doc_counter


readingfiles(1)
