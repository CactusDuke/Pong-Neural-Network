from network import *
from game import *
from classes import *

def trainVisual(fileName):
    pygame.init()
    genCount = 0
    oldGen = {}

    numOfGenerations = 50
    numTrainiesWithinGen = 25

    with open(fileName, "w") as file: #Ensures that the file is empty
        pass

    while genCount < numOfGenerations: 
        currentGen = []
        if genCount == 0: #If it is the first generation
            #Creating the correct number of random networks
            for i in range(numTrainiesWithinGen):
                temp = Network(3, [6, 3, 2])
                temp.randomizeInitial()
                currentGen.append(temp)
        else:
            #Sorts the network value pairs from best to worst
            oldGen = dict(sorted(oldGen.items(), key=lambda item: -item[1]))
            #Save best of the generation to a text file
            with open(fileName, "a") as file:
                file.write(f"\n\nScore: {list(oldGen.values())[0]}") #Saves the score value
            list(oldGen.keys())[0].save(fileName) #Saves the network

            #Collect top three networks and their scores
            goodNetworks = []
            goodValue = []
            
            for i in range(3):
                goodNetworks.append(list(oldGen.keys())[i]) 

            for i in range(3): #Ensures that if the score is beneath 100 it is set to 100
                if list(oldGen.values())[i] < 100:
                    goodValue.append(100)
                else:
                    goodValue.append(list(oldGen.values())[i])
            
            #Places top three networks twice each
            for i in range(3):
                temp = Network(3, [6, 3, 2])
                temp.copyWeights(goodNetworks[i].passLayers())
                currentGen.append(temp)

                temp = Network(3, [6, 3, 2])
                temp.copyWeights(goodNetworks[i].passLayers())
                currentGen.append(temp)

            #Mutates of the best performing network to create a majority of the rest of the generation
            for i in range(6, numTrainiesWithinGen - 5):
                temp = Network(3, [6, 3, 2])
                temp.copyWeights(goodNetworks[0].passLayers())
                temp.mutate(-i / goodValue[0], i / goodValue[0]) #The better the network the less available room for mutation, allow more room for mutation as the trainie number gets larger
                currentGen.append(temp)
            #Last five networks are fully random
            for i in range(5):
                temp = Network(3, [6, 3, 2])
                temp.randomizeInitial()
                currentGen.append(temp)

        oldGen = {}
        #Running the networks
        #TODO See if it is possible to multithread
        trainieNum = 0
        genCount += 1

        for network in currentGen:
            trainieNum += 1
            #Initializiation for game
            screen = pygame.display.set_mode((1280, 720))
            clock = pygame.time.Clock()
            screenW = 1280
            screenH = 720
            running = True
            dt = 0
            ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
            ball_dir = pygame.Vector2(300, 300)
            player_pos = pygame.Vector2(30, 30)
            globScore = 0
            array = [player_pos.x / 100, player_pos.y / 100, ball_pos.x / 100, ball_pos.y / 100, ball_dir.x / 100, ball_dir.y / 100]

            #Game
            while running:
                direction = 0 #Resets direction
                op1, op2 = network.run(array) #Two outputs from network. Taken from info from last turn
                
                if op1 > op2: #If output 1 is greater than output 2 the rectangle goes up, otherwise it goes down
                    direction = 1 #Up
                else:
                    direction = -1 #Down

                #Updating game states
                array, running, globScore, player_pos, ball_pos, ball_dir = AIControlled(screenW, screenH, player_pos, ball_pos, ball_dir, running, globScore, direction, trainieNum, genCount, True, screen, clock)
            
            #Saves the networks score to a dictionary
            oldGen[network] = globScore
        
    pygame.quit()

#TODO Make this work better, functionally similar to above
def trainNoVisual(fileName):
    genCount = 0
    oldGen = {}

    with open(fileName, "w") as file: #Ensures that the file is empty
        pass

    while genCount < 100:
        currentGen = []
        if genCount == 0:
            #Creating 100 random networks
            for i in range(25):
                temp = Network(3, [6, 3, 2])
                temp.randomizeInitial()
                currentGen.append(temp)
        else:
            oldGen = dict(sorted(oldGen.items(), key=lambda item: -item[1]))
            print(oldGen.values())
            #Save best of the generation to a text file
            with open(fileName, "a") as file:
                file.write(f"\n\nScore: {list(oldGen.values())[0]}")
            list(oldGen.keys())[0].save(fileName)
            #print(list(oldGen.values())[0])

            #Collect top five networks
            goodNetworks = []
            goodValue = []
            
            for i in range(3):
                goodNetworks.append(list(oldGen.keys())[i])

            for i in range(3):
                if list(oldGen.values())[i] < 100:
                    goodValue.append(100)
                else:
                    goodValue.append(list(oldGen.values())[i])
            
            #Places top three twice each
            for i in range(3):
                temp = Network(3, [6, 3, 2])
                temp.copyWeights(goodNetworks[i].passLayers())
                currentGen.append(temp)

                temp = Network(3, [6, 3, 2])
                temp.copyWeights(goodNetworks[i].passLayers())
                currentGen.append(temp)

            #Ones based off best
            #TODO Change so that the changes are smaller the greater the score gets
            for i in range(6, 20):
                temp = Network(3, [6, 3, 2])
                temp.copyWeights(goodNetworks[0].passLayers())
                temp.mutate(-i / goodValue[0], i / goodValue[0])
                currentGen.append(temp)
            #Fully random
            for i in range(5):
                temp = Network(3, [6, 3, 2])
                temp.randomizeInitial()
                currentGen.append(temp)

        oldGen = {}
        #Running the networks
        #TODO See if it is possible to multithread
        trainieNum = 0
        genCount += 1

        for network in currentGen:
            screenW = 1280
            screenH = 720
            trainieNum += 1
            #Initializiation for game
            running = True
            dt = 0
            ball_pos = Vec2(screenW / 2, screenH / 2)
            ball_dir = Vec2(300, 300)
            player_pos = Vec2(30, 30)
            globScore = 0
            array = [player_pos.x / 100, player_pos.y / 100, ball_pos.x / 100, ball_pos.y / 100, ball_dir.x / 100, ball_dir.y / 100]

            #Game
            while running:
                direction = 0 #Resets direction
                op1, op2 = network.run(array) #Two outputs from network. Taken from info from last turn
                
                if op1 > op2: #If output 1 is greater than output 2 the rectangle goes up, otherwise it goes down
                    direction = 1 #Up
                else:
                    direction = -1 #Down

                #Updating game states
                array, running, globScore, player_pos, ball_pos, ball_dir = AIControlled(screenW, screenH, player_pos, ball_pos, ball_dir, running, globScore, direction, trainieNum, genCount, False)
            
            #Saves the networks score to a dictionary
            oldGen[network] = globScore
        print(genCount)

if __name__ == '__main__':
    trainNoVisual("train.txt") #Yeah this doesnt work. Maybe?
    #trainVisual("train.txt") #AHHH