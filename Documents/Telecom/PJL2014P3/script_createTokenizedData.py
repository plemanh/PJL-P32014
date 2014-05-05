# -*- coding: utf-8 -*-
from functions import *
from sentiwordnet import *
import random

path1 = '/Users/paullemanh/Documents/Telecom/PJL2014P3/SentiWordNet.txt'
swn = SentiWordNetCorpusReader(path1)

path1 = '/Users/paullemanh/Documents/Telecom/PJL2014P3/testdata.csv'

data = createDataList(path1)

dico = {
'ADJ':'a', 'ADV':'r','N':'n','V':'v','VD':'v','VG':'v','VN':'v'
}

listNeg = ["aren't","arent""can't","cannot","cant""couldn't","couldnt","don't","dont","isn't","isnt","never","not","won't","wont","wouldn't","wouldnt"]

listBoost = ["absolutely","complete","completely","definitely","especially","extremely","fuckin","fucking","hugely","incredibly","overwhelmingly","really","so","total","totally","very"]

listPosEmoticons = ["^_^","--^--@",";^)",":-)",":-}",":-*",":-*",":-D",":-P",":)",":]",":3",":9",":b)",":D",":o)",":P",":P",":p",":X",":Þ","(^ ^)","(^_^)","(^-^)","(^.^)","(-:","(:","(o:","}:)","@}->--","*\o/*","%-)","<3","=)","=]",">:)",">:D",">=D","|D","0:)","8)","x3?","XD","xD","XP"]

listNegEmoticons = ["^o)",":_(",":-(",":-(o)",":-/",":-&",":-|",":-S",":,(",":…(",":'-(",":'(",":(",":[",":[",":*(",":/", ":#",":|",":E",":F",":O",":o(",":S",":s",")-:","):",")o:","%-(","</3-1","<o<","=(","=[",">:(",">:L",">:O",">[",">/",">o>","|8C","|8c","38*","8-0","8/","8c","B(","Bc","D:","X-(","X(","X(","XO"]

dicoSlang = {"121":"one to one", "a/s/l":"age sex location", "adn":"any day now", "afaik":"as far as I know", "afk":"away from keyboard", "aight":"alright", "alol":"actually laughing out loud","b4"	: "before","b4n"	: "bye for now","bak"	: "back at the keyboard","bf"	: "boyfriend","bff"	: "best friends forever","bfn"	: "bye for now","bg"	: "big grin","bta"	: "but then again","btw"	: "by the way","cid"	: "crying in disgrace","cnp"	: "continued in my next post","cp"	: "chat post","cu"	: "see you","cul" 	: "see you later","cul8r"	: "see you later","cya"	: "bye","cyo"	: "see you online","dbau"	: "doing business as usual","fud"	: "fear, uncertainty, and doubt","fwiw"	: "for what it's worth","fyi"	: "for your information","g"	: "grin†","g2g"	: "got to go","ga"	: "go ahead","gal"	: "get a life","gf"	: "girlfriend","gfn"	: "gone for now","gmbo"	: "giggling my butt off","gmta"	: "great minds think alike","h8"	: "hate","hagn"	: "have a good night","hdop"	: "help delete online predators","hhis"	: "hanging head in shame","iac"	: "in any case","ianal"	: "I am not a lawyer","ic"	: "I see","idk"	: "I don't know","imao"  : "in my arrogant opinion","imnsho": "in my not so humble opinion","imo"	: "in my opinion","iow"	: "in other words","ipn"	: "I'm posting naked","irl"	: "in real life","jk"	: "just kidding","l8r"	: "later","ld"	: "later, dude","ldr"	: "long distance relationship","llta"	: "lots and lots of thunderous applause","lmao"	: "laugh my ass off","lmirl"	: "let's meet in real life","lol"	: "laugh out loud","ltr"	: "longterm relationship","lulab"	: "love you like a brother","lulas"	: "love you like a sister","luv"	: "love","m/f"	: "male or female","m8"	: "mate","milf"	: "mother I would like to fuck","oll"	: "online love","omg"	: "oh my god","otoh"	: "on the other hand","pir"	: "parent in room","ppl"	: "people","r"	: "are","rofl"	: "roll on the floor laughing","rpg"	: "role playing games","ru"	: "are you","shid"	: "slaps head in disgust","somy"	: "sick of me yet","sot"	: "short of time","thanx"	: "thanks","thx"	: "thanks","ttyl"	: "talk to you later","u"	: "you","ur" 	: "you are","uw"	: "you are welcome","wb"	: "welcome back","wfm"	: "works for me","wibni"	: "wouldn't it be nice if","wtf"	: "what the fuck","wtg"	: "way to go","wtgp"	: "want to go private","ym"	: "young man"}

#Creation of the data set
usedData = []
i = 0
while i < 450:
    tweet = random.choice(data)
    usedData.append(tweet)
    data.remove(tweet)
    i = i+1     


#Test for version 1

nbPos = 0
nbNeg = 0
nbNeutral = 0
nbCorrectPos = 0
nbCorrectNeg = 0
nbCorrectNeutral = 0

nbPosInPos = 0
nbPosInNeg = 0
nbPosInNeutral = 0
nbNegInPos = 0
nbNegInNeg = 0
nbNegInNeutral = 0
nbNeutralInPos = 0
nbNeutralInNeg = 0
nbNeutralInNeutral = 0

error = []

for index, tweet in enumerate(usedData):
    #print index
    realSentiment = int(tweet[0])
    preProcessedTweet = preProcess(tweet[1], dicoSlang)
    sentiment = getSentimentFromTweet1(preProcessedTweet, dico, swn )
    
    if (realSentiment == 4):
        nbPos = nbPos+1
        if sentiment[2] == realSentiment:
            nbCorrectPos = nbCorrectPos+1
            nbPosInPos = nbPosInPos+1
        elif sentiment[2] == 2:
            nbPosInNeutral = nbPosInNeutral+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 0:
            nbPosInNeg = nbPosInNeg+1  
            error.append([tweet[1],realSentiment,sentiment[2]])  
    elif (realSentiment == 2):
        nbNeutral = nbNeutral+1
        if sentiment[2] == realSentiment:
            nbCorrectNeutral = nbCorrectNeutral+1
            nbNeutralInNeutral = nbNeutralInNeutral+1
        elif sentiment[2] == 4:
            nbNeutralInPos = nbNeutralInPos+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 0:
            nbNeutralInNeg = nbNeutralInNeg+1
            error.append([tweet[1],realSentiment,sentiment[2]])
    else:
        nbNeg = nbNeg+1
        if sentiment[2] == realSentiment:
            nbCorrectNeg = nbCorrectNeg+1
            nbNegInNeg = nbNegInNeg+1
        elif sentiment[2] == 4:
            nbNegInPos = nbNegInPos+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 2:
            nbNegInNeutral = nbNegInNeutral+1
            error.append([tweet[1],realSentiment,sentiment[2]])
            
print('algo1')
print('%d correct detection of positive sentiment out of %d positive tweets' % (nbCorrectPos, nbPos))
print('%d correct detection of neutral sentiment out of %d neutral tweets' % (nbCorrectNeutral, nbNeutral))
print('%d correct detection of negative sentiment out of %d negative tweets' % (nbCorrectNeg, nbNeg))

print('-- 4 - 2 - 0 -')
print('4-%d -%d -%d -' %(nbPosInPos, nbPosInNeutral, nbPosInNeg))
print('2-%d -%d -%d -' %(nbNeutralInPos, nbNeutralInNeutral, nbNeutralInNeg))
print('0-%d -%d -%d -' %(nbNegInPos, nbNegInNeutral, nbNegInNeg))


#Test for version 2 

nbPos = 0
nbNeg = 0
nbNeutral = 0
nbCorrectPos = 0
nbCorrectNeg = 0
nbCorrectNeutral = 0

nbPosInPos = 0
nbPosInNeg = 0
nbPosInNeutral = 0
nbNegInPos = 0
nbNegInNeg = 0
nbNegInNeutral = 0
nbNeutralInPos = 0
nbNeutralInNeg = 0
nbNeutralInNeutral = 0

error = []

for index, tweet in enumerate(usedData):
    #print index
    realSentiment = int(tweet[0])
    preProcessedTweet = preProcess(tweet[1], dicoSlang)
    sentiment = getSentimentFromTweet2(preProcessedTweet, dico, listNeg, listBoost, swn)
    
    if (realSentiment == 4):
        nbPos = nbPos+1
        if sentiment[2] == realSentiment:
            nbCorrectPos = nbCorrectPos+1
            nbPosInPos = nbPosInPos+1
        elif sentiment[2] == 2:
            nbPosInNeutral = nbPosInNeutral+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 0:
            nbPosInNeg = nbPosInNeg+1  
            error.append([tweet[1],realSentiment,sentiment[2]])  
    elif (realSentiment == 2):
        nbNeutral = nbNeutral+1
        if sentiment[2] == realSentiment:
            nbCorrectNeutral = nbCorrectNeutral+1
            nbNeutralInNeutral = nbNeutralInNeutral+1
        elif sentiment[2] == 4:
            nbNeutralInPos = nbNeutralInPos+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 0:
            nbNeutralInNeg = nbNeutralInNeg+1
            error.append([tweet[1],realSentiment,sentiment[2]])
    else:
        nbNeg = nbNeg+1
        if sentiment[2] == realSentiment:
            nbCorrectNeg = nbCorrectNeg+1
            nbNegInNeg = nbNegInNeg+1
        elif sentiment[2] == 4:
            nbNegInPos = nbNegInPos+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 2:
            nbNegInNeutral = nbNegInNeutral+1
            error.append([tweet[1],realSentiment,sentiment[2]])
            
print('algo2')
print('%d correct detection of positive sentiment out of %d positive tweets' % (nbCorrectPos, nbPos))
print('%d correct detection of neutral sentiment out of %d neutral tweets' % (nbCorrectNeutral, nbNeutral))
print('%d correct detection of negative sentiment out of %d negative tweets' % (nbCorrectNeg, nbNeg))

print('-- 4 - 2 - 0 -')
print('4-%d -%d -%d -' %(nbPosInPos, nbPosInNeutral, nbPosInNeg))
print('2-%d -%d -%d -' %(nbNeutralInPos, nbNeutralInNeutral, nbNeutralInNeg))
print('0-%d -%d -%d -' %(nbNegInPos, nbNegInNeutral, nbNegInNeg))


#Test for version 3
nbPos = 0
nbNeg = 0
nbNeutral = 0
nbCorrectPos = 0
nbCorrectNeg = 0
nbCorrectNeutral = 0

nbPosInPos = 0
nbPosInNeg = 0
nbPosInNeutral = 0
nbNegInPos = 0
nbNegInNeg = 0
nbNegInNeutral = 0
nbNeutralInPos = 0
nbNeutralInNeg = 0
nbNeutralInNeutral = 0

error = []

for index, tweet in enumerate(usedData):
    #print index
    realSentiment = int(tweet[0])
    preProcessedTweet = preProcess(tweet[1], dicoSlang)
    sentiment = getSentimentFromTweet3(preProcessedTweet, dico, listNeg, listBoost, swn)
    
    if (realSentiment == 4):
        nbPos = nbPos+1
        if sentiment[2] == realSentiment:
            nbCorrectPos = nbCorrectPos+1
            nbPosInPos = nbPosInPos+1
        elif sentiment[2] == 2:
            nbPosInNeutral = nbPosInNeutral+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 0:
            nbPosInNeg = nbPosInNeg+1  
            error.append([tweet[1],realSentiment,sentiment[2]])  
    elif (realSentiment == 2):
        nbNeutral = nbNeutral+1
        if sentiment[2] == realSentiment:
            nbCorrectNeutral = nbCorrectNeutral+1
            nbNeutralInNeutral = nbNeutralInNeutral+1
        elif sentiment[2] == 4:
            nbNeutralInPos = nbNeutralInPos+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 0:
            nbNeutralInNeg = nbNeutralInNeg+1
            error.append([tweet[1],realSentiment,sentiment[2]])
    else:
        nbNeg = nbNeg+1
        if sentiment[2] == realSentiment:
            nbCorrectNeg = nbCorrectNeg+1
            nbNegInNeg = nbNegInNeg+1
        elif sentiment[2] == 4:
            nbNegInPos = nbNegInPos+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 2:
            nbNegInNeutral = nbNegInNeutral+1
            error.append([tweet[1],realSentiment,sentiment[2]])
            
print('algo3')
print('%d correct detection of positive sentiment out of %d positive tweets' % (nbCorrectPos, nbPos))
print('%d correct detection of neutral sentiment out of %d neutral tweets' % (nbCorrectNeutral, nbNeutral))
print('%d correct detection of negative sentiment out of %d negative tweets' % (nbCorrectNeg, nbNeg))

print('-- 4 - 2 - 0 -')
print('4-%d -%d -%d -' %(nbPosInPos, nbPosInNeutral, nbPosInNeg))
print('2-%d -%d -%d -' %(nbNeutralInPos, nbNeutralInNeutral, nbNeutralInNeg))
print('0-%d -%d -%d -' %(nbNegInPos, nbNegInNeutral, nbNegInNeg))


#Test for version 4
nbPos = 0
nbNeg = 0
nbNeutral = 0
nbCorrectPos = 0
nbCorrectNeg = 0
nbCorrectNeutral = 0

nbPosInPos = 0
nbPosInNeg = 0
nbPosInNeutral = 0
nbNegInPos = 0
nbNegInNeg = 0
nbNegInNeutral = 0
nbNeutralInPos = 0
nbNeutralInNeg = 0
nbNeutralInNeutral = 0

error = []

for index, tweet in enumerate(usedData):
    #print index
    realSentiment = int(tweet[0])
    preProcessedTweet = preProcess(tweet[1], dicoSlang)
    sentiment = getSentimentFromTweet4(preProcessedTweet, dico, listNeg, listBoost, swn)
    
    if (realSentiment == 4):
        nbPos = nbPos+1
        if sentiment[2] == realSentiment:
            nbCorrectPos = nbCorrectPos+1
            nbPosInPos = nbPosInPos+1
        elif sentiment[2] == 2:
            nbPosInNeutral = nbPosInNeutral+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 0:
            nbPosInNeg = nbPosInNeg+1  
            error.append([tweet[1],realSentiment,sentiment[2]])  
    elif (realSentiment == 2):
        nbNeutral = nbNeutral+1
        if sentiment[2] == realSentiment:
            nbCorrectNeutral = nbCorrectNeutral+1
            nbNeutralInNeutral = nbNeutralInNeutral+1
        elif sentiment[2] == 4:
            nbNeutralInPos = nbNeutralInPos+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 0:
            nbNeutralInNeg = nbNeutralInNeg+1
            error.append([tweet[1],realSentiment,sentiment[2]])
    else:
        nbNeg = nbNeg+1
        if sentiment[2] == realSentiment:
            nbCorrectNeg = nbCorrectNeg+1
            nbNegInNeg = nbNegInNeg+1
        elif sentiment[2] == 4:
            nbNegInPos = nbNegInPos+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 2:
            nbNegInNeutral = nbNegInNeutral+1
            error.append([tweet[1],realSentiment,sentiment[2]])
            
print('algo4')
print('%d correct detection of positive sentiment out of %d positive tweets' % (nbCorrectPos, nbPos))
print('%d correct detection of neutral sentiment out of %d neutral tweets' % (nbCorrectNeutral, nbNeutral))
print('%d correct detection of negative sentiment out of %d negative tweets' % (nbCorrectNeg, nbNeg))

print('-- 4 - 2 - 0 -')
print('4-%d -%d -%d -' %(nbPosInPos, nbPosInNeutral, nbPosInNeg))
print('2-%d -%d -%d -' %(nbNeutralInPos, nbNeutralInNeutral, nbNeutralInNeg))
print('0-%d -%d -%d -' %(nbNegInPos, nbNegInNeutral, nbNegInNeg))


#Test for version 5

nbPos = 0
nbNeg = 0
nbNeutral = 0
nbCorrectPos = 0
nbCorrectNeg = 0
nbCorrectNeutral = 0

nbPosInPos = 0
nbPosInNeg = 0
nbPosInNeutral = 0
nbNegInPos = 0
nbNegInNeg = 0
nbNegInNeutral = 0
nbNeutralInPos = 0
nbNeutralInNeg = 0
nbNeutralInNeutral = 0

error = []

for index, tweet in enumerate(usedData):
    #print index
    realSentiment = int(tweet[0])
    preProcessedTweet = preProcess(tweet[1], dicoSlang)
    sentiment = getSentimentFromTweet5(preProcessedTweet, dico, listNeg, listBoost, swn)
    
    if (realSentiment == 4):
        nbPos = nbPos+1
        if sentiment[2] == realSentiment:
            nbCorrectPos = nbCorrectPos+1
            nbPosInPos = nbPosInPos+1
        elif sentiment[2] == 2:
            nbPosInNeutral = nbPosInNeutral+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 0:
            nbPosInNeg = nbPosInNeg+1  
            error.append([tweet[1],realSentiment,sentiment[2]])  
    elif (realSentiment == 2):
        nbNeutral = nbNeutral+1
        if sentiment[2] == realSentiment:
            nbCorrectNeutral = nbCorrectNeutral+1
            nbNeutralInNeutral = nbNeutralInNeutral+1
        elif sentiment[2] == 4:
            nbNeutralInPos = nbNeutralInPos+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 0:
            nbNeutralInNeg = nbNeutralInNeg+1
            error.append([tweet[1],realSentiment,sentiment[2]])
    else:
        nbNeg = nbNeg+1
        if sentiment[2] == realSentiment:
            nbCorrectNeg = nbCorrectNeg+1
            nbNegInNeg = nbNegInNeg+1
        elif sentiment[2] == 4:
            nbNegInPos = nbNegInPos+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 2:
            nbNegInNeutral = nbNegInNeutral+1
            error.append([tweet[1],realSentiment,sentiment[2]])
            
print('algo5')
print('%d correct detection of positive sentiment out of %d positive tweets' % (nbCorrectPos, nbPos))
print('%d correct detection of neutral sentiment out of %d neutral tweets' % (nbCorrectNeutral, nbNeutral))
print('%d correct detection of negative sentiment out of %d negative tweets' % (nbCorrectNeg, nbNeg))

print('-- 4 - 2 - 0 -')
print('4-%d -%d -%d -' %(nbPosInPos, nbPosInNeutral, nbPosInNeg))
print('2-%d -%d -%d -' %(nbNeutralInPos, nbNeutralInNeutral, nbNeutralInNeg))
print('0-%d -%d -%d -' %(nbNegInPos, nbNegInNeutral, nbNegInNeg))


#Test for version 6

nbPos = 0
nbNeg = 0
nbNeutral = 0
nbCorrectPos = 0
nbCorrectNeg = 0
nbCorrectNeutral = 0

nbPosInPos = 0
nbPosInNeg = 0
nbPosInNeutral = 0
nbNegInPos = 0
nbNegInNeg = 0
nbNegInNeutral = 0
nbNeutralInPos = 0
nbNeutralInNeg = 0
nbNeutralInNeutral = 0

error = []

for index, tweet in enumerate(usedData):
    #print index
    realSentiment = int(tweet[0])
    preProcessedTweet = preProcess(tweet[1], dicoSlang)
    sentiment = getSentimentFromTweet6(preProcessedTweet, dico, listNeg, listBoost, listPosEmoticons, listNegEmoticons, swn)
    
    if (realSentiment == 4):
        nbPos = nbPos+1
        if sentiment[2] == realSentiment:
            nbCorrectPos = nbCorrectPos+1
            nbPosInPos = nbPosInPos+1
        elif sentiment[2] == 2:
            nbPosInNeutral = nbPosInNeutral+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 0:
            nbPosInNeg = nbPosInNeg+1  
            error.append([tweet[1],realSentiment,sentiment[2]])  
    elif (realSentiment == 2):
        nbNeutral = nbNeutral+1
        if sentiment[2] == realSentiment:
            nbCorrectNeutral = nbCorrectNeutral+1
            nbNeutralInNeutral = nbNeutralInNeutral+1
        elif sentiment[2] == 4:
            nbNeutralInPos = nbNeutralInPos+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 0:
            nbNeutralInNeg = nbNeutralInNeg+1
            error.append([tweet[1],realSentiment,sentiment[2]])
    else:
        nbNeg = nbNeg+1
        if sentiment[2] == realSentiment:
            nbCorrectNeg = nbCorrectNeg+1
            nbNegInNeg = nbNegInNeg+1
        elif sentiment[2] == 4:
            nbNegInPos = nbNegInPos+1
            error.append([tweet[1],realSentiment,sentiment[2]])
        elif sentiment[2] == 2:
            nbNegInNeutral = nbNegInNeutral+1
            error.append([tweet[1],realSentiment,sentiment[2]])
            
print('algo6')
print('%d correct detection of positive sentiment out of %d positive tweets' % (nbCorrectPos, nbPos))
print('%d correct detection of neutral sentiment out of %d neutral tweets' % (nbCorrectNeutral, nbNeutral))
print('%d correct detection of negative sentiment out of %d negative tweets' % (nbCorrectNeg, nbNeg))

print('-- 4 - 2 - 0 -')
print('4-%d -%d -%d -' %(nbPosInPos, nbPosInNeutral, nbPosInNeg))
print('2-%d -%d -%d -' %(nbNeutralInPos, nbNeutralInNeutral, nbNeutralInNeg))
print('0-%d -%d -%d -' %(nbNegInPos, nbNegInNeutral, nbNegInNeg))
