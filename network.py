import random
import numpy as np
import math

class Network:
    def __init__(self, numLayers, sizes): 
        self.layers = []
        self.numLayers = numLayers

        for i in range(numLayers):
            self.layers.append(Layer(sizes[i]))

    def randomizeInitial(self):
        for i in range(1, self.numLayers):
            tempLayer = self.layers[i]
            tempLayer2 = self.layers[i -1]

            for j in range(tempLayer.numNodes):
                tempLayer.biases.append(random.uniform(-5,5))
                temp = []
                for k in range(tempLayer2.numNodes):
                    temp.append(random.uniform(-5,5))
                tempLayer.weights.append(temp)

    def run(self, startVal):
        values = startVal
        for i in range(1, self.numLayers):
            values = self.layers[i].calculateNextValues(values)
        return(values)

    def mutate(self, startInt, endInt):
        for i in range(1, self.numLayers):
            tempLayer = self.layers[i]
            tempLayer.change(startInt, endInt)

    def save(self, fileName):        
        for i in range(1, self.numLayers):
            with open(fileName, "a") as file:
                file.write(f"\nLayer {i}\n")

            tempLayer = self.layers[i]
            tempLayer.saveLayer(fileName)

    def passLayers(self):
        return(self.layers)

    def copyWeights(self, outsideLayers):
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

    
    def calculateNextValues(self, values):
        self.nodes = np.add(np.matmul(self.weights, values), self.biases)
        for i in range(len(self.nodes)):
            self.nodes[i] = 1 / (1 + math.exp(-1 * self.nodes[i]))
        return(self.nodes)

    def change(self, startInt, endInt):
        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                self.weights[i][j] += random.uniform(startInt, endInt)

        for i in range(len(self.biases)):
            self.biases[i] += random.uniform(startInt, endInt)

    def saveLayer(self, fileName):
        with open(fileName, "a") as file:
            file.write("Weights\n")
            file.write(f"{self.weights}")
            """
            file.write("[")
            for i in range(len(self.weights)):
                file.write("[")
                for j in range(len(self.weights[i])):
                    file.write(f"{self.weights[i][j]}, ")
                file.write("], ")
            file.write("]")
            """

            file.write("\nBiases\n")
            file.write(f"{self.biases}")
            """
            file.write("[")
            for i in range(len(self.biases)):
                file.write(f"{self.biases[i]}, ")
            file.write("]")
            """
        
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