import csv

import tensorflow as tf
import numpy as np
# from matplotlib import pyplot as plt


def plot_decision_boundary(pred_func, train_set_X, train_set_Y):
    X = np.array(train_set_X)
    Y = np.array(train_set_Y)

    # Set min and max values and give it some padding
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    h = 10
    # Generate a grid of points with distance h between them
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    # Predict the function value for the whole gid
    kx = xx.ravel()
    ky = yy.ravel()

    list = []
    for i in range(len(kx)):
        list.append([kx[i], ky[i]])

    Z = pred_func(list)
    Z = Z.reshape(xx.shape)
    # Plot the contour and training examples
    # plt.contourf(xx, yy, Z, cmap=plt.cm.copper)
    y = Y.reshape(len(Y))
    # plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm)
    # plt.show()


def calculateAccuracy(y, set_Y, b):
    test_correct = []
    test_wrong = []
    train_correct = []
    train_wrong = []
    for i in range(len(set_Y)):
        if (b):
            print(i, " predict:", y[i][0], " actual: ", set_Y[i][0])

        if y[i][0] > 0.5 and set_Y[i][0] == 1:
            test_correct.append(y[i])
        elif y[i][0] > 0.5 and set_Y[i][0] == 0:
            test_wrong.append(y[i])
        elif y[i][0] <= 0.5 and set_Y[i][0] == 0:
            test_correct.append(y[i])
        else:
            test_wrong.append(y[i])
    # print (test_correct)
    # print (test_wrong)
    result = len(test_correct) / float(len(test_correct) + len(test_wrong))
    print(result)
    return result



# Create model
def multilayer_perceptron(x, weights, biases):
    # Hidden fully connected layer with 256 neurons
    x0=tf.nn.batch_normalization(x,mean=0.01, variance=1,offset=0,scale=1,variance_epsilon=0.001)
    layer_1 = tf.nn.relu(tf.add(tf.matmul(x0, weights['h1']), biases['b1']))
    # layer1_out = tf.sigmoid(layer_1)

    # Hidden fully connected layer with 256 neurons
    # layer_2 = tf.nn.relu(tf.add(tf.matmul(layer_1, weights['h2']), biases['b2']))
    # layer2_out = tf.sigmoid(layer_2)

    # Output fully connected layer with a neuron for each class
    out_layer = tf.matmul(layer_1, weights['out']) + biases['out']
    return tf.nn.sigmoid(out_layer)

def preprocess(train_set_X, train_set_Y, test_set_X, test_set_Y, train_path, test_path, read_next):
    # read training data
    # train_path = "./dataset/train[-1]_[-1]_[2, -4, -3, 5]_[-1]_[-4, -2, 3]_[4, 0, -5]_[3, 5]_[2, 1, -1]_[2, -1]_8624.csv"
    with open(train_path, 'r+') as csvfile:
        with open('./dataset/train_next.csv', 'w+') as file:
            i = 0
            spamreader = csv.reader(csvfile)
            writer = csv.writer(file)
            for row in spamreader:
                if (i < 140 or i > 160):
                    i += 1
                    continue
                else:
                    i += 1
                writer.writerow(row)
                # writer.writerow([1-float(row[0]),float(row[1])+0.01,float(row[2])+0.01])
        file.close()

    # read testing data
    # test_path = "./dataset/test[-1]_[-1]_[2, -4, -3, 5]_[-1]_[-4, -2, 3]_[4, 0, -5]_[3, 5]_[2, 1, -1]_[2, -1]_8624.csv"
    with open(test_path, 'r+') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            # print(row)
            l = [float(x) for x in row]
            # print(l)
            test_set_X.append(l[1:])
            if (row[0] == '1.0'):
                test_set_Y.append([1])
            else:
                test_set_Y.append([0])

    if read_next:
        train_path = './dataset/train_next.csv'
    # read training data
    if read_next:
        train_path='./dataset/train_next.csv'
    with open(train_path, 'r+') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if(len(row)==0):
                continue
            l = [float(x) for x in row]
            # print(l)
            train_set_X.append(l[1:])
            if (row[0] == '1.0'):
                train_set_Y.append([1])
            else:
                train_set_Y.append([0])

def quickSort(alist):
   quickSortHelper(alist,0,len(alist)-1)

def quickSortHelper(alist,first,last):
   if first<last:

       splitpoint = partition(alist,first,last)

       quickSortHelper(alist,first,splitpoint-1)
       quickSortHelper(alist,splitpoint+1,last)


def partition(alist,first,last):
   pivotvalue = alist[first]

   leftmark = first+1
   rightmark = last

   done = False
   while not done:

       while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
           leftmark = leftmark + 1

       while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
           rightmark = rightmark -1

       if rightmark < leftmark:
           done = True
       else:
           temp = alist[leftmark]
           alist[leftmark] = alist[rightmark]
           alist[rightmark] = temp

   temp = alist[first]
   alist[first] = alist[rightmark]
   alist[rightmark] = temp


   return rightmark


def data_partition(train_set_X, train_set_Y):
    label_0=[]
    label_1=[]
    for i in range(len(train_set_X)):
        if(train_set_Y[i][0]==0):
            label_0.append(train_set_X[i])
        elif(train_set_Y[i][0]==1):
            label_1.append(train_set_X[i]) 
    return label_0,label_1

def addPoints(number,distanceList,selectedList,pointer):
    pivot=0
    while pivot<number:
        if distanceList[pointer] in selectedList:
            pointer+=1

        # add large points
        
        else:
            selectedList.append(distanceList[pointer])
            pivot+=1
            pointer+=1

def data_partition_gradient(train_set_X, train_set_Y,gradient):
    label_0=[]
    label_0_gradient=[]
    label_1=[]
    label_1_gradient=[]
    for i in range(len(train_set_X)):
        if(train_set_Y[i][0]==0):
            label_0.append(train_set_X[i])
            label_0_gradient.append(gradient[i])
        elif(train_set_Y[i][0]==1):
            label_1.append(train_set_X[i]) 
            label_1_gradient.append(gradient[i])
    return label_0,label_1,label_0_gradient,label_1_gradient
