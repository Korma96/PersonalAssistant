import numpy as np
import random
import pickle
import json as j
import chatbot.code.constants as const
import chatbot.code.helpers as helpers
import copy


def read_intent_configuration(path):
    with open(path) as json_data:
        intent_config = j.load(json_data)
    return intent_config


def process_intent_data(intents_path):
    with open(intents_path) as json_data:
        intents = j.load(json_data)

    all_words = []
    tokenized_requests = []

    print('Intent data processing started')
    intents_sum = float(len(list(intents.keys())))
    counter = 0.0

    # loop through each request in intents
    for intent_name in intents.keys():
        for request in intents[intent_name][const.REQUESTS]:
            words = helpers.parse_request(request)
            # add to our words list
            all_words.extend(words)
            tokenized_requests.append((words, intent_name))

        counter += 1
        print("{0:.2f}".format(counter / intents_sum * 100) + '%')

    print('Intent data processing finished')

    # remove unnecessary objects from memory
    for intent_name in intents.keys():
        del intents[intent_name][const.REQUESTS]

    # only slots remain in dict
    slots = intents

    # remove duplicates
    all_words = sorted(list(set(all_words)))

    return tokenized_requests, all_words, slots


def create_training_data(tokenized_requests, intent_names, all_words):
    # create our training data
    training = []
    # create an empty array for our output
    output_empty = list([0] * len(intent_names))
    # output is '0' for each intent and '1' for current intent
    output_rows = {}
    for i in range(len(intent_names)):
        output_empty_copy = copy.deepcopy(output_empty)
        output_empty_copy[i] = 1
        output_rows[intent_names[i]] = output_empty_copy

    print('Training data processing started')
    requests_sum = float(len(tokenized_requests))
    counter = 0.0

    # training set, bag of words for each sentence
    for request in tokenized_requests:
        # initialize our bag of words
        bag = []
        # list of tokenized words
        request_words = request[0]
        # create our bag of words array
        for word in all_words:
            if word in request_words:
                bag.append(1)
            else:
                bag.append(0)

        output_row = output_rows[request[1]]
        training.append([bag, output_row])

        counter += 1
        if counter % 100 == 0:
            print("{0:.2f}".format(counter / requests_sum * 100) + '%')

    print('Training data processing finished')

    # shuffle our features and turn into np.array
    random.shuffle(training)
    training = np.array(training)

    # create train lists
    train_x = list(training[:, 0])  # for each element(tuple) take first item
    train_y = list(training[:, 1])  # for each element(tuple) take second item

    return train_x, train_y


def save_training_data(all_words, slots, train_x, train_y):
    pickle.dump({'all_words': all_words, 'slots': slots, 'train_x': train_x, 'train_y': train_y},
                open("data/training_data", "wb"))


def load_training_data(path):
    # restore all of our data structures
    data = pickle.load(open(path, "rb"))
    all_words = data['all_words']
    slots = data['slots']
    train_x = data['train_x']
    train_y = data['train_y']
    return all_words, slots, train_x, train_y
