import random
import numpy as np
import matplotlib.pyplot as plt

def draw():
    rank = random.randint(1, 10)
    if(random.randint(1, 3) == 1):
        color = -1
    else:
        color = 1
    card = rank * color
    return card

def initializeEnvironment():
    #First card for dealer and player
    player = random.randint(1, 10)
    dealer = random.randint(1, 10)
    return (player, dealer)


#Take in inputs state s and action a
#Return state s', boolean done and reward r
def step(s, a):
    player = s[0]
    dealer = s[1]

    #Player's turn
    #print("Player",player,"Dealer",dealer, "Player turn, action:", a)
    if(a == 1):
        player += draw()
        #print("Player",player,"Dealer",dealer, "Player has drawn, action:", a)
        if(player > 21 or player < 1):
            return ((player, dealer), True, -1)
        else:
            return ((player, dealer), False, 0)
    #Dealer's turn
    elif(a == 0):
        while(True): 
            #print("Player",player,"Dealer",dealer, "Dealer turn")       
            dealer += draw()
          
            if(dealer > 21 or dealer < 1):
                #print("Player",player,"Dealer",dealer, "Dealer busts")  
                return (s, True, 1) 
            elif(dealer >= 17):
                if(dealer > player):
                    #print("Player",player,"Dealer",dealer, "Dealer wins")  
                    return (s, True, -1)
                elif(dealer < player):
                    #print("Player",player,"Dealer",dealer, "Player loses")  
                    return (s, True, 1)
                elif(dealer == player):
                    #print("Player",player,"Dealer",dealer, "Tie")  
                    return (s, True, 0)

playerSpace = [i+1 for i in range(21)]
dealerSpace = [i+1 for i in range(10)]
stateSpace = []
for hand in playerSpace:
    for card in dealerSpace:
        stateSpace.append((hand, card)) 


values = np.zeros((21, 10, 2)) #Values for all state-action pairs
Nsa = np.zeros((21, 10, 2)) #Number of times action a has been selected from state s
Ns = np.zeros((21, 10)) #Number of times state s has been visited

targetPolicy = {}
for state in stateSpace:
    valueOfState = values[state[0]-1][state[1]-1]
    bestAction = np.random.choice(np.where(valueOfState == valueOfState.max())[0])     
    targetPolicy[state] = bestAction


N0 = 100
numEpisodes = 1000000
for i in range(numEpisodes):
    if(i % (numEpisodes / 10) == 0):
        print("Done:", 100 * (i / numEpisodes))
    memory = []
    behaviourPolicy = {}
    for s in stateSpace:
        epsilon = N0 / (N0 + Ns[s[0]-1][s[1]-1])
        if(random.random() < 1 - epsilon):
            behaviourPolicy[s] = targetPolicy[s]
        else:
            if(random.random() < 0.5):
                behaviourPolicy[s] = 0
            else:
                behaviourPolicy[s] = 1
    state = initializeEnvironment()
    done = False
    while not done:
        action = behaviourPolicy[state]
        state_, done, reward = step(state, action)
        memory.append((state[0], state[1], action, reward))
        state = state_
    
    G = 0

    for player, dealer, action, reward in reversed(memory):
        G += reward
        #print("memory", player, dealer, action, reward)
        state = (player, dealer)
        #print("state",state)
        Nsa[player-1][dealer-1][action] += 1
        #print("value before", values[player-1][dealer-1][action])
        values[player-1][dealer-1][action] += ((1 /  Nsa[player-1][dealer-1][action]) * (G - values[player-1][dealer-1][action]))
        #print("N", Nsa[player-1][dealer-1][action], "value after",values[player-1][dealer-1][action],"G", G, "action", action, "fyrra", (1 /  Nsa[player-1][dealer-1][action]), "seinna", (G - values[player-1][dealer-1][action]))
        bestAction = np.random.choice(np.where(values[player-1][dealer-1] == values[player-1][dealer-1].max())[0]) 
        targetPolicy[state] = bestAction
        if(action != targetPolicy[state]):
            break
        

numEpisodes = 10000
rewards = np.zeros(numEpisodes)
totalReward = 0
wins = 0
losses = 0
draws = 0
print('getting ready to test target policy')   
for i in range(numEpisodes):
    state = initializeEnvironment()
    done = False
    while not done:
        action = behaviourPolicy[state]
        state_, done, reward = step(state, action)
        state = state_
    totalReward += reward
    rewards[i] = totalReward

    if reward >= 1:
        wins += 1
    elif reward == 0:
        draws += 1
    elif reward == -1:
        losses += 1

wins /= numEpisodes
losses /= numEpisodes
draws /= numEpisodes
print(values)
print('win rate', wins, 'loss rate', losses, 'draw rate', draws)
plt.plot(rewards)
plt.show()  


