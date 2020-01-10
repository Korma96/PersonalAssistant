from nltk.stem.lancaster import LancasterStemmer
import nltk
import chatbot.code.settings as s
import numpy as np
import json
import chatbot.code.constants as const
import re


stemmer = LancasterStemmer()


# tokenize + stem
def tokenize_request(request: str):
    # tokenize request
    words = nltk.word_tokenize(request)
    # stem each word
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


def get_json_string(objects: any):
    return json.dumps(objects, indent=True)


def read_json_from_file(path):
    with open(path) as json_data:
        json_object = json.load(json_data)
    return json_object


# TODO: log invalid slots
def is_slot_value_valid(slot_value: str, intent_config: dict, current_intent_name: str = ''):
    if (const.ALARM in current_intent_name and
            len(slot_value) < 10 and
            const.REMINDER in slot_value):
        return False
    if (const.REMINDER in current_intent_name and
            len(slot_value) < 10 and
            const.ALARM in slot_value):
        return False

    for intent_name in intent_config.keys():
        if slot_value in intent_name:
            return False
        for slot_name in intent_config[intent_name][const.ALL_SLOTS]:
            if slot_value in slot_name:
                return False

    return True


# TODO: log invalid requests
def is_request_valid(request: str, intent_name: str):
    if const.ALARM in intent_name and const.REMINDER in request:
        return False
    if const.REMINDER in intent_name and const.ALARM in request:
        return False
    return True


def already_exists_in_list(value: str, all_values: list, index: int):
    for val in all_values:
        if val[index] == value:
            return True
    return False


def normalize_string(string: str):
    # 1) lowercase
    string = string.lower()
    # 2) replace numbers
    string = re.sub('[0-9]', const.NUMERIC, string)
    # 3) remove unnecessary whitespaces
    return ' '.join(string.split())


def contains_letters(string: str):
    return any(char.isalpha() for char in string)


def replace_slots_in_request(request: str, all_slots) -> str:
    # slot = (intent_name, slot_name, slot_value)
    for slot in all_slots:
        if request_contains_slot(request, slot[2]):
            request = request.replace(slot[2], slot[1])

    return request


def request_contains_slot(request, slot):
    if 'tomorrow' in request and 'tomorrow' == slot:
        print('')
    if slot not in request:
        return False
    before, value, after = request.partition(slot)
    if value == '' or last_char_or_empty(before).isalpha() or last_char_or_empty(after).isalpha():
        return False
    return True


def last_char_or_empty(string: str):
    if string:
        return string[-1]
    return ''


def replace_slots_in_request_and_get_slots(request: str, all_slots):
    replaced_slots = {}
    # slot = (intent_name, slot_name, slot_value)
    for slot in all_slots:
        slot_name = slot[1]
        slot_value = slot[2]
        if request_contains_slot(request, slot_value):
            if slot_name not in replaced_slots:
                replaced_slots[slot_name] = []
            replaced_slots[slot_name].append(slot_value)
            request = request.replace(slot_value, slot_name)

    return request, replaced_slots


def get_percent(part, whole) -> float:
    return round(float(part) / whole, 4)
