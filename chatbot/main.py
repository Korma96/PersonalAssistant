import dataset.code.dataset_formatter as df
import chatbot.code.data_service as ds
import chatbot.code.model_service as ms
from chatbot.code.assistant import Assistant
from os import path
import chatbot.code.settings as s
import sys


def get_assistant():
    # load data
    intent_config = ds.read_intent_configuration(s.intents_config_path)

    if path.exists(s.train_data_path):
        all_words, slots, train_x, train_y = ds.load_training_data(s.train_data_path)
    else:
        if not path.exists(s.intents_path):
            df.format(s.original_train_data_path,
                      s.intents_path,
                      intent_config)

        tokenized_requests, all_words, slots = ds.process_intent_data(intents_path=s.intents_path)
        train_x, train_y = ds.create_training_data(tokenized_requests=tokenized_requests,
                                                   intent_names=list(intent_config.keys()),
                                                   all_words=all_words)
        ds.save_training_data(all_words=all_words,
                              slots=slots,
                              train_x=train_x,
                              train_y=train_y)

    # get model
    try:
        model = ms.create_model([None, len(train_x[0])], len(train_y[0]))
        model.load('data/model.tflearn')
    except Exception:
        exc_info = sys.exc_info()
        print(exc_info)
        model = ms.create_model([None, len(train_x[0])], len(train_y[0]))
        model.fit(train_x, train_y, n_epoch=50, batch_size=8)
        model.save('data/model.tflearn')

    return Assistant(model=model, intent_config=intent_config, all_words=all_words, slots=slots)


if __name__ == '__main__':
    assistant = get_assistant()
    response = assistant.request('hey assistant, set new alarm for tomorrow at 6:00 am')
    print(response)
