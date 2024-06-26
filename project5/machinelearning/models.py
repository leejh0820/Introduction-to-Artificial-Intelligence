import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        
        ###########
        return nn.DotProduct(self.w, x)
        "*** YOUR CODE HERE ***"

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        
        #######
        pred = self.run(x)
        pred = nn.as_scalar(pred)
        if pred < 0:
            return -1 
        else:
            return 1
        
        "*** YOUR CODE HERE ***"

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        #y: <Constant ....>
        #x: <Constant ....>
        lr = 1 # 0.1 # 0.01
        batch_size = 1
        epoch = 100
        for _ in range(epoch):
            for x, y in dataset.iterate_once(batch_size):
                pred = self.get_prediction(x)
                y_scalar = nn.as_scalar(y)
                if pred - y_scalar != 0:
                    direction = y_scalar*x.data
                    # import pdb; pdb.set_trace()
                    # update(Constant, )
                    self.w.update(nn.Constant(direction), lr)
        ###############
        "*** YOUR CODE HERE ***"
        
def Linear(x, weight, bias=None):
            linear = nn.Linear(x, weight)
            # self.w1.data.shape
            if bias:
                return nn.AddBias(linear, bias)
            else:
                return linear
            
class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.lr = 0.1
        self.batch_size = 10
        
        self.w1 = nn.Parameter(1, 128)
        self.w2 = nn.Parameter(128, 128)
        self.w3 = nn.Parameter(128, 1)
        
        self.b1 = nn.Parameter(1, 128)
        self.b2 = nn.Parameter(1, 128)
        self.b3 = nn.Parameter(1, 1)
        
        self.parameters = [self.w1, self.b1, 
                           self.w2, self.b2, 
                           self.w3, self.b3]
    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        x = nn.ReLU(Linear(x, self.w1, self.b1))
        x = nn.ReLU(Linear(x, self.w2, self.b2))
        x = Linear(x, self.w3, self.b3)
        
        return x
        
        "*** YOUR CODE HERE ***"

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        
        ############
        # SquareLoss(Constant, Constant)
        return nn.SquareLoss(self.run(x), y)
        "*** YOUR CODE HERE ***"

    def train(self, dataset):
        """
        Trains the model.
        """
        
        #############
        # get loss lower than 0.02 
        # epoch = 1000
        # for _ in range(epoch):
        
        loss = 1000
        while loss > 0.001:
            for x, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(x, y)
                gradient = nn.gradients(loss, self.parameters)
                loss = nn.as_scalar(loss)
                for param, grad in zip(self.parameters, gradient):
                    param.update(grad, -self.lr)
        "*** YOUR CODE HERE ***"

class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.lr = 0.1
        self.batch_size = 100
        
        self.w1 = nn.Parameter(784, 128)
        self.w2 = nn.Parameter(128, 128)
        self.w3 = nn.Parameter(128, 10)
        
        self.b1 = nn.Parameter(1, 128)
        self.b2 = nn.Parameter(1, 128)
        self.b3 = nn.Parameter(1, 10)
        
        self.parameters = [self.w1, self.b1, 
                           self.w2, self.b2, 
                           self.w3, self.b3]

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        x = nn.ReLU(Linear(x, self.w1, self.b1))
        x = nn.ReLU(Linear(x, self.w2, self.b2))
        x = Linear(x, self.w3, self.b3)
        
        return x
        "*** YOUR CODE HERE ***"

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        epoch = 10
        # import pdb; pdb.set_trace()
        """
        valid = 0
        for _ in range(epoch):
            for x, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(x, y)
                valid = dataset.get_validation_accuracy()
                gradient = nn.gradients(loss, self.parameters)
                # if valid < valid_:
                for param, grad in zip(self.parameters, gradient):
                    param.update(grad, -self.lr)
                #         valid = valid_
        """
                
        val_loss = 0
        while val_loss < 0.975:
            for x, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(x, y)
                gradient = nn.gradients(loss, self.parameters)
                for param, grad in zip(self.parameters, gradient):
                    param.update(grad, -self.lr)
            val_loss = dataset.get_validation_accuracy()
        "*** YOUR CODE HERE ***"
        
def RNN(linear1, linear2, bias=None):
    if bias:
        return nn.AddBias(nn.Add(linear1, linear2), bias)
    else:
        return nn.Add(linear1, linear2)
            
class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        output = len(self.languages)
        
        self.lr = 0.1
        self.batch_size = 50
        
        self.w1 = nn.Parameter(self.num_chars, 128)
        self.w2 = nn.Parameter(128, 128)
        self.w3 = nn.Parameter(128, 128)
        self.w4 = nn.Parameter(128, output)
        
        self.b1 = nn.Parameter(1, 128)
        self.b2 = nn.Parameter(1, 128)
        self.b3 = nn.Parameter(1, 128)
        self.b4 = nn.Parameter(1, output)
        
        self.parameters = [self.w1, self.b1, 
                           self.w2, self.b2, 
                           self.w3, self.b3,
                           self.w4, self.b4]
    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        x = nn.ReLU(Linear(xs[0], self.w1, self.b1))
        
        for i, ch in enumerate(xs[1:]):
            x = nn.ReLU(RNN(Linear(ch, self.w1), 
                            Linear(x, self.w2, self.b2), 
                            self.b2))
            x = nn.ReLU(RNN(Linear(xs[i], self.w1), 
                            Linear(x, self.w3, self.b3), 
                            self.b3))
            
        # import pdb; pdb.set_trace()
        x = Linear(x, self.w4, self.b4)
        
        return x
    

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(xs), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        val_loss = 0
        while val_loss < 0.89:
        # for _ in range(1000):
            for x, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(x, y)
                gradient = nn.gradients(loss, self.parameters)
                for param, grad in zip(self.parameters, gradient):
                    param.update(grad, -self.lr)
            val_loss = dataset.get_validation_accuracy()
