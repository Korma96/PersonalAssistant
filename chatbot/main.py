import dataset.code.dataset_formatter as df
import chatbot.code.data_service as ds
import chatbot.code.model_service as ms
from chatbot.code.assistant import Assistant
from os import path
import chatbot.code.settings as s
import chatbot.code.helpers as helpers
from chatbot.code.percent_tracker import PercentTracker


def get_assistant():
    # load data
    intent_config = helpers.read_json_from_file(s.intents_config_path)

    if path.exists(s.train_data_path):
        all_words, train_x, train_y = ds.load_training_data(s.train_data_path)
    else:
        if not path.exists(s.requests_path):
            df.format_dataset(input_path=s.original_train_data_path,
                              intents_output_path=s.intents_path,
                              requests_output_path=s.requests_path,
                              slots_output_path=s.slots_path,
                              intent_config=intent_config)

        tokenized_requests, all_words = ds.process_requests(requests_path=s.requests_path)
        train_x, train_y = ds.create_training_data(tokenized_requests=tokenized_requests,
                                                   intent_names=list(intent_config.keys()),
                                                   all_words=all_words)
        ds.save_training_data(path=s.train_data_path,
                              all_words=all_words,
                              train_x=train_x,
                              train_y=train_y)

    slots = helpers.read_json_from_file(s.slots_path)

    # get model
    try:
        model = ms.create_model([None, len(train_x[0])], len(train_y[0]))
        model.load('data/model.tflearn')
    except Exception:
        model = ms.create_model([None, len(train_x[0])], len(train_y[0]))
        model.fit(train_x, train_y, n_epoch=10, batch_size=8)
        model.save('data/model.tflearn')

    return Assistant(model=model, intent_config=intent_config, all_words=all_words, slots=slots)


def get_accuracy(assistant: Assistant, original_path):
    intent_config = helpers.read_json_from_file(s.intents_config_path)
    test_data = ds.get_test_data(original_path, list(intent_config.keys()))
    request_count = len(test_data)
    success_counter = 0
    failure_counter = 0
    percent_tracker = PercentTracker(request_count)
    print('Testing assistant started')
    for test_tuple in test_data:
        intent = assistant.request_test(test_tuple[1])
        if intent == test_tuple[0]:
            success_counter += 1
        else:
            failure_counter += 1

        percent_tracker.do_iteration()
    print('Testing assistant finished')

    return helpers.get_percent(success_counter, request_count)


def test_accuracy(assistant: Assistant):
    train_acc = get_accuracy(assistant, s.original_train_data_path)
    test_acc = get_accuracy(assistant, s.original_test_data_path)
    eval_acc = get_accuracy(assistant, s.original_eval_data_path)
    print('Train acc: ' + str(train_acc) + '\nTest acc: ' + str(test_acc) + '\nEval acc: ' + str(eval_acc))


def manual_test(assistant: Assistant):
    while True:
        request = input(s.YOU)
        if request == s.QUIT:
            print(s.CHATBOT + s.GOOD_BYE_MESSAGE)
            break

        response = assistant.request(request)
        print(s.CHATBOT + response)


if __name__ == '__main__':
    assistant = get_assistant()
    manual_test(assistant)
