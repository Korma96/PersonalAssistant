import chatbot.code.constants as const
import chatbot.code.settings as s
import chatbot.code.helpers as helpers
from chatbot.code.request import Request


class Assistant:

    def __init__(self, model, intent_config: dict, all_words: list, slots: list):
        self._model = model
        self._intent_config = intent_config
        # intents in intent_config are in same order as they are used for training
        self._intent_names = list(intent_config.keys())
        self._all_words = all_words
        self._slots = slots
        self._current_request: Request = None

    def request(self, request: str):
        results = self._classify(request)
        if s.DEBUG:
            print(results)
            print(self._current_request.with_replaced_slots)
            print(self._current_request.replaced_slots)
        # if we have a classification then find the matching intent tag
        if len(results) > 0:
            if results[0][1] < s.RESPONSE_THRESHOLD:
                return s.EMPTY_RESPONSE
            if len(results) > 1:
                if results[0][1] - results[1][1] < s.SIMILARITY_THRESHOLD:
                    return s.NOT_SURE

            # take only one result with higher probability
            result = results[0]
            intent = self._intent_config[result[0]]

            if self._is_required_slot_missing(intent):
                return s.MISSING_REQUIRED_SLOT

            response = self._get_most_relevant_response(intent)
            self._current_request.normalize_slot_values()
            response = self._replace_slot_names_with_values(response)
            self._send_api_request()
            return response
        else:
            return s.EMPTY_RESPONSE

    def request_test(self, request: str):
        results = self._classify(request, is_test=True)
        # if we have a classification then find the matching intent tag
        if len(results) > 0:
            return results[0][0]
        else:
            return s.EMPTY_RESPONSE

    def _send_api_request(self):
        with open(s.recognized_slots_output_path, 'a') as file:
            json_str = helpers.get_json_string(self._current_request.__dict__)
            file.write('\n-------------------------------------------\n')
            file.write(json_str)

    def _replace_slot_names_with_values(self, response):
        for slot_name, slot_value in self._current_request.replaced_slots.items():
            old_str = '{'+slot_name+'}'
            new_str = ' '.join(slot_value)
            response = response.replace(old_str, new_str)
        return response

    def _get_most_relevant_response(self, intent):
        most_relevant_response = (-1, '')
        for response in intent[const.RESPONSES]:
            slot_number = 0
            for slot_name in self._current_request.replaced_slots.keys():
                if slot_name in response:
                    slot_number += 1
            if slot_number > most_relevant_response[0]:
                most_relevant_response = (slot_number, response)

        return most_relevant_response[1]

    def _is_required_slot_missing(self, intent):
        for required_slot in intent[const.REQUIRED_SLOTS]:
            if required_slot not in self._current_request.replaced_slots:
                return True
        return False

    def _classify(self, request: str, is_test=False):
        self._current_request = Request(request, self._slots, is_test)
        request_words = helpers.tokenize_request(self._current_request.with_replaced_slots)
        bag = helpers.create_bag_of_words(request_words, self._all_words)
        # generate probabilities from the model
        results = self._model.predict([bag])[0]
        # filter out predictions below a threshold
        results = [[index, probability] for index, probability in enumerate(results) if probability > s.ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for result in results:
            return_list.append((self._intent_names[result[0]], result[1]))
        # return list of tuples (intent name, probability)
        return return_list
