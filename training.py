from network import *
from game import *

def trainVisual(fileName):
    genCount = 0
    oldGen = {}

    with open(fileName, "w") as file: #Ensures that the file is empty
        pass

    while genCount < 100:
        pygame.init()
        currentGen = []
        if genCount == 0:
            #Creating 100 random networks
            for i in range(25):
                temp = Network(3, [6, 3, 2])
                temp.randomizeInitial()
                currentGen.append(temp)
        else:
            oldGen = dict(sorted(oldGen.items(), key=lambda item: -item[1]))
            print(oldGen)
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
                if list(oldGen.values())[i] == 0:
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
                temp.mutate(-i / 100, i / 100)
                currentGen.append(temp)
            #Fully random
            for i in range(5):
                temp = Network(3, [6, 3, 2])
                temp.randomizeInitial()
                currentGen.append(temp)

        oldGen = {}
        #Running the networks
        #TODO See if it is possible to multithread
        for network in currentGen:
            #Initializiation for game
            screen = pygame.display.set_mode((1280, 720))
            clock = pygame.time.Clock()
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
                array, running, globScore, player_pos, ball_pos, ball_dir = AIControlled(screen, player_pos, ball_pos, ball_dir, running, globScore, direction, clock)
            
            #Saves the networks score to a dictionary
            oldGen[network] = globScore

        #Increases the generation count and prints it
        genCount += 1
        pygame.quit() #TODO try pushing pygame init and quit to outside the while statement
        print(genCount)


#TODO This will most certainly fail currently
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
            print(oldGen)
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
                if list(oldGen.values())[i] == 0:
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
                temp.mutate(-i / 100, i / 100)
                currentGen.append(temp)
            #Fully random
            for i in range(5):
                temp = Network(3, [6, 3, 2])
                temp.randomizeInitial()
                currentGen.append(temp)

        oldGen = {}
        #Running the networks
        #TODO See if it is possible to multithread
        for network in currentGen:
            #Initializiation for game
            screen = pygame.display.set_mode((1280, 720))
            clock = pygame.time.Clock()
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
                array, running, globScore, player_pos, ball_pos, ball_dir = AIControlled(screen, player_pos, ball_pos, ball_dir, running, globScore, direction, clock)
            
            #Saves the networks score to a dictionary
            oldGen[network] = globScore

        #Increases the generation count and prints it
        genCount += 1
        print(genCount)
