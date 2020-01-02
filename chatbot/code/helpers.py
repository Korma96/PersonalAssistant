from nltk.stem.lancaster import LancasterStemmer
import nltk
import chatbot.code.settings as s
import numpy as np
import json


stemmer = LancasterStemmer()


# lower + tokenize + stem
def parse_request(request: str):
    # make sure every character is lowercase
    request = request.lower()
    # tokenize each word in the sentence
    words = nltk.word_tokenize(request)
    # stem and lower each word
    return [stemmer.stem(word) for word in words if word not in s.ignore_words]


# return bag of words array: 0 or 1 for each word in the bag that exists in the request
def create_bag_of_words(request_words: list, all_words: list):
    # bag of words
    bag = [0] * len(all_words)
    for request_word in request_words:
        for index, word in enumerate(all_words):
            if word == request_word:
                bag[index] = 1
    # TODO: what if word is not found in all words ?
    return np.array(bag)


def write_json_to_file(objects: any, output_path: str):
    json_str = json.dumps(objects, indent=False)
    with open(output_path, 'w+') as json_file:
        json_file.write(json_str)


def read_json_from_file(path):
    with open(path) as json_data:
        json_object = json.load(json_data)
    return json_object
