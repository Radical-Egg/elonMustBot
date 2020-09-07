import os
import sys
import json
import tweepy
from os import environ
import requests
import random


class Elon:
    def __init__(self):
        self.rapidAPI = environ['ElonBot_RAPID_API_KEY']
        self.deepAPI = environ['ElonBot_DEEPAI_API_KEY']

    # getting random verb and prep
    def getVerb(self):

        # file paths and other variables
        verb_fp = "/mnt/nfs/home/pi/share/git/elonMustBot/data/verbs.json"
        preposition_fp = "/mnt/nfs/home/pi/share/git/elonMustBot/data/prepositions.json"
        size = 0
        t = 0
        q = 0

        # opening verb json, reading it and getting a random one from the list
        with open(verb_fp, 'r') as f:
            data = json.load(f) # load json
            size = len(data['verbs']) # get length of list
            randomAssignment = random.randrange(size) # get random int

            for verb in data['verbs']: # loop through until we get to the random point then make assignments
                t += 1
                if t == randomAssignment:
                    randomVerb = verb['present']

            f.close()
        
        # same process for preps and nouns, will turn this into one function in the future
        with open(preposition_fp, 'r') as f:
            data = json.load(f)
            size = len(data['prepositions'])
            randomAssignment = random.randrange(size)

            for prep in data['prepositions']:
                q += 1
                if q == randomAssignment:
                    randomPrep = prep
            f.close()

        verb_phrase = randomVerb + " " + randomPrep

        return verb_phrase
    def getNoun(self):
        nouns_fp = "/mnt/nfs/home/pi/share/git/elonMustBot/data/nouns.json"
        size = 0
        t = 0

        with open(nouns_fp, 'r') as f:
            data = json.load(f)
            size = len(data['nouns'])
            randomAssignment = random.randrange(size)

            for noun in data['nouns']:
                t += 1
                if t == randomAssignment:
                    randomNoun = noun
                
            f.close()

        return randomNoun
    def getTense(self):
        tense = ['past', 'present', 'future']
        size = len(tense)

        return tense[random.randrange(size)]

    def getElonSentence(self):
        url = "https://linguatools-sentence-generating.p.rapidapi.com/realise"

        querystring = {
            "object":self.getNoun(),
            "subject":"Elon Must",
            "verb": self.getVerb(), 
            "subjdet": "-", 
            "objdet": "-",
            "tense": self.getTense()
        }

        headers = {
            'x-rapidapi-host': "linguatools-sentence-generating.p.rapidapi.com",
            'x-rapidapi-key': self.rapidAPI
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        randomSentence = response.json()['sentence']

        return randomSentence

    def getElonParagraph(self):
        r = requests.post(
        "https://api.deepai.org/api/text-generator",
        data={
            'text': self.getElonSentence(),
        },
        headers={'api-key': self.deepAPI})
        
        print(r.json()['output'])

class tweet:
        def connect(self):
            ## getting keys from environment variables
            CONSUMER = environ['ElonBot_CONSUMER']
            CONSUMER_SECRET = environ['ElonBot_CONSUMER_SECRET']

            ACCESS_TOKEN = environ['ElonBot_ACCESS']
            ACCESS_TOKEN_SECRET = environ['ElonBot_ACCESS_SECRET']

            # Teepy API Auths
            self.auth = tweepy.OAuthHandler(CONSUMER, CONSUMER_SECRET)
            self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

            self.api = tweepy.API(self.auth)

            # making sure i can connect
            try:
                self.api.verify_credentials()
                print("Auth OK")
            except:
                print("Something went wrong")
        def tweetTextConent(self, sentence):
            self.api.update_status(sentence)
            print("Successfully tweeted {}".format(sentence))
        def __init__(self):
            self.api = None
            self.auth = None

            self.connect()

if __name__ == "__main__":
    elon = Elon()
    test = elon.getElonSentence()
    tweeting = tweet()
    tweeting.tweetTextConent(test)



            
