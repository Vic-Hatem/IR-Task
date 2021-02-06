import nltk
import html2text as html2text
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# nltk.download('stopwords')
# nltk.download('punkt')
cwd = os.getcwd()
emotionalFile=open(cwd+"/eng/joy.txt","r")
joy=nltk.word_tokenize(emotionalFile.read())


def readingfiles(docID):
    df=pd.DataFrame(columns=['DocID','Probability'])
    # df.append(pd.DataFrame(data=[5,0.2]))
    # sns.regplot(x=df['DocID'], y=df['Probability'], fit_reg=False)
    plt.xlabel('DocID')
    plt.ylabel('Probability')

    docCollectionSentencesCounter = 0
    dict={}
    path="/English/"
    for filename in os.listdir(cwd+path):
        file = open(cwd+path+filename,"r")
        h = html2text.HTML2Text()
        h.ignore_links = True
        fileText = h.handle(file.read())
        if fileText is not None:
            docCollectionSentencesCounter=docCollectionSentencesCounter+tokenizer(fileText, docID, dict,df)
        docID=docID+1
    print("The probability of emotional and trust terms occured in one sentence in the collection is: "+str(matchingPerCollection(dict,docCollectionSentencesCounter))+" and there is : "+str(docCollectionSentencesCounter)+" sentences in the collection!")

    plt.show()

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def tokenizer(text,docID,dict,df):
    ps=PorterStemmer()
    filteredWords=[]
    punc = '''!()-[]{};:'"\, <>``''./?@#$%^&*_~=+'''
    trustTerms=["loyalty","reliance","fraud","forgery","trust","confidence","covenant","pledge","promise","warn","alert","flatter","compliment","periphrasis","lie"]

    stop_words = set(stopwords.words('english'))
    sentences=nltk.sent_tokenize(text.casefold())
    docSentencesCounter=len(sentences)
    if docSentencesCounter == 0:
        return 0
    for i in range(len(sentences)):
        words=nltk.word_tokenize(sentences[i])
        for word in words:
            if word not in stop_words and word not in punc and hasNumbers(word)==False:
                if word in joy:
                    if 'joy' in dict.keys():
                        if "D" + str(docID) + "S" + str(i) not in dict['joy']:
                            dict['joy'].append("D" + str(docID) + "S" + str(i))
                    else:
                        dict['joy'] = ["D" + str(docID) + "S" + str(i)]
                    filteredWords.append("joy")
                elif word in trustTerms:
                    if 'trust' in dict.keys():
                        if "D" + str(docID) + "S" + str(i) not in dict['trust']:
                            dict['trust'].append("D" + str(docID) + "S" + str(i))
                    else:
                        dict['trust'] = ["D" + str(docID) + "S" + str(i)]
    if matchingPerDoc(dict,docSentencesCounter,docID)!=0:
        plt.plot(docID,matchingPerDoc(dict,docSentencesCounter,docID),'ro',color='green')
    print("Document: "+str(docID)+" the probability is= "+str(matchingPerDoc(dict,docSentencesCounter,docID))+" sentences= "+str(docSentencesCounter))
    return docSentencesCounter

def matchingPerDoc(dict,docSentencesCounter,docID):
    if 'joy' in dict.keys() and 'trust' in dict.keys():
        joylist=set(dict['joy'])
        trustList=set(dict['trust'])
        set1=joylist.intersection(trustList)
        matchCounter=0
        for i in set1:
            if i.find("D"+str(docID))!=-1:
                matchCounter=matchCounter+1
        return (float(matchCounter/docSentencesCounter))
    return 0


def matchingPerCollection(dict,docCollectionSentencesCounter):
    if 'joy' in dict.keys() and 'trust' in dict.keys():
        joylist=set(dict['joy'])
        trustList=set(dict['trust'])
        matchCounter = len(joylist.intersection(trustList))
        return (float(matchCounter/docCollectionSentencesCounter))
    return 0
readingfiles(1)