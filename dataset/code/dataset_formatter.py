import chatbot.code.constants as const
import chatbot.code.helpers as helpers
from chatbot.code.percent_tracker import PercentTracker
from joblib import Parallel, delayed
import multiprocessing
import re


def format(input_path, intents_output_path, requests_output_path, slots_output_path, intent_config):
    with open(input_path, 'r') as tsv_file:
        lines = tsv_file.readlines()

    all_slots = []  # (intent_name, slot_name, slot_value)
    all_requests = []  # (intent_name, request)
    num_of_columns = len(lines[0].split('\t'))

    percent_tracker = PercentTracker(len(lines), 3000)
    print('Processing slots started')
    for line in lines:
        _parse_line(line, num_of_columns, intent_config, all_slots, all_requests)
        percent_tracker.do_iteration()
    print('Processing slots finished')

    # sort slots
    all_slots.sort(key=lambda x: len(x[2]), reverse=True)
    '''
    num_cores = multiprocessing.cpu_count()
    processed_requests = Parallel(n_jobs=num_cores)(delayed(_format_request)(request_tuple, all_slots) for request_tuple in all_requests)
    '''

    percent_tracker = PercentTracker(len(all_requests), 100)
    print('Processing requests started')
    processed_requests = []
    for request_tuple in all_requests:
        request = request_tuple[1]
        request = helpers.normalize_string(request)
        request = helpers.replace_slots_in_request(request, all_slots)
        if not helpers.already_exists_in_list(request, processed_requests, 1):
            processed_requests.append((request_tuple[0], request))
        percent_tracker.do_iteration()
    print('Processing requests finished')

    processed_requests.sort(key=lambda x: len(x[1]))

    helpers.write_json_to_file(processed_requests, requests_output_path)
    helpers.write_json_to_file(all_slots, slots_output_path)

    # convert to user friendly view

    intents = {const.SLOTS: {}, const.REQUESTS: {}}

    for slot in all_slots:
        slot_name = slot[1]
        if slot_name not in intents[const.SLOTS]:
            intents[const.SLOTS][slot_name] = []
        intents[const.SLOTS][slot_name].append(slot[2])

    for request in processed_requests:
        intent_name = request[0]
        if intent_name not in intents[const.REQUESTS]:
            intents[const.REQUESTS][intent_name] = []
        intents[const.REQUESTS][intent_name].append(request[1])

    # sort slots
    for slot_name in intents[const.SLOTS]:
        intents[const.SLOTS][slot_name].sort(key=len)

    # sort requests
    for intent_name in intents[const.REQUESTS]:
        intents[const.REQUESTS][intent_name].sort(key=len)

    helpers.write_json_to_file(intents, intents_output_path)


def _format_request(request_tuple, all_slots):
    request = request_tuple[1]
    request = helpers.normalize_string(request)
    request = helpers.replace_slots_in_request(request, all_slots)
    return request_tuple[0], request


def _parse_line(line: str, num_of_columns: int, intent_config: dict, all_slots: list, all_requests: list):
    # intent \t slots \t request \t lang \t tokens
    parsed_line = line.split('\t')
    if len(parsed_line) != num_of_columns:
        raise Exception('invalid number of columns')

    intent_name = parsed_line[0]
    if intent_name not in intent_config:
        return

    request = parsed_line[2]
    if request:
        if helpers.is_request_valid(request, intent_name):
            all_requests.append((intent_name, request))

    slots_csv = parsed_line[1]
    if not slots_csv:
        return

    slots = slots_csv.split(',')
    for slot in slots:
        slot_split = slot.split(':')

        slot_name = slot_split[2]
        if slot_name not in intent_config[intent_name][const.ALL_SLOTS]:
            continue

        slot_value = request[eval(slot_split[0]):eval(slot_split[1])]
        if not helpers.contains_letters(slot_value):
            continue

        slot_value = helpers.normalize_string(slot_value)
        if not helpers.is_slot_value_valid(
                slot_value=slot_value,
                intent_config=intent_config,
                current_intent_name=intent_name):
            continue

        if helpers.already_exists_in_list(slot_value, all_slots, 2):
            continue

        all_slots.append((intent_name, slot_name, slot_value))
