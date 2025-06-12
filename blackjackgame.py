import random #random module
from collections import defaultdict #for the use of items with a list as its value
import time #for a smooth touch
import pygame 

#who doesnt love gambling 

#score stuff
wins = 0
loses = 0
streak = 0
blackjacks = 0

#dealers and users digital hand
DealersHand = {}
UsersHand = {}

#does the dealer/user have an ace? if so calculatings will be different
DealersAce = False
UsersAce = False

#does the user/dealer have blackjack? if so their winnings are priotitized
UserBlackjack = False
DealerBlackjack = False

#did the users best (soft hand) bust? if so they resort to their regular hand. if their regular hand busts they lose
UserBust = False
UserBestBust = False

#is it the dealers turn?
DealersTurn = False

#users hand and soft hand 
UsersValue = 0
UsersBest = 0

#dealers soft hand and regular  hand
DealersValue = 0
DealersBest = 0

#digital deck of cards (52 cards total)
CardDeck ={"♣️ Two": 2, "♣️ Three": 3, "♣️ Four": 4, "♣️ Five": 5, "♣️ Six": 6, "♣️ Seven": 7, "♣️ Eight": 8, "♣️ Nine": 9, "♣️ Ten": 10, "♣️ Jack": [10, "Pic"], "♣️ Queen": [10, "Pic"], "♣️ King": [10, "Pic"], "♣️ Ace": [1,11], 
           "♦️ Two": 2, "♦️ Three": 3, "♦️ Four": 4, "♦️ Five": 5, "♦️ Six": 6, "♦️ Seven": 7, "♦️ Eight": 8, "♦️ Nine": 9, "♦️ Ten": 10, "♦️ Jack": [10, "Pic"], "♦️ Queen": [10, "Pic"], "♦️ King": [10, "Pic"], "♦️ Ace": [1,11], 
           "♠️ Two": 2, "♠️ Three": 3, "♠️ Four": 4, "♠️ Five": 5, "♠️ Six": 6, "♠️ Seven": 7, "♠️ Eight": 8, "♠️ Nine": 9, "♠️ Ten": 10, "♠️ Jack": [10, "Pic"], "♠️ Queen": [10, "Pic"], "♠️ King": [10, "Pic"], "♠️ Ace": [1,11], 
           "♥️ Two": 2, "♥️ Three": 3, "♥️ Four": 4, "♥️ Five": 5, "♥️ Six": 6, "♥️ Seven": 7, "♥️ Eight": 8, "♥️ Nine": 9, "♥️ Ten": 10, "♥️ Jack": [10, "Pic"], "♥️ Queen": [10, "Pic"], "♥️ King": [10, "Pic"], "♥️ Ace": [1,11]}

def Rules():
    print()
    print("Rules:")
    print("All Blackjack games have vague and wierd dealer rules. Here are the rules that applies here:")
    print()
    print("1. Any picture cards (exluding 10 cards) that are and paired with an ACE is a blackjack.")
    print("2. Dealers MUST deal if their value is below 17, regardless if you have less than them")
    print("3. If you and the dealer are tied and both if your values are above 17, dealer will always win ties unless you have Blackjack.")
    print("4. If the dealers value or best value is above 17, they cannot deal anymore.")
    print()
    print("⭐ - Perfect Hand (21)")
    print("👑 - Blackjack! (ACE + Picture card)")
    print("❌ - Your best hand cannot be used (>21)")
    print("💥 - Bust!")
    print()
    print("Type X to start")
    choice = input().upper()
    if choice == "X":  
        DealCards()
        CalculateUsersValues()   
        PlayBlackjack()

def DealCards(): #Cards are being delt
    for _ in range(2):
        card, value = random.choice(list(CardDeck.items()))
        DealersHand.update({card: value})
        del CardDeck[card]

        # card, value = random.choice(list(CardDeck.items()))
        # UsersHand.update({card: value})
        # del CardDeck[card]
    
    #-------------------------------manual debugging below thanks chatgbt <3---------------------------------

    for card in list(CardDeck.keys()):
        if "Ace" in card:
            UsersHand[card] = CardDeck[card]
            del CardDeck[card]
            break

    for card in list(CardDeck.keys()):
        if "King" in card:
            UsersHand[card] = CardDeck[card]
            del CardDeck[card]
            break


def CalculateUsersValues(): #Values of all cards are calculated; only used once
    global UsersAce
    global UsersValue
    global UsersBest
    for card, value in UsersHand.items():
        if isinstance(value, list): #Checks if it is either an ACE or a picture card
            item = value[1]
            if item == 11: #Checks if it is an ACE, if so, UsersAce is true
                UsersAce = True
                UsersValue += value[0]
                UsersBest += value[1]
            elif item == "Pic": #Checks if it is a picture card
                UsersValue += value[0]
                UsersBest += value[0]
        else:
            UsersValue += value
            UsersBest += value

def DealerHit(): #the dealer hits
    global DealersValue
    global DealersBest
    global DealersAce

    card, value = random.choice(list(CardDeck.items()))
    DealersHand.update({card: value})
    del CardDeck[card]

    if isinstance(value, list): #Checks if it is either an ACE or a picture card
        item = value[1]
        if item == 11: #Checks if it is an ACE, if so, UsersAce is true
            DealersAce = True
            DealersValue += value[0]
            DealersBest += value[1]
        elif item == "Pic": #Checks if it is a picture card
            DealersValue += value[0]
            DealersBest += value[0]
    else:
        DealersValue += value
        DealersBest += value

def HitCard(): #the user hits
    global UsersValue
    global UsersBest
    global UsersAce

    card, value = random.choice(list(CardDeck.items()))
    UsersHand.update({card: value})
    del CardDeck[card]

    if isinstance(value, list): #Checks if it is either an ACE or a picture card
            item = value[1]
            if item == 11: #Checks if it is an ACE, if so, UsersAce is true
                UsersAce = True
                UsersValue += value[0]
                UsersBest += value[1]
            elif item == "Pic": #Checks if it is a picture card
                UsersValue += value[0]
                UsersBest += value[0]
    else:
        UsersValue += value
        UsersBest += value   
    PlayBlackjack()

def DealerCalculateCards(): #calculatrs the dealers hand
    global DealersAce
    global DealersValue
    global DealersBest
    for card, value in DealersHand.items():
        if isinstance(value, list): #Checks if it is either an ACE or a picture card
            item = value[1]
            if item == 11: #Checks if it is an ACE, if so, UsersAce is true
                DealersAce = True
                DealersValue += value[0]
                DealersBest += value[1]
            elif item == "Pic": #Checks if it is a picture card
                DealersValue += value[0]
                DealersBest += value[0]
        else:
            DealersValue += value
            DealersBest += value 

def DealerNowShallDeal(): #starts the dealer to deal
    if UserBlackjack == True:
        time.sleep(2)
        print()
        print("You got a Blackjack!")
        print("Standing. The dealer reveals his folded card")
        print()
        time.sleep(2)
    BlackjackDisplay = ""
    print()
    if UserBlackjack == False:
        print("Standing. The dealer reveals his folded card")
    print("Dealers Hand: ")
    if DealerBlackjack == True:
        BlackjackDisplay = "👑"
    for card, value in DealersHand.items():
        print(f"\"{card}\": {value}{BlackjackDisplay}")
    DealerCalculateCards()
    if DealersAce == True:
        print(f"Dealers Possible Values: {DealersValue}, {DealersBest}")
    else:
        print(f"Dealers Value: {DealersValue}")
    if DealerBlackjack == True:
        time.sleep(1.5)
        print()
        print("Dealer has a Blackjack.")
    time.sleep(1.5)
    PlayBlackjack()

def anotherRound(): #play again?
    global DealersAce
    global UsersAce
    global UserBlackjack
    global DealerBlackjack
    global UserBust
    global DealersTurn
    global UsersValue
    global UsersBest
    global DealersValue
    global DealersBest
    global wins
    global loses
    global UsersBestBust

    print()
    print(f"👑 Wins: {wins}")
    print(f"💔 Loses: {loses}")
    print(f"🔥 Streak: {streak}")
    print(f"🃏 Blackjacks: {blackjacks}")
    print()
    print("Play again? Type Y")
    if input().upper() == "Y":
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        for card in list(DealersHand.keys()):
            CardDeck.update({card: DealersHand[card]})
            del DealersHand[card]

        for card in list(UsersHand.keys()):
            CardDeck.update({card: UsersHand[card]})
            del UsersHand[card]
        DealersAce = False
        UsersAce = False
        UserBlackjack = False
        DealerBlackjack = False
        UserBust = False
        DealersTurn = False
        UsersBestBust = False
        UsersValue = 0
        UsersBest = 0
        DealersValue = 0
        DealersBest = 0
        DealCards()
        CalculateUsersValues()
        PlayBlackjack()
        

def WhatWouldYouDo(): #choose
    print("H to hit")
    print("S to stand")

def AskUser():
    global DealersTurn
    UserChoice = input().upper()
    if UserChoice == "H":
        HitCard()
    elif UserChoice == "S":
        DealersTurn = True
        DealerNowShallDeal()
    else:
        print("Invalid input, try again")
        AskUser()
        print()

def blackjackcheck(): #checks if user or dealer has blackjack
    global UserBlackjack
    global DealerBlackjack

    dealerHasAce = False
    dealerHas10 = False

    userHasAce = False
    userHas10 = False
    if len(DealersHand.items()) == 2: #check dealers blackjack
        for card, value in DealersHand.items():
            if isinstance(value, list):
                item = value[0]
                if (item == 10):
                    dealerHas10 = True
            if isinstance(value, list):
                item = value[1]
                if (item == 11):
                    dealerHasAce = True

    if len(UsersHand.items()) == 2: #checkusersblackjack
        for card, value in UsersHand.items():
            if isinstance(value, list):
                item = value[0]
                if (item == 10):
                    userHas10 = True
            if isinstance(value, list):
                item = value[1]
                if (item == 11):
                    userHasAce = True

    if userHasAce == True and userHas10 == True:
        UserBlackjack = True
    if dealerHasAce == True and dealerHas10 == True:
        DealerBlackjack = True

def CheckValues(check, x): #score
    global wins
    global loses
    global streak
    global blackjacks
    global UserBlackjack
    print()
    print()
    print(check)
    if x == "w":
        wins += 1
        streak += 1
    if x == "l":
        loses += 1
        streak = 0
    if x == "w" and UserBlackjack == True:
        blackjacks += 1
    time.sleep(1.5)
    anotherRound()
    
    
def DealersCheck(): #checks for (hopefully) all possible values if dealer wins or loses. this was fun to make..
    global DealersAce
    global UsersAce
    global UserBestBust

    NoDisplay1 = ""
    NoDisplay2 = ""
    BlackjackDisplay = ""
    print()
    print("-------------------------------------------------")
    print("🕴️ Dealers Hand:🕴️")
    if DealersTurn == True:
        if DealerBlackjack == True:
            BlackjackDisplay = "👑"
        for card, value in DealersHand.items():
            print(f"\"{card}\": {value}{BlackjackDisplay}")
        if DealersValue > 21:
            NoDisplay1 = "💥"
        if DealersAce == True:
            if DealersBest > 21:
                NoDisplay2 = "❌"
            print()
            print(f"Dealers Possible Values: {DealersValue}{NoDisplay1}, {DealersBest}{NoDisplay2}")
            if DealersBest >= 17:
                print()
                print("🛑17 Rule! Dealer cannot deal anymore🛑")
                print()
        elif DealersAce == False:
            if DealersValue >= 17:
                print()
                print("🛑17 Rule! Dealer cannot deal anymore🛑")
            print()
            print(f"Dealers Value: {DealersValue}{NoDisplay1}")

# :)
        if UsersAce == True and DealersAce == True:
            if DealersBest >= 17 and DealersBest <= 21: #dealers best can be used
                if UsersBest <= 21: #Users best can be used
                    if UsersBest == DealersBest: #User best and Dealer best
                        if UserBlackjack == True and DealerBlackjack == True:
                            check = "Push! It's a tie. You both have Blackjack."
                            x = "p"
                            CheckValues(check, x)
                        if UserBlackjack == True and DealerBlackjack == False:
                            check = "You win! You have Blackjack!"
                            x = "w"
                            CheckValues(check, x)
                        if UserBlackjack == False and DealerBlackjack == True:
                            check = "Dealer wins. Dealer has Blackjack."
                            x = "l"
                            CheckValues(check, x)
                        else:
                            check = "Dealer wins. Dealer wins by tie."
                            x = "l"
                            CheckValues(check, x)
                    elif DealersBest > UsersBest:
                        check = "Dealer wins. Dealers value is greater."
                        x = "l"
                        CheckValues(check, x)
                    elif DealersBest < UsersBest:
                        check = "You win!. Your value is greater."
                        x = "w"
                        CheckValues(check, x)
                else: #Dealers best can be used but users best cannot.
                    if DealersBest == UsersValue:
                        if DealerBlackjack == True:
                            check = "Dealer wins. Dealer has Blackjack."
                            x = "l"
                            CheckValues(check, x)
                        else:
                            check = "Dealer wins. Dealer wins by tie."
                            x = "l"
                            CheckValues(check, x)
                    if DealersBest > UsersValue:
                        check = "Dealer wins. Dealers value is greater."
                        x = "l"
                        CheckValues(check, x)
                    if DealersBest < UsersValue:
                        check = "You win! Your value is greater!"
                        x = "w"
                        CheckValues(check, x)
            elif DealersBest > 21 and UsersBest <= 21: #User Best: yes; Dealerbest: no, dealer value
                if UsersBest == DealersValue:
                    if UserBlackjack == True:
                        check = "You win! You have Blackjack!"
                        x = "w"
                        CheckValues(check, x)
                    else:
                        check = "Dealer wins. Dealer wins by tie."
                        x = "l"
                        CheckValues(check, x)
                elif UsersBest > DealersValue:
                    check = "You win!. Your value is greater."
                    x = "w"
                    CheckValues(check, x)
                elif UsersBest < DealersValue:
                    check = "Dealer wins. Dealers value is greater."
                    x = "l"
                    CheckValues(check, x)
            elif UsersBest > 21 and DealersBest > 21: #neither best can be used, determined by values.
                if UsersValue == DealersValue:
                    check = "Dealer wins. Dealer wins by tie."
                    x = "l"
                    CheckValues(check, x)
                elif UsersValue > DealersValue:
                    check = "You win!. Your value is greater."
                    x = "w"
                    CheckValues(check, x)
                elif UsersValue < DealersValue:
                    check = "Dealer wins. Dealers value is greater."
                    x = "l"
                    CheckValues(check, x)
            elif DealersBest < 17: #hit if below 17
                time.sleep(1.5)
                DealerHit()
                PlayBlackjack()
    #----------------------------------------#
    #DEALER HAS ACE BUT USER DOES NOT
    #----------------------------------------#
        if UsersAce == False and DealersAce == True:
            if DealersBest >= 17 and DealersBest <= 21: #dealers best can be used
                if DealersBest == UsersValue: #User best and Dealer best
                    if DealerBlackjack == True:
                        check = "Dealer wins. Dealer has Blackjack."
                        x = "l"
                        CheckValues(check, x)
                    else:
                        check = "Dealer wins. Dealer wins by tie."
                        x = "l"
                        CheckValues(check, x)
                elif DealersBest > UsersValue:
                    check = "Dealer wins. Dealers value is greater."
                    x = "l"
                    CheckValues(check, x)
                elif DealersBest < UsersValue:
                    check = "You win! Your value is greater!"
                    x = "w"
                    CheckValues(check, x)
            elif DealersBest > 21:
                if UsersValue == DealersValue:
                    check = "Dealer wins. Dealer wins by tie."
                    x = "l"
                    CheckValues(check, x)
                elif UsersValue > DealersValue:
                    check = "You win!. Your value is greater."
                    x = "w"
                    CheckValues(check, x)
                elif UsersValue < DealersValue:
                    check = "You lose. Dealers value is greater."
                    x = "w"
                    CheckValues(check, x)
            elif DealersBest < 17: #hit if below 17
                time.sleep(1.5)
                DealerHit()
                PlayBlackjack()
    #----------------------------------------#
    #USER HAS ACE BUT DEALER DOES NOT
    #----------------------------------------#
        if UsersAce == True and DealersAce == False:
            if DealersValue >= 17 and DealersValue <= 21: #Dealers value can be used
                if UsersBest <= 21: #Users best can be used
                    if UsersBest == DealersValue: #User best and Dealer best
                        if UserBlackjack == True:
                            check = "You win! You have Blackjack!"
                            x = "w"
                            CheckValues(check, x)
                        else:
                            check = "Dealer wins. Dealer wins by tie."
                            x = "l"
                            CheckValues(check, x)
                    elif UsersBest > DealersValue:
                        check = "You win! Your value is greater!"
                        x = "w"
                        CheckValues(check, x)
                    elif UsersBest < DealersValue:
                        check = "You lose. Dealers value is greater."
                        x = "l"
                        CheckValues(check, x)
                elif UsersBest > 21: #users ace cant be used
                    if UsersValue == DealersValue:
                        check = "Dealer wins. Dealer wins by tie."
                        x = "l"
                        CheckValues(check, x)
                    elif UsersValue > DealersValue:
                        check = "You win!. Your value is greater."
                        x = "w"
                        CheckValues(check, x)
                    elif UsersValue < DealersValue:
                        check = "You lose. Dealers value is greater."
                        x = "l"
                        CheckValues(check, x)
            elif DealersValue > 21: #Dealer has busted
                check = "You win!. Dealer has busted!."
                x = "w"
                CheckValues(check, x)
            elif DealersValue < 17: #hit if below 17
                time.sleep(1.5)
                DealerHit()
                PlayBlackjack()
    #----------------------------------------#
    #NEITHER HAS ACE, RELY ON VALUES
    #----------------------------------------#
        if UsersAce == False and DealersAce == False:
            if DealersValue >= 17: #will the dealer hit?
                if DealersValue <= 21:
                    if UsersValue == DealersValue:
                        check = "Dealer wins. Dealer wins by tie."
                        x = "l"
                        CheckValues(check, x)
                    elif UsersValue > DealersValue:
                        check = "You win!. Your value is greater."
                        x = "w"
                        CheckValues(check, x)
                    elif UsersValue < DealersValue:
                        check = "You lose. Dealers value is greater."
                        x = "l"
                        CheckValues(check, x)
                elif DealersValue > 21: #dealer bust
                    check = "You win!. Dealer has busted!."
                    x = "w"
                    CheckValues(check, x)
            elif DealersValue < 17:
                time.sleep(1.5)
                DealerHit()
                PlayBlackjack()
    else: #if it is not the dealers turn.
        card, value = list(DealersHand.items())[0]
        print(f"\"{card}\": {value}")
        print("FOLDED CARD: ???")
        print("Dealers possible value(s): ???")
        print()
#after a while there was a pattern and it got easier


def PlayBlackjack(): #What is displayed to the user; starts the game
    global UsersAce
    global UserBust
    global DealersTurn
    global UserBestBust

    NoDisplay1 = ""
    NoDisplay2 = ""
    SpecialDisplay1 = ""
    SpecialDisplay2 = ""
    DealersCheck()
    print()
    print("🤠Your Hand:🤠")
    blackjackcheck()
    for card, value in UsersHand.items():
        print(f"\"{card}\": {value}")
    if UsersValue == 21:
        SpecialDisplay1 = "⭐"
    if UsersBest == 21:
        if UserBlackjack == False:
            SpecialDisplay2 = "⭐"
        else:
            SpecialDisplay2 = "👑"
    if UsersValue > 21:
        NoDisplay1 = "💥"
        UserBust = True
    if UsersAce == True:
        if UsersBest > 21:
            NoDisplay2 = "❌"
            UserBestBust = True
        print(f"Your Possible Values: {UsersValue}{NoDisplay1}{SpecialDisplay1}, {UsersBest}{NoDisplay2}{SpecialDisplay2}")
    else:
        print(f"Your Value: {UsersValue}{NoDisplay1}{SpecialDisplay1}")
    #CheckCards()
    if UserBlackjack == True:
        DealersTurn = True
        DealerNowShallDeal()
    print()
    if UserBust == True:
        time.sleep(1.5)
        check = "Bust! Dealer wins."
        x = "l"
        CheckValues(check, x)

    else:
        WhatWouldYouDo()
        AskUser()

def StartTheGame():
    choice = input().upper()
    if choice == "X":    
        DealCards()
        CalculateUsersValues()   
        PlayBlackjack()
    elif choice == "R":    
        Rules()
    else:
        print("Type the key X to start")
        StartTheGame()
print()
print()
print("Welcome to Python Blackjack!")
print()
print("Type S to stand")
print("Type H to hit")
print()
print("DRAG UP THE SCREEN TO THE TOP FOR BEST EXPERIENCE")
print()
print()
print("RECOMMENDED: Type R for rules")
print("Type X to play!")
StartTheGame()