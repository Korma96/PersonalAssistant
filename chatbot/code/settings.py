# paths
# train
intents_config_path = '../dataset/formatted_data/intents_config.json'
original_train_data_path = '../dataset/original_data/train-en.tsv'
requests_path = '../dataset/formatted_data/train/requests.json'
slots_path = '../dataset/formatted_data/train/slots.json'
intents_path = '../dataset/formatted_data/train/intents.json'
train_data_path = 'data/training_data'
all_words_path = 'data/all_words.json'
# test
original_test_data_path = '../dataset/original_data/test-en.tsv'
original_eval_data_path = '../dataset/original_data/eval-en.tsv'
test_requests_path = '../dataset/formatted_data/test/requests.json'
test_slots_path = '../dataset/formatted_data/test/slots.json'
test_intents_path = '../dataset/formatted_data/test/intents.json'
recognized_slots_output_path = '../dataset/formatted_data/api.txt'

# thresholds
ERROR_THRESHOLD = 0.25
RESPONSE_THRESHOLD = 0.7
SIMILARITY_THRESHOLD = 0.1

# assistant config
EMPTY_RESPONSE = ''
NOT_SURE = 'Can you please rephrase the request?'
MISSING_REQUIRED_SLOT = 'Your request is incomplete, please provide more information.'

# general
default_show_period = 200
ignore_words = ['?', '!']
QUIT = 'q'
YOU = 'You: '
CHATBOT = 'Chatbot: '
GOOD_BYE_MESSAGE = 'Good bye'
DEBUG = False
