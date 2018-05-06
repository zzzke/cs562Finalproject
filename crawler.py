import tweepy
from tweepy import OAuthHandler
import pymysql
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import os

def getloc(address):
    geolocator = Nominatim()
    try:
        return geolocator.geocode(address, addressdetails=True)
    except GeocoderTimedOut:
        return getloc(address)

def initTweepy():
    consumer_key = 'yRSEp8qDquaRr9Qw7l32MyzYj'
    consumer_secret = 'kX9ifhWcg94PKpQDahK5sMaIlQlw5uX8MOwnENi59yUHWqw6v0'
    access_token = '3389751963-fFUOLj5E4qfefZwmz8DpFPY7WQAT0YyE2dkZcak'
    access_secret = 'PWQFvyC8D2vRkzIj9Waw1TxQEplvjyP5hDhYI6WU5yT5H'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

def searchTweets(api, numoftweet):
    db = pymysql.connect(host = "localhost", port = 3306, user = "root", password = "", db = "tweetinfo", charset="utf8")
    cursor = db.cursor()
    for tweet in tweepy.Cursor(api.search, q='syria AND airstrike -filter:retweets', lang="en").items(10000):
        if numoftweet <= 10000:
            loc = getloc(tweet.user.location)
            if loc is not None:
                if 'country' in loc.raw['address']:
                    if loc.raw['address']['country'] == 'United States of America':
                        if 'state' in loc.raw['address']:
                            state = loc.raw['address']['state']
                            print("[", tweet.id, ",", state, ", ", tweet.text, ", ", tweet.user.name, ", ", str(tweet.created_at)[:10],"]")
                            txt = str(tweet.text).replace("\'", "\\'")
                            txt.replace('\"', '\\"')
                            name = str(tweet.user.name).replace("\'","\\'")
                            name.replace('\"', '\\"')
                            sql = "INSERT IGNORE INTO TWEET(ID, \
                                   TWEETTEXT, USER, TIME, STATE) \
                                   VALUES ('%d', '%s', '%s', '%s', '%s' )" % \
                                  (tweet.id, txt, name,
                                  str(tweet.created_at)[:10], str(state))
                            try:
                                cursor.execute(sql)
                                db.commit()
                                numoftweet += 1
                                print(numoftweet, " data inserted")
                            except pymysql.InternalError as e:
                                print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                                db.rollback()
        else:
            print("already get 10000 tweets")
            break
    cursor.close()
    db.close()
    return numoftweet

def requestandsleep(api):
    num = 0
    for i in range(50):
        num = searchTweets(api, num)
        time.sleep(900)
    print("get ",num, " tweets")

def outputcsv():
    if os.path.exists('d:/mysql/db/tweetinfo/tweet.csv'):
        print("tweet.csv already exists")
        return;
    db = pymysql.connect(host = "localhost", port = 3306, user = "root", password = "", db = "tweetinfo", charset="utf8")
    cursor = db.cursor()
    sql = "SELECT * FROM TWEET ORDER BY STATE INTO OUTFILE 'tweet.csv' FIELDS TERMINATED BY ',' OPTIONALLY \
            ENCLOSED BY '\"' LINES TERMINATED BY '\n'"
    try:
        cursor.execute(sql)
        db.commit()
    except pymysql.InternalError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))
        db.rollback()
    cursor.close()
    db.close()

def main():
    api = initTweepy()
    db = pymysql.connect(host = "localhost", port = 3306, user = "root", password = "", db = "tweetinfo", charset="utf8")
    cursor = db.cursor()
    stmt = "SHOW TABLES LIKE 'tweet'"
    cursor.execute(stmt)
    result = cursor.fetchone()
    if result:
        print("data already stored")
        cursor.close()
        db.close()
    else:
        requestandsleep(api)
        cursor.close()
        db.close()
    outputcsv()

if __name__ == "__main__":
    main()