import numpy as np
import random
import pickle
import chatbot.code.helpers as helpers
import copy
from chatbot.code.percent_tracker import PercentTracker
import chatbot.code.settings as settings


def process_requests(requests_path):
    requests = helpers.read_json_from_file(requests_path)
    all_words = []
    tokenized_requests = []

    print('Request data processing started')
    percent_tracker = PercentTracker(len(requests))
    # loop through each request in intents
    for request_tuple in requests:
        request = request_tuple[1]
        words = helpers.tokenize_request(request)
        # add to our words list
        all_words.extend(words)
        tokenized_requests.append((request_tuple[0], words))
        percent_tracker.do_iteration()
    print('Request data processing finished')

    # remove duplicates
    all_words = list(set(all_words))
    all_words.sort(key=len)

    return tokenized_requests, all_words


def create_training_data(tokenized_requests, intent_names, all_words):
    training = []
    output_rows = _get_output_rows(intent_names)

    print('Training data processing started')
    percent_tracker = PercentTracker(len(tokenized_requests))
    # training set, bag of words for each sentence
    for request in tokenized_requests:
        bag = helpers.create_bag_of_words(request[1], all_words)
        output_row = output_rows[request[0]]
        training.append([bag, output_row])
        percent_tracker.do_iteration()
    print('Training data processing finished')

    # shuffle our features and turn into np.array
    random.shuffle(training)
    training = np.array(training)

    # create train lists
    train_x = list(training[:, 0])  # for each element(tuple) take first item
    train_y = list(training[:, 1])  # for each element(tuple) take second item

    return train_x, train_y


def _get_output_rows(intent_names):
    output_rows = {}
    # create an empty array for our output
    output_empty = list([0] * len(intent_names))
    for i in range(len(intent_names)):
        output_empty_copy = copy.deepcopy(output_empty)
        # output is '0' for each intent and '1' for current intent
        output_empty_copy[i] = 1
        output_rows[intent_names[i]] = output_empty_copy
    return output_rows


def save_training_data(path, all_words: list, train_x, train_y):
    helpers.write_json_to_file(all_words, settings.all_words_path)
    pickle.dump({'all_words': all_words, 'train_x': train_x, 'train_y': train_y},
                open(path, 'wb'))


def load_training_data(path):
    data = pickle.load(open(path, 'rb'))
    all_words = data['all_words']
    train_x = data['train_x']
    train_y = data['train_y']
    return all_words, train_x, train_y

