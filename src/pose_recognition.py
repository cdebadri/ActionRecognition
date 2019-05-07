import tensorflow as tf
import numpy as np
import os

class pose_recognition:
    def __init__(self):
        self.graph = pose_recognition.load_graph(os.path.abspath(__file__ + '/../../models/lstm97.pb'))

    @staticmethod
    def load_graph(path):
        with tf.gfile.GFile(path, "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
        with tf.Graph().as_default() as graph:
            # The name var will prefix every op/nodes in your graph
            # Since we load everything in a new graph, this is not needed
            tf.import_graph_def(graph_def, name="prefix")
        return graph

    def inference(self, points):
        x = self.graph.get_tensor_by_name('prefix/input:0')
        y = self.graph.get_tensor_by_name('prefix/output:0')

        with tf.Session(graph=self.graph) as sess:
            output = sess.run(y, feed_dict={ x: points })
            # print(np.amax(output))
            return pose_recognition.action(np.argmax(output))

    @staticmethod
    def action(act):
        if act == 0:
            return 'jumping'
        elif act == 1:
            return 'jumping jacks'
        elif act == 2:
            return 'boxing'
        elif act == 3:
            return 'waving 2 hands'
        elif act == 4:
            return 'waving 1 hand'
        return 'clapping'
