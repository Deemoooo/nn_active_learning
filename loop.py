from __future__ import print_function
import tensorflow as tf
import csv
import numpy as np
import random
import util
import math
# Parameters
learning_rate = 1
training_epochs = 100
display_step = 1
changing_rate=[1]

active_learning_iteration = 10

# Network Parameters
n_hidden_1 = 10  # 1st layer number of neurons
n_hidden_2 = 10  # 2nd layer number of neurons
n_input = 2  # MNIST data input (img shape: 28*28)
n_classes = 1  # MNIST total classes (0-9 digits)

random_seed = 0
random.seed(random_seed)
np.random.seed(random_seed)
tf.set_random_seed(random_seed)
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

train_set = []
test_set_X = []
test_set_Y = []
train_set_X = []
train_set_Y = []

util.preprocess(train_set_X, train_set_Y, test_set_X, test_set_Y)

# Construct model
logits = util.multilayer_perceptron(X)

# Define loss and optimizer
loss_op = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=logits, labels=Y))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
# optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
# Initializing the variables
train_op = optimizer.minimize(loss_op)
# Initializing the variables
init = tf.global_variables_initializer()

grads = tf.gradients(loss_op, weights["out"])
newgrads = tf.gradients(logits, X)

y = None

# ten times training
with tf.Session() as sess:
	sess.run(init)
	##data processing


	with open('test.csv', 'rt') as csvfile:
		spamreader = csv.reader(csvfile)
		for row in spamreader:
        # print(row)
			l = [0, 0]
			l[0] = float(row[1])
 			l[1] = float(row[2])
        # print(l)
 			test_set_X.append(l)
 			if (row[0] == '1.0'):
				test_set_Y.append([1])
			else:
				test_set_Y.append([0])

	with open('train_next.csv', 'rt') as csvfile:
		spamreader = csv.reader(csvfile)
		for row in spamreader:
			l = [0, 0]
			l[0] = float(row[1])
			l[1] = float(row[2])
        # print(l)
			train_set_X.append(l)
			if (row[0] == '1.0'):
				train_set_Y.append([1])
			else:
				train_set_Y.append([0])



	h1 = sess.run(weights["h1"])
	out = sess.run(weights["out"])

	print("h1", h1)
	print("out", out)

	g = sess.run(newgrads, feed_dict={X: train_set_X, Y: train_set_Y})
	##print(g)
	smallGradient_Unchanged=0.0
	smallGradient_total=0.0
	largeGradient_Unchanged=0.0
	largeGradient_total=0.0
	for i in range(active_learning_iteration):
		for epoch in range(training_epochs):
 			_, c = sess.run([train_op, loss_op], feed_dict={X: train_set_X, Y: train_set_Y})

			
			##print(g)
			##print("Epoch:", '%04d' % (epoch + 1), "cost={:.9f}".format(c))

		g = sess.run(newgrads, feed_dict={X: train_set_X, Y: train_set_Y})
		print (g)
		print(str(i)+"Turn Optimization Finished!\n")
		train_y = sess.run(logits, feed_dict={X: train_set_X})
		test_y = sess.run(logits, feed_dict={X: test_set_X})

		##print(len(train_y))
		##print(len(train_set_Y))
		util.calculateAccuracy(train_y, train_set_Y, False)
		util.calculateAccuracy(test_y, test_set_Y, False)
		new_train_set_X=[]
		new_train_set_Y=[]


		# smallGradient_Unchanged=0
		# smallGradient_total=0
		# largeGradient_Unchanged=0
		# largeGradient_total=0
		for k in changing_rate:

			for j in range(len(train_set_X)):
				tmpX1=train_set_X[j][0]+g[0][j][0]*k
				tmpX2=train_set_X[j][1]+g[0][j][1]*k

				if (g[0][j][0]>0):
					new_train_set_X.append([tmpX1,tmpX2])
					
					##if((tmpX1-12.5)*(tmpX1-12.5)+tmpX2*tmpX2<100 or (tmpX1+12.5)*(tmpX1+12.5)+tmpX2*tmpX2<100):
					if(tmpX2>tmpX1*tmpX1*tmpX1+tmpX1*tmpX1+tmpX1):
						
						new_train_set_Y.append([0])
					else:
						
						new_train_set_Y.append([1])


				##boundary remaining test
				##small gradient test
				# X1=train_set_X[j][0]
				# X2=train_set_X[j][1]
				# newY=train_set_Y[j][0]
				# ##print ("Y",newY)
				# if(g[0][j][0]<0.01):
					
				# 	smallGradient_total+=1
				# 	if(newY==0):
				# 		if(polynomialModel(tmpX1,tmpX2)):
				# 			smallGradient_Unchanged+=1
				# 	elif(newY==1):
				# 		if(not polynomialModel(tmpX1,tmpX2)):
				# 			smallGradient_Unchanged+=1


				# ##large gradient test
				# if(g[0][j][0]>0.1):
				# 	newtmpX1=train_set_X[j][0]-g[0][j][0]*k
				# 	newtmpX2=train_set_X[j][1]-g[0][j][1]*k

				# 	largeGradient_total+=1
				# 	if(newY==0):
				# 		if(polynomialModel(newtmpX1,newtmpX2)):
				# 			largeGradient_Unchanged+=1
				# 	elif(newY==1):
				# 		if(not polynomialModel(newtmpX1,newtmpX2)):
				# 			largeGradient_Unchanged+=1		





		train_set_X=train_set_X+new_train_set_X
		train_set_Y=train_set_Y+new_train_set_Y

		print(len(train_set_X))
		print(len(train_set_Y))

	# print(smallGradient_total)
	# print (smallGradient_Unchanged)
	# print(largeGradient_total)
	# print (largeGradient_Unchanged)	

	# print ("small gradient unchanged rate: ",smallGradient_Unchanged/smallGradient_total)
	# print ("large gradient unchanged rate: ", largeGradient_Unchanged/largeGradient_total)

