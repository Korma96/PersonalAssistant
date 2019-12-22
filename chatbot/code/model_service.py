import tflearn
import tensorflow as tf


# to do: should not be independent method
def create_trained_model(train_x, train_y):
    model = create_model([None, len(train_x[0])], len(train_y[0]))
    # Start training (apply gradient descent algorithm)
    model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
    model.save('data/model.tflearn')
    return model


def load_model(train_x_data_shape, train_y_data_shape):
    # load our saved model
    model = create_model(train_x_data_shape, train_y_data_shape)
    model.load('data/model.tflearn')
    return model


def create_model(train_x_data_shape, train_y_data_shape):
    # reset underlying graph data
    tf.reset_default_graph()
    # Build neural network
    net = tflearn.input_data(shape=train_x_data_shape)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, train_y_data_shape, activation='softmax')
    net = tflearn.regression(net)

    # Define model and setup tensorboard
    return tflearn.DNN(net, tensorboard_dir='tflearn_logs')
