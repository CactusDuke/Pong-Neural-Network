import random
import numpy as np

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
            tempLayer.biases.append(random.uniform(-1,1))

            for j in range(tempLayer.numNodes):
                temp = []
                for k in range(tempLayer2.numNodes):
                    temp.append(random.uniform(-1,1))
                tempLayer.weights.append(temp)

    def run(self, startVal):
        values = startVal
        for i in range(1, self.numLayers):
            values = self.layers[i].calculateNextValues(values)
        return(values)


class Layer:
    def __init__(self, numNuerons): 
        self.nodes = [] #node values
        self.numNodes = numNuerons
        self.weights = [] #2d array for 
        self.biases = []

    
    def calculateNextValues(self, values):
        self.nodes = np.add(np.matmul(self.weights, values), self.biases)
        return(self.nodes)
        

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