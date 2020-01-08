import chatbot.code.constants as const
import chatbot.code.helpers as helpers


def format(input_path, intents_output_path, requests_output_path, slots_output_path, intent_config):
    with open(input_path, 'r') as tsv_file:
        lines = tsv_file.readlines()

    all_slots = []  # (intent_name, slot_name, slot_value)
    all_requests = []  # (intent_name, request)
    num_of_columns = len(lines[0].split('\t'))
    for line in lines:
        _parse_line(line, num_of_columns, intent_config, all_slots, all_requests)

    # sort slots
    all_slots.sort(key=lambda x: len(x[2]), reverse=True)

    processed_requests = []
    for request_tuple in all_requests:
        request = request_tuple[1]
        request = helpers.normalize_string(request)
        request, _ = helpers.replace_slots_in_request(request, all_slots)
        if not helpers.already_exist(request, processed_requests, 1):
            processed_requests.append((request_tuple[0], request))
    processed_requests.sort(key=lambda x: len(x[1]))

    helpers.write_json_to_file(processed_requests, requests_output_path)
    helpers.write_json_to_file(all_slots, slots_output_path)

    # convert to user friendly view

    intents = {}  # { intent_name : { slots: { slot_name: [], ... }, requests[] } }

    for slot in all_slots:
        intent_name = slot[0]
        if intent_name not in intents:
            intents[intent_name] = {const.REQUESTS: [], const.SLOTS: {}}
        slot_name = slot[1]
        if slot_name not in intents[intent_name][const.SLOTS]:
            intents[intent_name][const.SLOTS][slot_name] = []
        intents[intent_name][const.SLOTS][slot_name].append(slot[2])

    for request in processed_requests:
        intent_name = request[0]
        request_val = request[1]
        intents[intent_name][const.REQUESTS].append(request_val)

    # sort slots and requests
    for intent_name in intents.keys():
        intent = intents[intent_name]
        intent[const.REQUESTS].sort(key=len)
        for slot_name in intent[const.SLOTS].keys():
            intent[const.SLOTS][slot_name].sort(key=len)

    helpers.write_json_to_file(intents, intents_output_path)


def _parse_line(line: str, num_of_columns: int, intent_config: dict, all_slots: list, all_requests: list):
    # intent \t slots \t request \t lang \t tokens
    parsed_line = line.split('\t')
    if len(parsed_line) != num_of_columns:
        raise Exception('invalid number of columns')

    intent_name = parsed_line[0]
    if intent_name in intent_config.keys():
        request = parsed_line[2]
        if request:
            if helpers.is_request_valid(request, intent_name):
                all_requests.append((intent_name, request))

        slots_csv = parsed_line[1]
        if slots_csv:
            slots = slots_csv.split(',')
            for slot in slots:
                splitted_slot = slot.split(':')
                start_char_index = eval(splitted_slot[0])
                end_char_index = eval(splitted_slot[1])
                slot_name = splitted_slot[2]

                if slot_name in intent_config[intent_name][const.ALL_SLOTS]:
                    slot_value = request[start_char_index:end_char_index]
                    slot_value = helpers.normalize_string(slot_value)

                    if not helpers.is_slot_value_valid(
                            slot_value=slot_value,
                            intent_config=intent_config,
                            current_intent_name=intent_name):
                        continue

                    if not helpers.already_exist(slot_value, all_slots, 2):
                        all_slots.append((intent_name, slot_name, slot_value))
