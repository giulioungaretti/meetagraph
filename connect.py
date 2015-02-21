import tweepy


def connect():
    consumer_key = "QomNnhW10Ua5u0r5m7BpuG2lm"
    consumer_secret = "TptWkzflOsQ8lJNxL3m4qwfKCVSGigg9bncbgC1aZ9tNJrQnFR"
    access_token = "424935828-JPuALO7QAcFv2VEO42hNfkYDVTd5AGO2PFknrAi9"
    access_token_secret = "UIUpNogJceEHkID09EhwImOUNtkNWiH9z6SKydI8DVlZ8"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api
