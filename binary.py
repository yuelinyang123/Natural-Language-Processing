from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from scipy.linalg import norm
import spacy
## this is a try
nlp = spacy.load('en')
def get_binary_answer(question,target):
    voc_list=['Did','Do','May','Can','Should','Is','Are','Will','Does','Has']
    verb=[]
    question_nlp=nlp(question)
    for i in question_nlp:
        if(i.pos_=='VERB'and i.orth_ not in voc_list ):
            verb.append(i.orth_)
            
    target_list=target.split()
    answer='Yes'
    for index in range(len(target_list)):
        if(target_list[index] in verb):
            if(index<len(target_list)-1):
                if(target_list[index-1]=='not' or target_list[index+1]=='not'or target_list[index+1]=='no' ):
                    answer='No'
            else:
                if(target_list[index-1]=='not'):
                    answer='No'
  
    return answer

def tfidf_similarity(s1, s2):

  
    cv = TfidfVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
   
    first_vector=vectors[0][vectors[0]!=0]
    second_vector=vectors[1][vectors[0]!=0]
    #print(cv.get_feature_names())
    #print(first_vector)
    #print(second_vector)
    
    
    
    
    
    
    return np.dot(first_vector, second_vector) / (norm(first_vector) * norm(second_vector))

def read_file(file_name):
    sentences=[]
    with open(file_name) as f:
        lines=f.readlines()
        for line in lines:
            each_sentence=line.split('.')
            for sentence in each_sentence:
                sentences.append(sentence)
    return sentences

def similar_sentence(question, lines):
    similarity=[]
    for line in lines:
        cosine=tfidf_similarity(question, line)
        similarity.append(cosine)
    array_similar=np.array(similarity)
    x=np.argsort(-array_similar)
    return lines[x[0]]

def readquestion(filename):
    with open(filename) as f:
        questions=[]
        lines=f.readlines()
        for line in lines:
            questions.append(line.strip('\n'))
    return questions


def get_question_type(str_question):
    wh_dic=['who','when','how','whom','what','whose','why']
    words=str_question.split()
    init_word=words[0].lower()
    if init_word in wh_dic:
        return 'WH_question'
    else:
        return 'binary'

def main(corpusfile, questionfile):
    sentences=read_file(corpusfile)
    questions=readquestion(questionfile)
  
    for question in questions:
        target=similar_sentence(question, sentences)
        question_type=get_question_type(question)
        if (question_type=='binary'):
            print(question)
            print(get_binary_answer(question,target))
    
    
    
    
    
    
    
    
    
    
    

