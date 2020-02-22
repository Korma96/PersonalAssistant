import tflearn
import tensorflow as tf


def create_model(train_x_data_shape, train_y_data_shape):
    # reset underlying graph data
    tf.reset_default_graph()
    # Build neural network
    net = tflearn.input_data(shape=train_x_data_shape)
    net = tflearn.fully_connected(net, 8, activation="relu")
    net = tflearn.fully_connected(net, 8, activation="relu")
    net = tflearn.fully_connected(net, train_y_data_shape, activation='softmax')
    net = tflearn.regression(net)

    # Define model
    return tflearn.DNN(net)


def get_model(train_x, train_y):
    try:
        model = create_model([None, len(train_x[0])], len(train_y[0]))
        model.load('data/model.tflearn')
    except Exception:
        model = create_model([None, len(train_x[0])], len(train_y[0]))
        model.fit(train_x, train_y, n_epoch=50, batch_size=64)
        model.save('data/model.tflearn')
    return model
