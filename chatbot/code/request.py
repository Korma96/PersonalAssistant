
class Request:

    def __init__(self, original, slots):
        self._original = original
        self.with_replaced_slots = self._replace_slot_values_with_slot_names(original, slots)

    @staticmethod
    def _replace_slot_values_with_slot_names(request: str, slots):
        # slot = (intent_name, slot_name, slot_value)
        for slot in slots:
            if slot[2] in request:
                request = request.replace(slot[2], slot[1])

        return request
