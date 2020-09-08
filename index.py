import os
import sys
import json
import tweepy
from os import environ
import requests
import random
import re


class Elon:
    # init function with API Keys
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

        verb_phrase = randomVerb + " " + randomPrep # combining verb and prep

        return verb_phrase
    def getNoun(self):
        # file path and increment vars
        nouns_fp = "/mnt/nfs/home/pi/share/git/elonMustBot/data/nouns.json"
        size = 0
        t = 0
        # opening up the file, getting the data
        with open(nouns_fp, 'r') as f:
            data = json.load(f)
            size = len(data['nouns'])
            randomAssignment = random.randrange(size)

            for noun in data['nouns']: # looping through the nouns, getting a random one
                t += 1
                if t == randomAssignment:
                    randomNoun = noun
                
            f.close()

        return randomNoun
    def getTense(self): # getting the tense
        tense = ['past', 'present', 'future']
        size = len(tense)

        return tense[random.randrange(size)]

    def getElonSentence(self): # getting sentence from linqua tools API using the getter functions above
        url = "https://linguatools-sentence-generating.p.rapidapi.com/realise"
        # querying
        querystring = {
            "object":self.getNoun(),
            "subject":"Elon",
            "verb": self.getVerb(), 
            "subjdet": "-", 
            "objdet": "-",
            "tense": "present",
            "modal": "must"
        }
        # headers
        headers = {
            'x-rapidapi-host': "linguatools-sentence-generating.p.rapidapi.com",
            'x-rapidapi-key': self.rapidAPI
            }
        # reponse
        response = requests.request("GET", url, headers=headers, params=querystring)

        # putting the sentence into variable
        randomSentence = response.json()['sentence']

        return randomSentence

    # function for POST for paragraph
    def getElonParagraph(self):
        r = requests.post(
        "https://api.deepai.org/api/text-generator",
        data={
            'text': self.getElonSentence(), # using data from getElonSentence
        },
        headers={'api-key': self.deepAPI})

        try:
            marker = 280
            responseOutputRaw = r.json()['output'][:marker]
            addedString = ""
            separator = " "

            for word in responseOutputRaw.split(): # loop through string - trying to find punctuation to end at a good point
                addedString = separator.join((addedString, word))
                count = len(addedString)

                if re.search(r'^.+[\!\.\?]{1}$', word): 
                    marker = count
                
            return addedString[:marker]
        except:
            print(r.json())
            return r.json()

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

        # tweeting string content
        def tweetTextConent(self, sentence):
            self.api.update_status(sentence)
            print("Successfully tweeted {}".format(sentence))
        def __init__(self):
            self.api = None
            self.auth = None

            self.connect() # connecting to twitter API

if __name__ == "__main__":
    # making elon and tweet objects
    elon = Elon()
    #tweeting = tweet()
    
    # storing strings into var to make less typing in future
    elonPara = elon.getElonParagraph()
    print(elonPara)
    #elonSentence = elon.getElonSentence()

    # example of tweeting out a sentence and then a paragraph
    #tweeting.tweetTextConent(elonSentence)
    #tweeting.tweetTextConent(elonPara)


            
