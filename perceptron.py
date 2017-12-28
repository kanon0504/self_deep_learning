class Perceptron(object):
    def __init__(self, nb_inputs, activator):
        self.nb_inputs = nb_inputs
        self.weights = [0.0 for _ in range(self.nb_inputs)]
        self.bias = 0.0
        self.activator = activator

    def __str__(self):
        return 'weights\t:%s\n bias\t:%f\n' % (self.weights, self.bias)

    def train(self, input_vec, label, learning_rate, iterations):
        for iters in range(iterations):
            self._one_iteration(input_vec, label, learning_rate)

    def predict(self, x):
        weighted_sum = reduce(lambda a, b: a + b,
                              map(lambda (x, w): x * w,
                                  zip(x, self.weights)), self.bias)
        return self.activator(weighted_sum)

    def _update_weight(self, output, x, y, learning_rate):
        delta = output - y
        self.weights = map(lambda (w, x): w - x * delta * learning_rate,
                           zip(self.weights, x))
        self.bias -= delta * learning_rate

    def _one_iteration(self, input_vec, label, learning_rate):

        for x, y in zip(input_vec, label):
            output = self.predict(x)
            self._update_weight(output, x, y, learning_rate)
        print self.__str__()




