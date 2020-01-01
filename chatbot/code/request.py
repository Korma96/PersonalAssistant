import chatbot.code.constants as const


class Request:

    def __init__(self, original, slots):
        self._original = original
        self.with_replaced_slots = self._replace_slot_values_with_slot_names(original, slots)

    @staticmethod
    def _replace_slot_values_with_slot_names(request: str, slots):
        for intent_name in slots:
            intent_slots = slots[intent_name][const.SLOTS]
            for slot_name in intent_slots:
                slot_values = intent_slots[slot_name]
                for slot_value in slot_values:
                    if slot_value in request:
                        request = request.replace(slot_value, slot_name)

        return request
