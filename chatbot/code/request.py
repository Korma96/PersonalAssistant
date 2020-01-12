import chatbot.code.helpers as helpers
import chatbot.code.constants as const
import re


class Request:

    def __init__(self, original, slots):
        self.original = original
        self.normalized = helpers.normalize_string(self.original)
        self.with_replaced_slots, self.replaced_slots = helpers.replace_slots_in_request(self.normalized, slots)

    def normalize_slot_values(self):
        numeric = const.NUMERIC.strip()
        for key, value in self.replaced_slots.items():
            for i, slot_value in enumerate(value):
                if numeric in slot_value:
                    new_slot_value = self._replace_numbers(slot_value)
                    value[i] = new_slot_value
                    self.replaced_slots[key] = value

    def _replace_numbers(self, string: str) -> str:
        numeric = const.NUMERIC.strip()
        pattern = string.replace(numeric, '[0-9]', 1)
        count = string.count(numeric)
        if count > 1:
            numeric = ' ' + numeric
            pattern = pattern.replace(numeric, '[0-9]')

        occurrences = re.findall(pattern, self.original)
        if occurrences:
            return occurrences[0]
        return string
