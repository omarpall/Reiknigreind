
# coding: utf-8

# In[3]:


import numpy as np
import random as r


def newDeck():
    freshDeck = []
    rank = ["A","2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suit = ["Hearts", "Spades", "Diamonds", "Clubs"]
    for j in range(len(suit)):
        for i in range(len(rank)):
            freshDeck.append((rank[i], suit[j]))       
    return freshDeck

def shuffle(deck):
    r.shuffle(deck)
    return deck

def getValue(hand):
    value = [0, "h"]
    for i in range(len(hand)):
        if(hand[i][0] == "A"):
            value[0] += 11
            value[1] = "s"
        elif(hand[i][0] == "10" or hand[i][0] == "J" or hand[i][0] == "Q" or hand[i][0] == "K"):
            value[0] += 10
        else:
            value[0] += int(hand[i][0])
    if(value[1] == "s" and value[0] < 32 and value[0] > 21):
        value[0] = value[0] - 10
        value[1] = "h"
    return value

def startGame():
    money = 100
    while(money > 0 and money < 200):
        print("Bank:", money)
        inn = input("Please enter bet: ")
        if(inn == "q"):
            return        
        bet = int(inn)
        money += startHand(bet)
    if(money <= 0):
        print("you lose sucker")
    elif(money >= 200):
        print("ez win")
        
    

def startHand(bet):
    #Initialiaze
    deck = newDeck()
    shuffle(deck)
    turn = True
    player = []
    dealer = []
    
    #Deal
    player.append(deck[0])
    del deck[0]
    dealer.append(deck[0])
    del deck[0]
    player.append(deck[0])
    del deck[0]
    playerTotal = getValue(player)
    dealerTotal = getValue(dealer)
    print("player:", player, "total:",playerTotal)
    print("dealer:", dealer,"total:",dealerTotal)
    
    #Player hits a blackjack
    if(playerTotal[0] == 21):
        dealer.append(deck[0])
        del deck[0]
        dealerTotal = getValue(dealer)
        print("dealer:", dealer,"total:",dealerTotal)
        if(dealerTotal[0] == 21):
            return 0
        else:
            "Print Player Blackjack"
            return int(1.5*bet)
    else:
        #Player turn
        while(turn):
            move = input("Please enter h or s: ")
            #Hit
            if(str(move) == "h"):
                player.append(deck[0])
                del deck[0]
                playerTotal = getValue(player)
                print("player:", player, "total:",playerTotal)
                if(playerTotal[0] > 21):
                    print("Busted")
                    return -bet     
            #Stand        
            elif(str(move) == "s"):
                turn = False
            else:
                print("Incorrect input")
        #Dealer turn
        while(dealerTotal[0] < 17):
            dealer.append(deck[0])
            del deck[0]
            dealerTotal = getValue(dealer)
            if(dealerTotal[0] > 21 and dealerTotal[1] == "s"):
                dealerTotal[0] = dealerTotal[0] - 10
                dealerTotal[1] = "h"
            print("dealer:", dealer,"total:",dealerTotal)
        if(dealerTotal[0] < 22):
            if(dealerTotal[0] > playerTotal[0]):
                print("Dealer wins")
                return -bet
            elif(dealerTotal[0] < playerTotal[0]):
                print("Player wins")
                return bet
            else:
                print("Tie")
                return 0
            
        else:
            print("Dealer bust")
            return bet


# In[7]:


startGame()


# In[ ]:




