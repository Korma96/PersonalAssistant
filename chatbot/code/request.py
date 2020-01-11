import chatbot.code.helpers as helpers


class Request:

    def __init__(self, original, slots):
        self.original = original
        self.normalized = helpers.normalize_string(self.original)
        self.with_replaced_slots, self.replaced_slots = helpers.replace_slots_in_request(self.normalized, slots)
