import random
import numpy as np
import math

class Network:
    def __init__(self, numLayers, sizes): 
        self.layers = []
        self.sizes = sizes
        self.numLayers = numLayers

        for i in range(numLayers):
            self.layers.append(Layer(sizes[i])) #Creates the layers with their correct sizes

    def randomizeInitial(self): #Fills all of the layers weight and bias values with random numbers
        for i in range(1, self.numLayers): #Starts at 1 because the input layer does not have associated weight values
            tempLayer = self.layers[i] #Layer that the weigths are being creates for
            tempLayer2 = self.layers[i -1] #Layer before

            for j in range(tempLayer.numNodes):
                tempLayer.biases.append(random.uniform(-5,5)) #Random float between -5 and 5 for the weights
                temp = []
                for k in range(tempLayer2.numNodes):
                    temp.append(random.uniform(-5,5)) #Random float between -5 and 5 for the biases
                tempLayer.weights.append(temp)

    def run(self, startVal): #Takes an array of values equivalent in number to the input layer number of nodes  
        assert self.sizes[0] == len(startVal), Exception("Error: Invalid input size")

        values = startVal
        for i in range(1, self.numLayers): #Starts at 1 because the input layer does not have associated weight values
            values = self.layers[i].calculateNextValues(values)
        return(values)

    def mutate(self, startInt, endInt): #Mutates the values for weights, changes all weights by random numbers between start and end values (Interval)
        for i in range(1, self.numLayers):
            tempLayer = self.layers[i]
            tempLayer.change(startInt, endInt)

    def save(self, fileName): #Saves the network to a file
        with open(fileName, "a") as file:
                file.write(f"\nLayer Sizes: {self.sizes}\n")

        for i in range(1, self.numLayers):
            with open(fileName, "a") as file:
                file.write(f"\nLayer {i}\n")

            tempLayer = self.layers[i]
            tempLayer.saveLayer(fileName)

    def passLayers(self): #Returns the array of layers
        return(self.layers) 

    def copyWeights(self, outsideLayers): #Takes an array of layers and deep copies the weight values. Must be the same size of network or errors and broken
        for i in range(1, self.numLayers):
            tempLayer = self.layers[i]
            tempLayer.weights = outsideLayers[i].weights.copy()
            tempLayer.biases = outsideLayers[i].biases.copy()

        



class Layer:
    def __init__(self, numNuerons): 
        self.nodes = [] #node values
        self.numNodes = numNuerons
        self.weights = [] #2d array for 
        self.biases = []

    
    def calculateNextValues(self, values): #Does the matrix calculations and returns the layers values
        self.nodes = np.add(np.matmul(self.weights, values), self.biases)
        for i in range(len(self.nodes)):
            self.nodes[i] = 1 / (1 + math.exp(-1 * self.nodes[i])) #Sigmoid
        return(self.nodes)

    def change(self, startInt, endInt): #Changes the weights and biases by a random number whithin the interval
        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                self.weights[i][j] += random.uniform(startInt, endInt)

        for i in range(len(self.biases)):
            self.biases[i] += random.uniform(startInt, endInt)

    def saveLayer(self, fileName): #Saves the weights and biases to a file
        with open(fileName, "a") as file:
            file.write("Weights\n")
            file.write(f"{self.weights}")

            file.write("\nBiases\n")
            file.write(f"{self.biases}")
        
def test():

    test = Network(3, [2, 3, 2])
    test.randomizeInitial()
    val = test.run([1, 0])
    print("Weights for layer 1")
    for i in range(test.layers[1].numNodes):
        print(test.layers[1].nodes[i])

    print("Weights for layer 2")
    for i in range(test.layers[2].numNodes):
        print(test.layers[2].nodes[i])


    print("Output")
    for i in range(len(val)):
        print(val[i])


    val = test.run([1, 0])
    print("Weights for layer 1")
    for i in range(test.layers[1].numNodes):
        print(test.layers[1].nodes[i])

    print("Weights for layer 2")
    for i in range(test.layers[2].numNodes):
        print(test.layers[2].nodes[i])


    print("Output")
    for i in range(len(val)):
        print(val[i])