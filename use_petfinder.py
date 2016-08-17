import os
import requests

consumer_token = os.environ["API_KEY"]
consumer_secret = os.environ["API_SECRET"]
# access_token = os.environ["TWITTER_ACCESS_TOKEN"]
# access_secret = os.environ["TWITTER_ACCESS_SECRET"]

print "Your consumer token is %s" % consumer_token


r = requests.get(
    "http://api.petfinder.com/auth.getToken?key=d109d9d9e8539d67687bcfacaca8da3a&sig=e8e2c5d5f6098157e866304a257268c6")

print r


