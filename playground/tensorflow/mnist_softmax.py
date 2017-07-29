import argparse
import sys

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

FLAGS = None


def main(_):
    #Import data
    mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

    X = tf.placeholder(tf.float32, [None, 784])
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros(10))

    Y = tf.nn.softmax(tf.matmul(X, W) + b)

    Y_ = tf.placeholder(tf.float32, [None, 10])
    cross_entropy = -tf.reduce_sum(Y_ * tf.log(Y))

    optimizer = tf.train.GradientDescentOptimizer(0.003)
    model = optimizer.minimize(cross_entropy)

    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)

    for i in range(1000):
        # load batch of images and correct answers
        batch_X, batch_Y = mnist.train.next_batch(100)
        train_data = {X: batch_X, Y_: batch_Y}

        # train
        sess.run(model, feed_dict=train_data)

        # Test trained model
        correct_prediction = tf.equal(tf.argmax(Y, 1), tf.argmax(Y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        # accuracy and entropy for train data
        acc, entropy = sess.run([accuracy, cross_entropy], feed_dict=train_data)
        print(str(i) + ": **** epoch " + str(i*100//mnist.train.images.shape[0]+1) + " **** train accuracy:" + str(acc) + " train loss: " + str(entropy))

        # accuracy and entropy for train data
        acc, entropy = sess.run([accuracy, cross_entropy], feed_dict={X: mnist.test.images, Y_: mnist.test.labels})
        print(str(i) + ": **** epoch " + str(i*100//mnist.train.images.shape[0]+1) + " **** test accuracy:" + str(acc) + " test loss: " + str(entropy))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_dir', type=str, default='/tmp/tensorflow/mnist/input_data',
                      help='Directory for storing input data')
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)