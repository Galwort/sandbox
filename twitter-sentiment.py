from dotenv import load_dotenv
from os import getenv
from tweepy import OAuthHandler, API, Cursor, errors
from time import sleep, strftime, gmtime
from requests import post
from pandas import DataFrame

import matplotlib.pyplot as plt

load_dotenv()
consumer_key = getenv('TWT_KEY')
consumer_secret = getenv('TWT_SECRET')
access_token = getenv('TWT_TOKEN')
access_token_secret = getenv('TWT_TOKEN_SECRET')
hf_token = getenv('HF_TOKEN')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

i = 0
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except errors.TooManyRequests:
            print('we did ' + str(i) + ' tweety tweets')
            print(strftime("%H:%M:%S", gmtime()))
            print('i go sleep now')
            sleep(61 * 15)
            print(strftime("%H:%M:%S", gmtime()), 'i wake up now')
        except StopIteration:
            break

search = limit_handled(Cursor(api.search_tweets, q='twitter', lang='en').items(10000))
tweets = []
for tweet in search:
    i += 1
    tweets.append(tweet.text)

model = "cardiffnlp/twitter-roberta-base-sentiment-latest"
API_URL = "https://api-inference.huggingface.co/models/" + model
headers = {"Authorization": "Bearer %s" % (hf_token)}

def analysis(data):
    payload = dict(inputs=data, options=dict(wait_for_model=True))
    response = post(API_URL, headers=headers, json=payload)
    return response.json()

tweets_analysis = []
for tweet in tweets:
    try:
        sentiment_result = analysis(tweet)[0]
        top_sentiment = max(sentiment_result, key=lambda x: x['score']) # Get the sentiment with the higher score
        tweets_analysis.append({'tweet': tweet, 'sentiment': top_sentiment['label']})
 
    except Exception as e:
        print(e)

df = DataFrame(tweets_analysis)
sentiment_counts = df.groupby(['sentiment']).size()

fig = plt.figure(figsize=(6,6), dpi=100)
ax = plt.subplot(111)
sentiment_counts.plot.pie(ax=ax, autopct='%1.1f%%', startangle=270, fontsize=12, label="")
plt.show()