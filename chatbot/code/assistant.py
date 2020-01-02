import chatbot.code.constants as const
import chatbot.code.settings as s
import chatbot.code.helpers as helpers
from chatbot.code.request import Request


class Assistant:

    def __init__(self, model, intent_config: dict, all_words: list, slots: list):
        self._model = model
        self._intent_config = intent_config  # TODO: parse intent config
        # intents in intent_config are in same order as they are used for training
        self._intent_names = list(intent_config.keys())
        self._all_words = all_words
        self._slots = slots
        self._current_request = None

    def request(self, request: str):
        results = self._classify(request)
        print(self._current_request.with_replaced_slots)
        print(results)
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
            # TODO: return response with the most matching slots
            return intent[const.RESPONSES][0]
        else:
            return s.EMPTY_RESPONSE

    def request_test(self, request: str):
        results = self._classify(request)
        # if we have a classification then find the matching intent tag
        if len(results) > 0:
            return results[0][0]
        else:
            return s.EMPTY_RESPONSE

    def _classify(self, request: str):
        self._current_request = Request(request, self._slots)
        request_words = helpers.parse_request(self._current_request.with_replaced_slots)
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
