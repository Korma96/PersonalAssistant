import chatbot.code.settings as s
import chatbot.code.helpers as helpers


class PercentTracker:

    def __init__(self, whole_count, show_period=s.default_show_period):
        self._whole_count = whole_count
        self._show_period = show_period
        self._counter = 0

    def do_iteration(self):
        self._counter += 1
        if self._counter % self._show_period == 0:
            print(str(round(helpers.get_percent(part=self._counter, whole=self._whole_count)*100)) + '%')
