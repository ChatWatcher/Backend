e# Import Libraries
from chat_downloader import ChatDownloader
import pandas
import json

# Twitch
url = 'https://www.twitch.tv/videos/1469302943'

# Youtube
# url = 'https://www.youtube.com/watch?v=FuZHQTvgN_U'

# Reddit
# url = ''

# Get input text - chat logs from streams
def getChatLogs():
    # Download chat logs
    chat = ChatDownloader().get_chat(url)

    # Insert data into dataframe
    data = []
    for obj in chat:
        data.append(obj['message'])

    # return dataframe from array
    return pandas.DataFrame(data)

print(getChatLogs(url))

''' Sentiment Analysis '''

# Step 1: Clearning up text
def segmentSentences(df):
    