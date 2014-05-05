import nltk
from nltk.corpus import wordnet
import csv
from nltk import word_tokenize, wordpunct_tokenize
from sentiwordnet import *
import xml.etree.ElementTree as ET
import codecs
from nltk.tag.simplify import simplify_wsj_tag

def createDataList(path):
    '''
    input : .csv file path
    return: tweets in a list (text only, no meta data)
    '''         
    dataFile = open(path, 'rb')  
    dataReader = csv.reader(dataFile, delimiter=',')
    data = []
    
    for row in dataReader:
        l = []
        l.append(row[0])
        l.append(row[5])
        data.append(l)
            
    return data


def createTreeFromXML(path):
    '''
    input: .xml file path
    return: tree 
    '''
    
    tree = ET.parse(path)
    return tree
               
def getSentimentFromTweet1(tweet, dico, swn):
    '''
    input: preprocessed tweet = [(word,PoS), (word, PoS) ... ] ; dico = dictionnary which links PoS of nltk to PoS of synsets, swn = sentiwordnet corpus reader
    return: posScore,negScore, sentiment = an int equal to 0 (negative), 2(neutral) or 4(positive)
    
    Summary: Just add pos scores and neg scores  
    ''' 
        
    posScore = 0
    negScore = 0
    
    for couple in tweet:
        synset = None
        if couple[1] in dico:
            synsets = swn.senti_synsets(couple[0])
            for elem in synsets:
                if (elem.synset.pos == dico[couple[1]]):
                    synset = elem
                    break
            if synset != None:
                posScore = posScore + synset.pos_score
                negScore = negScore + synset.neg_score
    
    if (posScore > negScore):
        sentiment = 4
    elif (posScore == negScore):
        sentiment = 2
    else:
        sentiment = 0
    
    return [posScore, negScore, sentiment]

def getSentimentFromTweet2(tweet, dico, listNeg, listBoost, swn):
    '''
    input: preprocessed tweet = [(word,PoS), (word, PoS) ... ]; dico = dictionnary which links PoS of nltk to PoS of synsets, swn = sentiwordnet corpus reader, listNeg and listBoost
    return: posScore,negScore, sentiment = an int equal to 0 (negative), 2(neutral) or 4(positive) 
    
    Summary: same as before, but checks the word before and invert or multiply by 2 if in neglist or boostlist
    ''' 

    posScore = 0
    negScore = 0
    
    for index, couple in enumerate(tweet):
        synset = None
        if couple[1] in dico:
            synsets = swn.senti_synsets(couple[0])
            for elem in synsets:
                if (elem.synset.pos == dico[couple[1]]):
                    synset = elem
                    break
            if synset != None:
                if (index > 0):
                    coupleBefore = tweet[(index-1)]
                    wordBefore = coupleBefore[0]
                    if wordBefore in listNeg:
                        posScore = posScore + synset.neg_score
                        negScore = negScore + synset.pos_score
                    elif wordBefore in listBoost:
                        posScore = posScore + 2*synset.pos_score
                        negScore = negScore + 2*synset.neg_score
                    else: 
                        posScore = posScore + synset.pos_score
                        negScore = negScore + synset.neg_score
                else:
                    posScore = posScore + synset.pos_score
                    negScore = negScore + synset.neg_score                    
    
    if (posScore > negScore):
        sentiment = 4
    elif (posScore == negScore):
        sentiment = 2
    else:
        sentiment = 0
    
    return [posScore, negScore, sentiment]

def getSentimentFromTweet3(tweet, dico, listNeg, listBoost, swn):
    '''
    input: preprocessed tweet = [(word,PoS), (word, PoS) ... ]; dico = dictionnary which links PoS of nltk to PoS of synsets, swn = sentiwordnet corpus reader, listNeg and listBoost
    return: posScore,negScore, sentiment = an int equal to 0 (negative), 2(neutral) or 4(positive) 
    
    Summary: Same as before but considers words for which posScore= negScore as boosterWords 
    ''' 
    

    
    posScore = 0
    negScore = 0
    boosterWord = False
    
    for index, couple in enumerate(tweet):
        synset = None
        if couple[1] in dico:
            synsets = swn.senti_synsets(couple[0])
            for elem in synsets:
                if (elem.synset.pos == dico[couple[1]]):
                    synset = elem
                    break
            if synset != None:
                if (synset.neg_score == synset.pos_score):
                    boosterWord = True
                elif (index > 0):
                    coupleBefore = tweet[(index-1)]
                    wordBefore = coupleBefore[0]
                    if wordBefore in listNeg:
                        posScore = posScore + synset.neg_score
                        negScore = negScore + synset.pos_score
                    elif (wordBefore in listBoost) or (boosterWord):
                        posScore = posScore + 2*synset.pos_score
                        negScore = negScore + 2*synset.neg_score
                    else:
                        posScore = posScore + synset.pos_score
                        negScore = negScore + synset.neg_score    
                    boosterWord = False
                else:
                    posScore = posScore + synset.pos_score
                    negScore = negScore + synset.neg_score                    
    
    if (posScore > negScore):
        sentiment = 4
    elif (posScore == negScore):
        sentiment = 2
    else:
        sentiment = 0
    
    return [posScore, negScore, sentiment]

def getSentimentFromTweet4(tweet, dico, listNeg, listBoost, swn):
    '''
    input: preprocessed tweet = [(word,PoS), (word, PoS) ... ]; dico = dictionnary which links PoS of nltk to PoS of synsets, swn = sentiwordnet corpus reader, listNeg and listBoost
    return: posScore,negScore, sentiment = an int equal to 0 (negative), 2(neutral) or 4(positive) 
    
    Summary: Same as 2 but either negScore or posScore is added for each word, not both
    ''' 
    
    posScore = 0
    negScore = 0
    
    for index, couple in enumerate(tweet):
        synset = None
        if couple[1] in dico:
            synsets = swn.senti_synsets(couple[0])
            for elem in synsets:
                if (elem.synset.pos == dico[couple[1]]):
                    synset = elem
                    break
            if synset != None:
                if (index > 0):
                    coupleBefore = tweet[(index-1)]
                    wordBefore = coupleBefore[0]
                    if wordBefore in listNeg:
                        if (synset.pos_score > synset.neg_score):
                            negScore = negScore + synset.pos_score
                        else:
                            posScore = posScore + synset.neg_score
                    elif (wordBefore in listBoost):
                        if (synset.pos_score > synset.neg_score):
                            posScore = posScore + 2*synset.pos_score
                        else:
                            negScore = negScore + 2*synset.neg_score
                    else:
                        if (synset.pos_score > synset.neg_score):
                            posScore = posScore + synset.pos_score
                        else:
                            negScore = negScore + synset.neg_score
                else:
                    if (synset.pos_score > synset.neg_score):
                        posScore = posScore + synset.pos_score
                    else:
                        negScore = negScore + synset.neg_score                    
    
    if (posScore > negScore):
        sentiment = 4
    elif (posScore == negScore):
        sentiment = 2
    else:
        sentiment = 0
    
    return [posScore, negScore, sentiment]
    
def getSentimentFromTweet5(tweet, dico, listNeg, listBoost, swn):
    '''
    input: preprocessed tweet = [(word,PoS), (word, PoS) ... ]; dico = dictionnary which links PoS of nltk to PoS of synsets, swn = sentiwordnet corpus reader, listNeg and listBoost
    return: posScore,negScore, sentiment = an int equal to 0 (negative), 2(neutral) or 4(positive) 
    
    Summary: Same as 2, but checks whether n-2 word is a negative word
    ''' 
        
    posScore = 0
    negScore = 0
    
    for index, couple in enumerate(tweet):
        synset = None
        if couple[1] in dico:
            synsets = swn.senti_synsets(couple[0])
            for elem in synsets:
                if (elem.synset.pos == dico[couple[1]]):
                    synset = elem
                    break
            if synset != None:
                if (index > 0):
                    coupleBefore = tweet[(index-1)]
                    wordBefore = coupleBefore[0]
                    if wordBefore in listNeg:
                        posScore = posScore + synset.neg_score
                        negScore = negScore + synset.pos_score       
                    elif (wordBefore in listBoost):
                        if (index > 1):
                            coupleBeforeBis = tweet[(index-2)]
                            wordBeforeBis = coupleBeforeBis[0]
                            if wordBeforeBis in listNeg:
                                posScore = posScore + 0.5*synset.neg_score
                                negScore = negScore + 0.5*synset.pos_score
                            else:
                                posScore = posScore + 2*synset.pos_score
                                negScore = negScore + 2*synset.neg_score
                        else:
                            posScore = posScore + 2*synset.pos_score
                            negScore = negScore + 2*synset.neg_score 
                    else:
                        if (index > 1):
                            coupleBeforeBis = tweet[(index-2)]
                            wordBeforeBis = coupleBeforeBis[0]
                            if wordBeforeBis in listNeg:
                                posScore = posScore + synset.neg_score
                                negScore = negScore + synset.pos_score 
                            else:
                                posScore = posScore + synset.pos_score
                                negScore = negScore + synset.neg_score    
                        else:
                            posScore = posScore + synset.pos_score
                            negScore = negScore + synset.neg_score
                else:
                    posScore = posScore + synset.pos_score
                    negScore = negScore + synset.neg_score                    
    
    if (posScore > negScore):
        sentiment = 4
    elif (posScore == negScore):
        sentiment = 2
    else:
        sentiment = 0
    
    return [posScore, negScore, sentiment]
                                                                                                                                                                                                                                                                
def getSentimentFromTweet6(tweet, dico, listNeg, listBoost, listPosEmoticons, listNegEmoticons, swn):
    '''
    input: preprocessed tweet = [(word,PoS), (word, PoS) ... ]; dico = dictionnary which links PoS of nltk to PoS of synsets, swn = sentiwordnet corpus reader, listNeg and listBoost
    return: posScore,negScore, sentiment = an int equal to 0 (negative), 2(neutral) or 4(positive) 
    
    Summary: Same as before + emoticons
    ''' 
    
    
    posScore = 0
    negScore = 0
    
    for index, couple in enumerate(tweet):
        synset = None
        if couple[0] in listPosEmoticons:
            posScore = posScore+1
        elif couple[0] in listNegEmoticons: 
            negScore = negScore+1   
        elif couple[1] in dico:
            synsets = swn.senti_synsets(couple[0])
            for elem in synsets:
                if (elem.synset.pos == dico[couple[1]]):
                    synset = elem
                    break
            if synset != None:
                if (index > 0):
                    coupleBefore = tweet[(index-1)]
                    wordBefore = coupleBefore[0]
                    if wordBefore in listNeg:
                        posScore = posScore + synset.neg_score
                        negScore = negScore + synset.pos_score       
                    elif (wordBefore in listBoost):
                        if (index > 1):
                            coupleBeforeBis = tweet[(index-2)]
                            wordBeforeBis = coupleBeforeBis[0]
                            if wordBeforeBis in listNeg:
                                posScore = posScore + 0.5*synset.neg_score
                                negScore = negScore + 0.5*synset.pos_score
                            else:
                                posScore = posScore + 2*synset.pos_score 
                                negScore = negScore + 2*synset.neg_score
                        else:
                            posScore = posScore + 2*synset.pos_score 
                            negScore = negScore + 2*synset.neg_score 
                    else:
                        if (index > 1):
                            coupleBeforeBis = tweet[(index-2)]
                            wordBeforeBis = coupleBeforeBis[0]
                            if wordBeforeBis in listNeg:
                                posScore = posScore + synset.neg_score
                                negScore = negScore + synset.pos_score 
                            else:
                                posScore = posScore + synset.pos_score
                                negScore = negScore + synset.neg_score    
                        else:
                            posScore = posScore + synset.pos_score
                            negScore = negScore + synset.neg_score
                else:
                    posScore = posScore + synset.pos_score
                    negScore = negScore + synset.neg_score                    
    
    if (posScore > negScore):
        sentiment = 4
    elif (posScore == negScore):
        sentiment = 2
    else:
        sentiment = 0
    
    return [posScore, negScore, sentiment]

def getSentimentFromTweet7(tweet, dico, listNeg, listBoost, listPosEmoticons, listNegEmoticons, swn, dicoSlang):
    '''
    input: tweet = string ; dico = dictionnary which links PoS of nltk to PoS of synsets, swn = sentiwordnet corpus reader, listNeg and listBoost
    return: posScore,negScore, sentiment = an int equal to 0 (negative), 2(neutral) or 4(positive) 
    
    Summary: Only the best neg and best pos are taken into account
    ''' 
    
    tokenizedData = tweet.split(' ')
    PreProcessedTokenizedData = preProcess(tokenizedData, dicoSlang)
    taggedData = nltk.pos_tag(PreProcessedTokenizedData)
    simplifiedData = [(word, simplify_wsj_tag(tag)) for word, tag in taggedData]
    
    posScore = 0
    negScore = 0
    boosterWord = False
    
    for index, couple in enumerate(simplifiedData):
        synset = None
        if couple[0] in listPosEmoticons:
            if posScore < 1:
                posScore = 1
        elif couple[0] in listNegEmoticons:
            if negScore < 1: 
                negScore = 1   
        elif couple[1] in dico:
            synsets = swn.senti_synsets(couple[0])
            for elem in synsets:
                if (elem.synset.pos == dico[couple[1]]):
                    synset = elem
                    break
            if synset != None:
                if (synset.neg_score == synset.pos_score):
                    boosterWord = True
                elif (index > 0):
                    coupleBefore = simplifiedData[(index-1)]
                    wordBefore = coupleBefore[0]
                    if wordBefore in listNeg:
                        if posScore < synset.neg_score:
                            posScore = synset.neg_score
                        if negScore < synset.pos_score:
                            negScore = synset.pos_score       
                    elif (wordBefore in listBoost) or (boosterWord):
                        if (index > 1):
                            coupleBeforeBis = simplifiedData[(index-2)]
                            wordBeforeBis = coupleBeforeBis[0]
                            if wordBeforeBis in listNeg:
                                if posScore < (synset.neg_score + 1):
                                    posScore = synset.neg_score + 1
                                if negScore < (synset.pos_score + 1):
                                    negScore = synset.pos_score + 1
                            else:
                                if posScore < (synset.pos_score + 1):
                                    posScore = synset.pos_score + 1
                                if negScore < (synset.neg_score + 1):
                                    negScore = synset.neg_score + 1
                        else:                           
                            if posScore < (synset.pos_score + 1):
                                posScore = synset.pos_score + 1
                            if negScore < (synset.neg_score + 1):
                                negScore = synset.neg_score + 1
                    else:
                        if (index > 1):
                            coupleBeforeBis = simplifiedData[(index-2)]
                            wordBeforeBis = coupleBeforeBis[0]
                            if wordBeforeBis in listNeg:
                                if posScore < synset.neg_score:
                                    posScore =  synset.neg_score
                                if negScore < synset.pos_score:
                                    negScore = synset.pos_score 
                            else:
                                if posScore < synset.pos_score:
                                    posScore = synset.pos_score
                                if negScore < synset.neg_score:
                                    negScore = synset.neg_score    
                        else:
                            if posScore < synset.pos_score:
                                posScore = synset.pos_score
                            if negScore < synset.neg_score:
                                negScore = synset.neg_score 
                    boosterWord = False
                else:
                    if posScore < synset.pos_score:
                        posScore = synset.pos_score
                    if negScore < synset.neg_score:
                        negScore = synset.neg_score                    
    if (posScore > negScore):
        sentiment = 4
    elif (posScore == negScore):
        sentiment = 2
    else:
        sentiment = 0
    
    return [posScore, negScore, sentiment]


def preProcess(tweet, dicoSlang):
    
    preProcessedTokens = []
    tokens = tweet.split(' ')
    for token in tokens:
        if len(token) > 0 :
            if token[0] != '@':
                if token[0] == '#':
                    token = token.replace('#','')
                if token in dicoSlang:
                    newTokens = dicoSlang[token]
                    newTokensBis = newTokens.split(' ')
                    for newToken in newTokensBis:
                        preProcessedTokens.append(newToken)    
                else:
                    preProcessedTokens.append(token)
                
    taggedData = nltk.pos_tag(preProcessedTokens)
    simplifiedData = [(word, simplify_wsj_tag(tag)) for word, tag in taggedData] 
               
    return simplifiedData

    