import chatbot.code.helpers as helpers


class PercentTracker:

    def __init__(self, whole_count):
        self._whole_count = whole_count
        self._show_period = int(whole_count / 100)
        self._counter = 0

    def do_iteration(self):
        self._counter += 1
        if self._counter % self._show_period == 0:
            print(str(round(helpers.get_percent(part=self._counter, whole=self._whole_count)*100)) + '%')
