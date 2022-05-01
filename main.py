from chat_downloader import ChatDownloader
import pandas as pd
import json
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
nltk.download('all')
from textblob import TextBlob
import matplotlib.pyplot as plt

url = 'https://www.twitch.tv/videos/1452495883'


def getChatLogs():
    # Download chat logs
    chat = ChatDownloader().get_chat(url)

    # Insert data into dataframe
    data = []
    for obj in chat:
        data.append(obj['message'])

    # return dataframe from array
    return pd.DataFrame(data)



def clean(text):
    # Removes all special characters and numericals leaving the alphabets
    text = re.sub('[^A-Za-z]+', ' ', text) 
    return text

pos_dict = {'J':wordnet.ADJ, 'V':wordnet.VERB, 'N':wordnet.NOUN, 'R':wordnet.ADV}

def token_stop_pos(text):
    tags = pos_tag(word_tokenize(text))
    newlist = []
    for word, tag in tags:
        if word.lower() not in set(stopwords.words('english')):
            newlist.append(tuple([word, pos_dict.get(tag[0])]))
    return newlist

def lemmatize(pos_data):
    lemma_rew = " "
    for word, pos in pos_data:
        if not pos: 
            lemma = word
            lemma_rew = lemma_rew + " " + lemma
        else:  
            lemma = wordnet_lemmatizer.lemmatize(word, pos=pos)
            lemma_rew = lemma_rew + " " + lemma
    return lemma_rew



# function to calculate subjectivity 
def getSubjectivity(chat):
    return TextBlob(chat).sentiment.subjectivity

# function to calculate polarity
def getPolarity(chat):
    return TextBlob(chat).sentiment.polarity

# function to analyze the chats
def analysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

df = getChatLogs()
df["cleaned"] = df[0].apply(clean)
df["POS tagged"] = df[0].apply(token_stop_pos)
df['Lemma'] = df['POS tagged'].apply(lemmatize)

fin_data = pd.DataFrame(df[[0, 'Lemma']])
fin_data['Polarity'] = fin_data['Lemma'].apply(getPolarity) 
fin_data['Analysis'] = fin_data['Polarity'].apply(analysis)
print(fin_data.head())
tb_counts = fin_data.Analysis.value_counts()
print(tb_counts)



tb_count= fin_data.Analysis.value_counts()
plt.figure(figsize=(10, 7))
plt.pie(tb_counts.values, labels = tb_counts.index, explode = (0, 0, 0.25), autopct='%1.1f%%', shadow=False)
plt.show()