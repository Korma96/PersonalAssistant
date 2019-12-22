import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import random
import pickle
import json as j
import chatbot.code.constants as const


def read_intent_configuration(path):
    with open(path) as json_data:
        intent_config = j.load(json_data)
    return intent_config


def process_intent_data(intents_path):
    with open(intents_path) as json_data:
        intents = j.load(json_data)

    all_words = []
    tokenized_requests = []
    ignore_words = ['?']

    # loop through each request in intents
    for intent_name in intents.keys():
        for request in intents[intent_name][const.REQUESTS]:

            # tokenize each word in the sentence
            w = nltk.word_tokenize(request)

            # add to our words list
            all_words.extend(w)

            tokenized_requests.append((w, intent_name))

    for intent_name in intents.keys():
        # remove unnecessary objects from memory
        del intents[intent_name][const.REQUESTS]

    # only slots remain in dict
    slots = intents

    stemmer = LancasterStemmer()
    # stem and lower each word and remove duplicates
    all_words = [stemmer.stem(w.lower()) for w in all_words if w not in ignore_words]
    all_words = sorted(list(set(all_words)))

    return tokenized_requests, all_words, slots


def create_training_data(tokenized_requests, intent_names, all_words):
    stemmer = LancasterStemmer()
    # create our training data
    training = []
    # create an empty array for our output
    output_empty = [0] * len(intent_names)

    print('Data processing started')
    documents_num = float(len(tokenized_requests))
    counter = 0.0
    # training set, bag of words for each sentence
    for doc in tokenized_requests:
        # initialize our bag of words
        bag = []
        # list of tokenized words for the pattern
        pattern_words = doc[0]
        # stem each word. to do: this can be done in earlier step
        pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
        # create our bag of words array
        for w in all_words:
            bag.append(1) if w in pattern_words else bag.append(0)

        # output is a '0' for each intent and '1' for current intent
        output_row = list(output_empty)
        output_row[intent_names.index(doc[1])] = 1

        training.append([bag, output_row])

        counter += 1
        if counter % 100 == 0:
            print("{0:.2f}".format(counter / documents_num * 100) + '%')

    print('Data processing finished')

    # shuffle our features and turn into np.array
    random.shuffle(training)
    training = np.array(training)

    # create train lists
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    return train_x, train_y


def save_training_data(all_words, slots, train_x, train_y):
    pickle.dump({'all_words': all_words, 'slots': slots, 'train_x': train_x, 'train_y': train_y},
                open("data/training_data", "wb"))


def load_training_data():
    # restore all of our data structures
    data = pickle.load(open("training_data", "rb"))
    all_words = data['all_words']
    slots = data['slots']
    train_x = data['train_x']
    train_y = data['train_y']
    return all_words, slots, train_x, train_y
