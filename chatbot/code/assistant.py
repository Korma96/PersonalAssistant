import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import random
import chatbot.code.constants as const


class Assistant:

    ERROR_THRESHOLD = 0.25

    def __init__(self, model, intent_config, all_words, slots):
        # create a data structure to hold user context
        self.context = {}
        self.stemmer = LancasterStemmer()
        self.model = model
        self.intent_config = intent_config
        self.intent_names = list(intent_config.keys())
        self.words = all_words
        self.slots = slots

    def classify(self, sentence):
        # generate probabilities from the model
        results = self.model.predict([self.bow(sentence, self.words)])[0]
        # filter out predictions below a threshold
        results = [[i, r] for i, r in enumerate(results) if r > self.ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for result in results:
            return_list.append((self.intent_names[result[0]], result[1]))
        # return tuple of intent and probability
        return return_list

    def response(self, sentence, userID='123', show_details=False):
        results = self.classify(sentence)
        # if we have a classification then find the matching intent tag
        if results:
            # loop as long as there are matches to process
            for result in results:
                for i in self.slots['intents']:
                    # find a tag matching the first result
                    if i['tag'] == result[0]:
                        '''
                        # set context for this intent if necessary
                        if 'context_set' in i:
                            if show_details:
                                print('context:', i['context_set'])
                            self.context[userID] = i['context_set']

                        # check if this intent is contextual and applies to this user's conversation
                        if 'context_filter' not in i or \
                                (userID in self.context and 'context_filter' in i and
                                 i['context_filter'] == self.context[userID]):
                            if show_details:
                                print('tag:', i['tag'])
                            # a random response from the intent
                        '''
                        return random.choice(i['responses'])

    def clean_up_sentence(self, sentence):
        # tokenize the pattern
        sentence_words = nltk.word_tokenize(sentence)
        # stem each word
        sentence_words = [self.stemmer.stem(word.lower()) for word in sentence_words]
        return sentence_words

    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
    def bow(self, sentence, words, show_details=False):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words
        bag = [0]*len(words)
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)

        return np.array(bag)
