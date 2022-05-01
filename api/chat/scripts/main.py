# Imports
# Library to get a past streams chat logs
from chat_downloader import ChatDownloader

# Sentiment analysis library
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

# Data Analysis
import matplotlib.pyplot as plt
import pandas as pd
import json
import re

# Making Requests
import requests

# Model Import
from ..models import Stats

# Retreive the chat logs of the video
def getChatLogs(url):
    # Download chat logs
    chat = ChatDownloader().get_chat(url)

    # Insert data into dataframe
    data = []
    for obj in chat:
        data.append(
            [
                obj['message'],
                obj['author']['name']
            ]
        )

    # return dataframe from array
    return pd.DataFrame(data)

# Step 1: Clean text
def clean(text):
    # Removes all special characters and numericals leaving the alphabets
    text = re.sub('[^A-Za-z]+', ' ', text) 
    return text

pos_dict = {'J':wordnet.ADJ, 'V':wordnet.VERB, 'N':wordnet.NOUN, 'R':wordnet.ADV}

# Step 2: Word Tokenization, Filter Stop Words and Parts-of-Speech Tagging
def token_stop_pos(text):
    tags = pos_tag(word_tokenize(text))
    newlist = []
    for word, tag in tags:
        if word.lower() not in set(stopwords.words('english')):
            newlist.append(tuple([word, pos_dict.get(tag[0])]))
    return newlist

# Step 3: Lemmatization
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

def main(url):
    # Get the chat logs
    df = getChatLogs(url)

    # VOD ID - parse from end of string, or question mark to last slash

    if "youtube" in url:
        #  split after =
        VOD_ID = url.split('=')[1]
    elif "?" not in url:    
        # Twitch
        VOD_ID = url.rsplit('/', 1)[1]
    else:
        # match regex expression
        VOD_ID = re.search(".*\/(.*)\?", url).group(1)


    # Get VOD streamer name and Thumbnail
    if "twitch" in url:
        # Twitch
        # Get access token
        clientId = "4sgiryddrqj4d1vtqxcjf42nxf6azu"
        clientSecret = "d1hvhpnlwvj1ftzddv4mtwmzoscdd7"

        url = f"https://id.twitch.tv/oauth2/token?client_id={clientId}&client_secret={clientSecret}&grant_type=client_credentials"

        response = requests.post(url)

        accessToken = response.json()['access_token']

        # Get streamer name and thumbnail
        url = f"https://api.twitch.tv/helix/videos?id={VOD_ID}"
        headers = {
            'Authorization': f'Bearer {accessToken}',
            'Client-Id': clientId
        }

        response = requests.request("GET", url, headers=headers).json()

        streamerName = response['data'][0]['user_name']
        streamerThumbnail = response['data'][0]['thumbnail_url']
        
        if streamerThumbnail == "":
            streamerThumbnail = "https://static-cdn.jtvnw.net/ttv-static/404_preview-1920x1080.jpg"
        
        
    elif "youtube" in url:
        streamerThumbnail = f"https://img.youtube.com/vi/{VOD_ID}/maxresdefault.jpg"

        # get streamer name
        url = f"https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v={VOD_ID}"
        response = requests.get(url).json()
        streamerName = response['author_name']


    elif "reddit" in url:
        # Reddit
        # Get streamer name and thumbnail
        url = f"https://strapi.reddit.com/videos/{VOD_ID}"

        request = requests.get(url).json()

        streamerName = request['data']['post']['authorInfo']['name']
        streamerThumbnail = request['data']['stream']['thumbnail']


    # Apply Sentiment Analysis to the chat logs

    # Clean the chat logs
    df["cleaned"] = df[0].apply(clean)

    # Word Tokenization, Filter Stop Words and Parts-of-Speech Tagging
    df["POS tagged"] = df[0].apply(token_stop_pos)

    # Lemmatization
    df['Lemma'] = df['POS tagged'].apply(lemmatize)

    fin_data = pd.DataFrame(df[[1, 0, 'Lemma']])
    fin_data['Polarity'] = fin_data['Lemma'].apply(getPolarity) 
    fin_data['Analysis'] = fin_data['Polarity'].apply(analysis)

    # remove all rows with where row[1] is "nightbot"
    fin_data = fin_data[fin_data[1] != "nightbot"]

    # Get number of Posotive, Negative and Neutral comments
    tb_counts = fin_data.Analysis.value_counts()

    try: numPositiveComments = tb_counts['Positive']
    except: numPositiveComments = 0

    try: numNegativeComments = tb_counts['Negative']
    except: numNegativeComments = 0
    
    try: numNeutralComments = tb_counts['Neutral']
    except: numNeutralComments = 0
    
    # Get most common word that does not belong to a certain user
    
    mostCommonWord = fin_data['Lemma'].value_counts().idxmax()

    
    # Average polarity of the comments
    tb_polarity = fin_data.groupby(['Analysis'])['Polarity'].mean()

    # calcualte each users total polairty score
    scores = {}

    # iterate thorugh df
    for index, row in fin_data.iterrows():
        # if the user name is not in the dict, add it with the polarity score
        if row[1] not in scores:
            scores[row[1]] = row['Polarity']
        
        else:
            # if the user name is in the dict, add the polarity score to the existing value
            scores[row[1]] += row['Polarity']

    # sort the dict by polarity score
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Get the user with the highest polarity score - most positive user 
    mostPositiveUser = sorted_scores[0]

    # Get the user with the lowest polarity score - most negative user
    mostNegativeUser = sorted_scores[-1]

    # create new objet for this VOD
    # print(VOD_ID, streamerName, streamerThumbnail, numPositiveComments, numNegativeComments, numNeutralComments, mostCommonWord, mostPositiveUser, mostNegativeUser, sep='\n')
    
    Stats.objects.get_or_create(
        VOD=VOD_ID, 
        streamerName=streamerName, 
        positiveComments=numPositiveComments, 
        negativeComments=numNegativeComments,
        neutralComments=numNeutralComments, 
        streamerThumbnail=streamerThumbnail,
        mostCommonWord=mostCommonWord, 
        mostPositiveUser=mostPositiveUser, 
        mostNegativeUser=mostNegativeUser
    )    

    return VOD_ID


# Initialize NLP libraries for Sentiment Analysis 
wordnet_lemmatizer = WordNetLemmatizer()
# nltk.download('all')
