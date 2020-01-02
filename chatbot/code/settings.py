# paths
# train
intents_config_path = '../dataset/formatted_data/intents_config.json'
original_train_data_path = '../dataset/original_data/train-en.tsv'
intents_path = '../dataset/formatted_data/intents.json'
slots_path = '../dataset/formatted_data/slots.json'
train_data_path = 'data/training_data'
# test
original_test_data_path = '../dataset/original_data/test-en.tsv'
original_eval_data_path = '../dataset/original_data/eval-en.tsv'

# thresholds
ERROR_THRESHOLD = 0.25
RESPONSE_THRESHOLD = 0.7
SIMILARITY_THRESHOLD = 0.1

# assistant config
EMPTY_RESPONSE = ''
NOT_SURE = 'Can you please rephrase the request?'

# general
ignore_words = ['?', '!']
QUIT = 'q'
YOU = 'You: '
CHATBOT = 'Chatbot: '
GOOD_BYE_MESSAGE = 'Good bye'
