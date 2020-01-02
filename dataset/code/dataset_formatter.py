import chatbot.code.constants as const
import chatbot.code.helpers as helpers


def format(input_path, intents_output_path, slots_output_path, intent_config):
    desired_intent_names = list(intent_config.keys())

    with open(input_path, 'r') as tsv_file:
        lines = tsv_file.readlines()

    intents = {}
    all_slots = []
    num_of_columns = len(lines[0].split('\t'))
    for line in lines:
        parse_line(line, intents, num_of_columns, desired_intent_names, intent_config, all_slots)

    # sort requests
    for intent_name in intents:
        intent = intents[intent_name]
        intent[const.REQUESTS].sort(key=len)

    # sort slots
    all_slots.sort(key=lambda x: len(x[2]), reverse=True)

    helpers.write_json_to_file(intents, intents_output_path)
    helpers.write_json_to_file(all_slots, slots_output_path)


def parse_line(line: str, intents: dict, num_of_columns: int, desired_intent_names: list, intent_config, all_slots):
    # intent \t slots \t request \t lang \t tokens
    parsed_line = line.split('\t')
    if len(parsed_line) != num_of_columns:
        raise Exception('invalid number of columns')

    intent_name = parsed_line[0]
    if intent_name in desired_intent_names:
        if intent_name not in intents:
            intents[intent_name] = {const.REQUESTS: []}

        intent = intents[intent_name]
        request = parsed_line[2].lower()
        slots_csv = parsed_line[1]
        if slots_csv:
            slots = slots_csv.split(',')
            parsed_slots = []
            for slot in slots:
                splitted_slot = slot.split(':')
                start_char_index = eval(splitted_slot[0])
                end_char_index = eval(splitted_slot[1])
                slot_name = splitted_slot[2]

                if slot_name in intent_config[intent_name][const.ALL_SLOTS]:

                    slot_value = request[start_char_index:end_char_index]

                    # do not add invalid data
                    if is_invalid(slot_value, intent_config):
                        continue

                    if (const.ALARM in intent_name and
                            len(slot_value) < 10 and
                            const.REMINDER in slot_value):
                        continue
                    if (const.REMINDER in intent_name and
                            len(slot_value) < 10 and
                            const.ALARM in slot_value):
                        continue

                    all_slots.append((intent_name, slot_name, slot_value))
                    parsed_slots.append((slot_name, slot_value))
            # TODO: replace slot values with slot names after sorting all slots
            for parsed_slot in parsed_slots:
                slot_name = parsed_slot[0]
                slot_value = parsed_slot[1]
                request = request.replace(slot_value, slot_name, 1)

        # do not add invalid data
        if const.ALARM in intent_name and const.REMINDER in request:
            return
        if const.REMINDER in intent_name and const.ALARM in request:
            return

        if request not in intent[const.REQUESTS]:
            intent[const.REQUESTS].append(request)


def is_invalid(slot_value: str, intent_config):
    for intent_name in intent_config.keys():
        if slot_value in intent_name:
            return True
        for slot_name in intent_config[intent_name][const.ALL_SLOTS]:
            if slot_value in slot_name:
                return True

    return False

