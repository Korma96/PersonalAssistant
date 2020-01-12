import chatbot.code.helpers as helpers
import chatbot.code.constants as const
import re


class Request:

    def __init__(self, original, slots, is_test=False):
        self.original = original
        self.normalized = helpers.normalize_string(self.original)
        if is_test:
            self.with_replaced_slots = helpers.replace_slots_in_request(self.normalized, slots)
        else:
            self.with_replaced_slots, self.replaced_slots = helpers.replace_slots_in_request_and_get_slots(self.normalized, slots)

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
        # try to replace common scenarios
        string = string.replace('num num : num num', '[0-9][0-9]:[0-9][0-9]')
        string = string.replace('num : num num', '[0-9]:[0-9][0-9]')
        pattern = string.replace('num num', '[0-9][0-9]')
        if numeric in string:
            # if there are still numeric values in
            pattern = pattern.replace(numeric, '[0-9]', 1)
            count = pattern.count(numeric)
            if count > 0:
                numeric = ' ' + numeric
                pattern = pattern.replace(numeric, '[0-9]')

        occurrences = re.findall(pattern, self.original)
        if occurrences:
            return occurrences[0]
        return string
