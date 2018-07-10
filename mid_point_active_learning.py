from __future__ import print_function

import math
import random

import models
import numpy as np
import tensorflow as tf
import formula

import testing_function
import util
def generate_accuracy(train_data_file, test_data_file,formu,category):

    # Parameters
    learning_rate = 0.1
    training_epochs = 100

    pointsNumber = 10
    active_learning_iteration = 10
    threhold = 5
    test_set_X = []
    test_set_Y = []
    train_set_X = []
    train_set_Y = []

    util.preprocess(train_set_X, train_set_Y, test_set_X, test_set_Y, train_data_file,test_data_file,read_next=True)
    # Network Parameters
    n_hidden_1 = 10  # 1st layer number of neurons
    n_hidden_2 = 10  # 2nd layer number of neurons
    n_input = len(train_set_X[0])  # MNIST data input (img shape: 28*28)
    n_classes = 1  # MNIST total classes (0-9 digits)

    random_seed = 0
    random.seed(random_seed)
    np.random.seed(random_seed)
    tf.set_random_seed(random_seed)
    
    train_acc_list=[]
    test_acc_list=[]
    result = []


    
    # tf Graph input
    X = tf.placeholder("float", [None, n_input])
    Y = tf.placeholder("float", [None, n_classes])
    weights = {
        'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1], mean=0)),
        'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2], mean=0)),
        'out': tf.Variable(tf.random_normal([n_hidden_1, n_classes], mean=0))
    }
    biases = {
        'b1': tf.Variable(tf.random_normal([n_hidden_1])),
        'b2': tf.Variable(tf.random_normal([n_hidden_2])),
        'out': tf.Variable(tf.random_normal([n_classes]))
    }


    # Construct model
    logits = util.multilayer_perceptron(X, weights, biases)

    # Define loss and optimizer
    loss_op = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=logits, labels=Y))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
    # optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
    # Initializing the variables
    train_op = optimizer.minimize(loss_op)
    # Initializing the variables
    init = tf.global_variables_initializer()

    newgrads = tf.gradients(logits, X)
    y = None


    # class point_pair:
    #     def __init__(self, point_label_0, point_label_1, distance):
    #         self.point_label_0 = point_label_0
    #         self.point_label_1 = point_label_1
    #         self.distance = distance


    for i in range(active_learning_iteration):
        print("*******", i, "th loop:")
        print("training set size", len(train_set_X))
        pointsNumber = 10
        with tf.Session() as sess:
            sess.run(init)
            label_0 = []
            label_1 = []
            label_0, label_1 = util.data_partition(train_set_X, train_set_Y)
            print(len(label_0), len(label_1))
            distanceList = []
            point_pairList = {}

            for m in label_0:
                for n in label_1:
                    distance=0
                    for d in range(n_input):

                        distance += (m[d] - n[d]) * (m[d] - n[d])
                    distance=math.sqrt(distance)
                    if (distance > threhold):

                        # if(distance in distanceList):
                        ##print ("cnm")
                        key=()
                        for h in range(n_input):
                            tmpKey=(m[h],n[h])
                            key=key+tmpKey
                       

                        value = distance
                        if (not point_pairList):
                            point_pairList[key] = value
                        elif (not (key in point_pairList.keys())):
                            point_pairList[key] = value
                        distanceList.append(distance)
                # print(m,n)

            # print (distanceList)

            util.quickSort(distanceList)
            # print(distanceList)
            selectedList = []
            # pivot=0
            # while pivot<pointsNumber:

            # 	if(distanceList[pivot] in selectedList):
            # 		pointsNumber+=1
            # 		pivot+=1

            # 	else:

            # 		selectedList.append(distanceList[pivot])
            # 		pivot+=1
            length = len(distanceList)
            index1 = length / 3
            index2 = length / 3 * 2
            pointer = 0
            for p in range(3):
                if (pointer < index1):
                    num = int(pointsNumber * 0.6)
                    util.addPoints(num, distanceList, selectedList, pointer)
                    pointer = index1
                elif (pointer < index2):
                    num = int(pointsNumber * 0.3)
                    util.addPoints(num, distanceList, selectedList, pointer)
                    #
                    pointer = index2
                else:
                    num = int(pointsNumber * 0.1)
                    util.addPoints(num, distanceList, selectedList, pointer)

                # pick large pooints

            ##print (selectedList)
            ##print (distanceList)
            # print (len(selectedList))
            # print (len(point_pairList))
            # print (train_set_X)


            for m in selectedList:
                for k, v in point_pairList.items():
                    if (m == v):
                        
                        point_0 = []
                        point_1 = []
                        for b in range(len(k)):
                            if(b%2==0):
                                point_0.append(k[b])
                            else:
                                point_1.append(k[b])
                        middlepoint = []
                        
                        for b in range(n_input):
                            middlepoint.append((point_0[b]+point_1[b])/2.0)
                        
                        # print (point_0)
                        # print("original point", point_0, point_1)
                        # print("middlepoint", middlepoint)
                      
                        if category == formula.POLYHEDRON:
                            flag = testing_function.polycircleModel(formu[0], formu[1], middlepoint)
                        elif category== formula.POLYNOMIAL:
                            flag= testing_function.polynomialModel(formu[:-1],middlepoint,formu[-1])
                       
                        if (flag):
                            if (middlepoint not in train_set_X):
                                train_set_X.append(middlepoint)
                                train_set_Y.append([0])

                        else:
                            if (middlepoint not in train_set_X):
                                train_set_X.append(middlepoint)
                                train_set_Y.append([1])

            for epoch in range(training_epochs):
                _, c = sess.run([train_op, loss_op], feed_dict={X: train_set_X, Y: train_set_Y})
            train_y = sess.run(logits, feed_dict={X: train_set_X})
            test_y = sess.run(logits, feed_dict={X: test_set_X})

            print("new train size", len(train_set_X), len(train_set_Y))
            train_acc = util.calculateAccuracy(train_y, train_set_Y, False)
            test_acc = util.calculateAccuracy(test_y, test_set_Y, False)

            train_acc_list.append(train_acc)
            test_acc_list.append(test_acc)
    result.append(train_acc_list)
    result.append(test_acc_list)
    return result