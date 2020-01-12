

class InvalidData:

    def __init__(self, intent='', request='', slot_name='', slot_value='', message=''):
        self.intent = intent
        self.request = request
        self.slot_name = slot_name
        self.slot_value = slot_value
        self.message = message

    def __str__(self):
        return [self.intent, self.request, self.slot_name, self.slot_value, self.message]
