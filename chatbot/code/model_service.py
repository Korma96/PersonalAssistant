import tflearn
import tensorflow as tf


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
