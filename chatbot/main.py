import dataset.code.dataset_formatter as df
import chatbot.code.data_service as ds
import chatbot.code.model_service as ms
from chatbot.code.assistant import Assistant
from os import path


def get_assistant():
    # load data
    intent_config = ds.read_intent_configuration('../dataset/formatted_data/intents_config.json')

    if path.exists('data/training_data'):
        all_words, slots, train_x, train_y = ds.load_training_data("data/training_data")
    else:
        if not path.exists('../dataset/formatted_data/intents.json'):
            df.format('../dataset/original_data/train-en.tsv',
                      '../dataset/formatted_data/intents.json',
                      intent_config)

        tokenized_requests, all_words, slots = ds.process_intent_data(intents_path='../dataset/formatted_data/intents.json')
        train_x, train_y = ds.create_training_data(tokenized_requests=tokenized_requests,
                                                   intent_names=list(intent_config.keys()),
                                                   all_words=all_words)
        ds.save_training_data(all_words=all_words,
                              slots=slots,
                              train_x=train_x,
                              train_y=train_y)

    try:
        model = ms.create_model([None, len(train_x[0])], len(train_y[0]))
        model.load('data/model.tflearn')
    except:
        model = ms.create_model([None, len(train_x[0])], len(train_y[0]))
        model.fit(train_x, train_y, n_epoch=1, batch_size=8)
        model.save('data/model.tflearn')

    return Assistant(model=model, intent_config=intent_config, all_words=all_words, slots=slots)


if __name__ == '__main__':
    assistant = get_assistant()
    print('')
