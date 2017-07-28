import os
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from nltk.stem import WordNetLemmatizer
import gensim
import nltk
from numpy.random import np
import re
import csv
from csvoperations import writeToCsv
from jsonoperations import writeToJson
import sys
import codecs
from pathlib import Path
import time



'''
Author: Kunwar Singh
Topic extraction and metadata extraction from text documents using LDA algorithm
'''

SOME_FIXED_SEED = 42
arg_list = sys.argv
data_format = arg_list[0]
counter = 0
eventid = 1
source = '/Users/okt/Desktop/my_project/data/text'
path_to_save_meta = '/Users/okt/Desktop/my_project/data/text_meta'
path_to_save_meta_json = '/Users/okt/Desktop/my_project/data/text_json'

def getTopics(data,calltype = 'default'):
    """
    gets topics from data using LDA algorithm
    """
    global counter
    global eventid
    flag = 0
    tag_dict={}
    i = 0
    texts = cleanData(data)
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    # generate LDA model
    np.random.seed(SOME_FIXED_SEED)
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=1, id2word = dictionary, passes=10)
    topics = ldamodel.show_topics(num_words = 3,formatted=True)
    topic_string = topics[0][1]
    topic_final = re.findall(r'"([^"]*)"', topic_string)
    topic_keys = ['primary', 'secondary', 'tertiary']
    for topics in topic_final:
        tag_dict[topic_keys[i]] = topics
        i = i + 1
    
    if(calltype == 'create'):
        if (counter == 0 or counter == 1):
            flag = 1
            tag_dict['eventid'] = 1

        if(counter%2 == 0 and counter!=0):
            eventid = eventid+1

        counter = counter + 1
            
        if(flag!=1):
            tag_dict['eventid'] = eventid
    

    return tag_dict


    
    
    




def cleanData(data):
    texts = []
    tokenizer = RegexpTokenizer(r'\w+')
    en_stop = get_stop_words('en')
    p_stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    raw = data.lower()
    tokens = tokenizer.tokenize(raw)
    stopped_tokens = [i for i in tokens if not i in en_stop]
    stemmed_tokens = [lemmatizer.lemmatize(i) for i in stopped_tokens]
    tagged = nltk.pos_tag(stemmed_tokens)
    nouns = [word for word,pos in tagged if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    texts = [nouns]         #a list inside a list is neccessary for LDA library to work in python. texts contain another list noun

    return texts



if __name__ == '__main__':
    
    
    for root, dirs, filenames in os.walk(source):
        for f in filenames:
            if f.endswith('.txt'):
                dirpath = os.path.join(source,root)
                print(dirpath)
                fullpath = os.path.join(dirpath, f)
                with codecs.open(fullpath,encoding='utf-8', errors = 'ignore') as fw:
                    data = fw.read()
                    topics = getTopics(data, 'create')
                    topics['path'] = fullpath
                    print(topics['eventid'])
                    if(data_format == 'csv'):
                        meta_filename = f + '_meta.csv'
                        writeToCsv(path_to_save_meta,meta_filename,topics)
                    else:
                        meta_filename = f + '_meta.json'
                        writeToJson(path_to_save_meta_json,meta_filename,topics)


def getTextMetadata(path):
    global path_to_save_meta_json
    returnvalue = None
    with open('mynumber.txt', 'r') as fr:
        eventid = int(fr.read())
    
    if '.txt' not in path:
        print("not a txt file")
        returnvalue = 0
    
    try:
        if(os.path.isfile(path)):
            print("is a txt file")
            time.sleep(0.2)
            with open(Path(path), 'r') as file:
                file.flush()
                file.seek(0)
                data = file.read()

            print(data)
            topics = getTopics(data)
            topics['path'] = path
            topics['eventid'] = eventid
            basename = re.search(r'[^\\/]+(?=[\\/]?$)', path)
            if basename:
                print( "basename is %s" %basename.group(0))
                basename =  basename.group(0)
                meta_filename =  basename + '_meta.json'
                writeToJson(path_to_save_meta_json,meta_filename,topics)
                returnvalue = topics

    except:
        pass

    finally:
        return returnvalue


    
        
        

    
    





