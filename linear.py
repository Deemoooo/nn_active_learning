""" Multilayer Perceptron.
A Multilayer Perceptron (Neural Network) implementation example using
TensorFlow library. This example is using the MNIST database of handwritten
digits (http://yann.lecun.com/exdb/mnist/).
Links:
    [MNIST Dataset](http://yann.lecun.com/exdb/mnist/).
Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
"""

# ------------------------------------------------------------------
#
# THIS EXAMPLE HAS BEEN RENAMED 'neural_network.py', FOR SIMPLICITY.
#
# ------------------------------------------------------------------


from __future__ import print_function

# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

import tensorflow as tf
import csv
import numpy as np

# Parameters
learning_rate = 0.01
training_epochs = 2000
display_step = 1

# Network Parameters
n_hidden_1 = 256 # 1st layer number of neurons
n_hidden_2 = 256 # 2nd layer number of neurons
n_input = 2 # MNIST data input (img shape: 28*28)
n_classes = 2 # MNIST total classes (0-9 digits)

# tf Graph input
X = tf.placeholder("float", [None, n_input])
Y = tf.placeholder("float", [None, n_classes])

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

train_set = []
test_set_X = []
test_set_Y = []
train_set_X = []
train_set_Y = []

# read training data
with open('train.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        train_set.append(row)

# read testing data
with open('test.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        test_set_X.append(row[1:])
        if (row[0]==1):
            test_set_Y.append([0.0,1.0])
        else:
            test_set_Y.append([1.0,0.0])

# read testing data
with open('train.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        train_set_X.append(row[1:])
        if (row[0]==1):
            train_set_Y.append([0.0,1.0])
        else:
            train_set_Y.append([1.0,0.0])


# Create model
def multilayer_perceptron(x):
    # Hidden fully connected layer with 256 neurons
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    # Hidden fully connected layer with 256 neurons
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    # Output fully connected layer with a neuron for each class
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

# Construct model
logits = multilayer_perceptron(X)

# Define loss and optimizer
loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    logits=logits, labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)
# Initializing the variables
init = tf.global_variables_initializer()

grads = tf.gradients(loss_op, X)

with tf.Session() as sess:
    sess.run(init)

    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        total_batch = 700
        # Loop over all batches
       #for i in range(total_batch):
        # batch_x = np.asarray([[train_set[i][1],train_set[i][2]]])
        # if(train_set[i][0]==1):
        #     batch_y=np.asarray([[0.0,1.0]])
        # else:
        #     batch_y=np.asarray([[1.0,0.0]])
        
        ##batch_y = np.asarray([[train_set[i][0],1.0]])
        # Run optimization op (backprop) and cost op (to get loss value)
        gradients,_, c = sess.run([grads ,train_op, loss_op], feed_dict={X: train_set_X,
                                                        Y: train_set_Y})
        if c<0.00001 :
            break
        avg_cost += c

        #np.savetxt("gradients.csv", gradients, delimiter="\n", fmt = "%.32f")
        print(gradients)
        
        # Compute average loss
            
        # Display logs per epoch step
       # if epoch % display_step == 0:
        print("Epoch:", '%04d' % (epoch+1), "cost={:.9f}".format(c))

    print("Optimization Finished!")

   
#  [array([[2, 1]], dtype=int32)]
    # Test model
    pred = tf.nn.softmax(logits)  # Apply softmax to logits
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(Y, 1))
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print("Accuracy:", accuracy.eval({X: np.asarray(test_set_X), Y: np.asarray(test_set_Y)}))
    print("Accuracy:", accuracy.eval({X: np.asarray(train_set_X), Y: np.asarray(train_set_Y)}))