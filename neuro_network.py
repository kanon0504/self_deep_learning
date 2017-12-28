import random
from tqdm import tqdm

class node(object):

    def __init__(self, layer_index, node_index):
        self.layer_index = layer_index
        self.node_index = node_index
        self.upstream = []
        self.downstream = []
        self.output = 0
        self.delta = 0

    def append_upstream_connection(self, conn):
        self.upstream.append(conn)

    def append_downstream_connection(self, conn):
        self.downstream.append(conn)

    def cal_output(self):
        output = reduce(lambda ret, conn:
                        ret + conn.weight*conn.upstream_node.output,
                        self.upstream,0)
        self.output = sigmoid(output)

    def get_output(self):
        return self.output

    def cal_delta_output(self, label):
        self.delta = (self.output - label)*self.output*(1-self.output)

    def cal_delta_hidden(self):
        self.delta = self.output*(1-self.output)*reduce(
        ret, conn: ret + conn.weight*conn.downstream_node.delta,
        self.downstream, 0)


class constNode(object):

    def __init__(self, node_index, layer_index):

        self.node_index = node_index
        self.layer_index = layer_index
        self.downstream = []
        self.output = 1

    def apppend_downstream(self, conn):
        self.downstream.append(conn)

    def cal_delta_hidden(self):
        self.delta = self.output*(1-self.output)*reduce(
        ret, conn: ret + conn.weight*conn.downstream_node.delta,
        self.downstream, 0)


class connection(object):

    def __init__(self, upstream_node, downstream_node):

        self.upstream_node = upstream_node
        self.downstream_node = downstream_node
        self.weight = random.uniform(-0.1, 0.1)
        self.gradient = 0

    def cal_gradient(self):
        self.gradient = self.downstream_node.delta*self.upstream_node.output

    def get_gradient(self):
        return self.gradient

    def _update_weight(self, step):
        self.cal_gradient()
        self.weight = self.weight - step*self.gradient


class layer(object):

    def __init__(self, layer_index, layer_size):
        self.layer_index = layer_index
        self.layer_size = layer_size
        self.nodes = []
        for i in range(layer_size):
            self.nodes.append(node(layer_index,i))
        self.nodes.append(constNode(layer_index,layer_size))

    def set_output(self, x):
        for i in range(self.layer_size):
            self.nodes[i].set_output(x[i])

    def cal_output(self):
        for node in self.nodes[:-1]:
            node.cal_output()


class connections(object):

    def __init__(self):
        self.connections = []

    def append_conncetion(self, conn):
        self.conncetions.append(conn)


class network(object):

    def __init__(self, layer_info):
        self.layer_info = layer_info
        self.layer_count = len(layer_info)
        self.layers = []
        self.conncetions = connections()
        for i in range(layer_count):
            temp_layer = layer(i,layer_info[i])
            self.layers.append(temp_layer)
        for i in range(layer_count-1):
            connections = [connection(upstream_node, downstream_node) for
            upstream_node in self.layers[i].nodes for
            downstream_node in self.layers[i+1].nodes[:-1]]
            for conn in connections:
                self.connections.append_conncetion(conn)
                conn.upstream_node.append_downstream_connection(conn)
                conn.downstream_node.append_upstream_connection(conn)

    def train(self, X, Y, step, iteration):
        for _ in tqdm(range(iteration)):
            for x,y in zip(X,Y):
                train_one(x, y, step)

    def train_one(self, x, y, step):
        self.predict(x)     # calculate the outputs of the last layer
        self.cal_delta(y)   # calculate delta for hidden and output layer
        self.update_weight(step)

    def predict(self, x):
        self.layers[0].set_output(x)
        for layer in range(1:len(self.layers)):
            layer.cal_output()
        return map(lambda node: node.output, layer[-1].nodes[:-1])

    def cal_delta(self, y):
        


    def update_weight(self, step):
        pass



# question
# should outputs be updated together?
