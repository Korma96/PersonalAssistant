import json
import chatbot.code.constants as const

'''
intents: {
    intent_name: {
        'slots': {
            slot_name1: []
            slot_name2: []
            slot_name3: []
                 .
                 .
                 .
        },
        'requests': []
    }
}
'''


def format(input_path, output_path, intent_config):
    # if desired_intent_names is empty list then all intents will be added to output
    desired_intent_names = intent_config.keys()
    are_all_intents_desired = len(desired_intent_names) == 0

    with open(input_path, 'r') as tsv_file:
        lines = tsv_file.readlines()

    intents = {}
    num_of_columns = len(lines[0].split('\t'))
    for line in lines:
        # intent \t slots \t request \t lang \t tokens
        parsed_line = line.split('\t')
        if len(parsed_line) != num_of_columns:
            raise Exception('invalid number of columns')

        intent_name = parsed_line[0]
        if are_all_intents_desired or intent_name in desired_intent_names:
            if intent_name not in intents:
                intents[intent_name] = {const.SLOTS: {}, const.REQUESTS: []}

            intent = intents[intent_name]
            request = parsed_line[2]
            # dataset contains duplicate requests
            if request not in intent[const.REQUESTS]:
                intent[const.REQUESTS].append(request)

                slots_csv = parsed_line[1]
                if slots_csv:
                    slots = slots_csv.split(',')
                    for slot in slots:
                        splitted_slot = slot.split(':')
                        start_char_index = eval(splitted_slot[0])
                        end_char_index = eval(splitted_slot[1])
                        slot_name = splitted_slot[2]
                        if are_all_intents_desired or slot_name in intent_config[intent_name][const.ALL_SLOTS]:
                            if slot_name not in intent[const.SLOTS]:
                                intent[const.SLOTS][slot_name] = []

                            slot_value = request[start_char_index:end_char_index]
                            if slot_value not in intent[const.SLOTS][slot_name]:
                                intent[const.SLOTS][slot_name].append(slot_value)

    json_str = json.dumps(intents, indent=True)
    with open(output_path, 'w+') as json_file:
        json_file.write(json_str)
