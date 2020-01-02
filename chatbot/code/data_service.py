import numpy as np
import random
import pickle
import chatbot.code.constants as const
import chatbot.code.helpers as helpers
import copy


def process_intent_data(intents_path):
    intents = helpers.read_json_from_file(intents_path)
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

    # remove duplicates
    all_words = sorted(list(set(all_words)))

    return tokenized_requests, all_words


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
        bag = helpers.create_bag_of_words(request[0], all_words)
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


def save_training_data(all_words, train_x, train_y):
    pickle.dump({'all_words': all_words, 'train_x': train_x, 'train_y': train_y},
                open("data/training_data", "wb"))


def load_training_data(path):
    # restore all of our data structures
    data = pickle.load(open(path, "rb"))
    all_words = data['all_words']
    train_x = data['train_x']
    train_y = data['train_y']
    return all_words, train_x, train_y


# TODO: remove invalid data(reuse functions from dataset formatter)
def get_test_data(original_test_data_path, intent_names: list):
    with open(original_test_data_path, 'r') as tsv_file:
        lines = tsv_file.readlines()

    result = []
    num_of_columns = len(lines[0].split('\t'))
    # intent \t slots \t request \t lang \t tokens
    for line in lines:
        parsed_line = line.split('\t')
        if len(parsed_line) != num_of_columns:
            raise Exception('invalid number of columns')

        intent_name = parsed_line[0]
        if intent_name in intent_names:
            request = parsed_line[2].lower()
            result.append((intent_name, request))

    return result
