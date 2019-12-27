import chatbot.code.constants as const
import chatbot.code.settings as s
import chatbot.code.helpers as helpers


class Assistant:

    def __init__(self, model, intent_config: dict, all_words: list, slots: dict):
        self._model = model
        self._intent_config = intent_config
        # only intents in slots are in same order as they are used for training
        self._intent_names = list(slots.keys())
        self._all_words = all_words
        self._slots = slots
        self._current_request = None

    def request(self, request: str):
        results = self._classify(request)
        # if we have a classification then find the matching intent tag
        if len(results) > 0:
            # take only one result with higher probability
            result = results[0]
            intent = self._intent_config[result[0]]
            # TODO: return response with the most matching slots
            return intent[const.RESPONSES][0]
        else:
            # TODO: when this case happens ? investigate
            # TODO: return default 'request unrecognized' message
            pass

    def _classify(self, request: str):
        # TODO: replace slot values with slot names in request
        request_words = helpers.parse_request(request)
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
