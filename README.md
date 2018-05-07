# Data Mining on Twitter and Visualization

Twitter is a popular social network where users can share short SMS-like messages called tweets. Users share thoughts, links and pictures on Twitter, journalists comment on live events, companies promote products and engage with customers. The list of different ways to use Twitter could be really long, and with 500 millions of tweets per day, there’s a lot of data to analyze and to play with.
[alt text](result.PNG)


## Approach and method description

Accessing the Data
In order to authorise our app to access Twitter on our behalf, we need to use the OAuth interface:
import tweepy
from tweepy import OAuthHandler
consumer_key = 'YOUR-CONSUMER-KEY'
consumer_secret = 'YOUR-CONSUMER-SECRET'
access_token = 'YOUR-ACCESS-TOKEN'
access_secret = 'YOUR-ACCESS-SECRET'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

Removing stop-words
Given the nature of our data and our tokenisation, we should also be careful with all the punctuation marks and with terms like RT (used for re-tweets) and via(used to mention the original author of an article or a re-tweet), which are not in the default stop-word list.

NLP tasks using TextBlob Sentiment Analysis
The sentiment property returns a named tuple of the form Sentiment(polarity,subjectivity). The polarity score is a float within the range [-1.0, 1.0]. The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.

WordCloud and BaseMap for Viusalization
Matplotlib‘s main tool for this type of visualization is the Basemap toolkit, which is one of several Matplotlib toolkits which lives under the mpl_toolkitsnamespace. Basemap is a useful tool for Python users to have in their virtual toolbelts.
Word clouds are a very information-dense representation of the frequency of all words in a given text. Word clouds are more effective than just using bar charts displaying the counts of words for large amounts of text, as the chart would be difficult to parse if there are too many bars.

### References 


1.	Mining Twitter Data with Python (Part 1: Collecting data)  
2.	 The wordcloud library is MIT licenced, but contains DroidSansMono.ttf, a true type font by Google, that is apache licensed. The font is by no means integral, and any other font can be used by setting the font_path variable when creating a WordCloud object.
3.	 Geographic Data with Basemap
4.	TextBlob is a Python (2 and 3) library for processing textual data. It provides a consistent API for diving into common natural language processing (NLP) tasks such as part-of-speech tagging, noun phrase extraction, sentiment analysis, and more. http://textblob.readthedocs.io/en/dev/

