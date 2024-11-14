from network import *
from game import *

genCount = 0
oldGen = {}

with open("Test.txt", "w") as file:
    pass

while genCount < 20:
    pygame.init()
    currentGen = []
    if genCount == 0:
        #Creating 100 random networks
        for i in range(20):
            temp = Network(3, [6, 3, 2])
            temp.randomizeInitial()
            currentGen.append(temp)
    else:
        oldGen = dict(sorted(oldGen.items(), key=lambda item: -item[1]))
        print(oldGen)
        #Save best of the generation to a text file
        list(oldGen.keys())[0].save("Test.txt")
        #print(list(oldGen.values())[0])

        #Collect top five networks
        goodNetworks = []
        goodNetworks.append(list(oldGen.keys())[0])
        """
        for i in range(5):
            goodNetworks.append(list(oldGen.keys())[i])
        """
        temp = Network(3, [6, 3, 2])
        temp.copyWeights(goodNetworks[0].passLayers())
        currentGen.append(temp)

        for i in range(1, 20):
            temp = Network(3, [6, 3, 2])
            temp.copyWeights(goodNetworks[0].passLayers())
            temp.mutate(-i/100, i/100)
            currentGen.append(temp)





    oldGen = {}
    for network in currentGen:
        # pygame setup
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()
        running = True
        dt = 0
        ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        ball_dir = pygame.Vector2(300, 300)
        player_pos = pygame.Vector2(30, 30)
        globScore = 0

        array = [player_pos.x / 100, player_pos.y / 100, ball_pos.x / 100, ball_pos.y / 100, ball_dir.x / 100, ball_dir.y / 100]
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            direction = 0
            op1, op2 = network.run(array)
             
            if op1 > op2:
                direction = 1
            else:
                direction = -1


            array, running, globScore, player_pos, ball_pos, ball_dir = AIControlled(screen, player_pos, ball_pos, ball_dir, running, globScore, direction, clock)
        
        
        oldGen[network] = globScore


    genCount += 1
    pygame.quit()
    print(genCount)

