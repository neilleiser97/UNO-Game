#!/usr/bin/env python3
"""
Assignment 2 - UNO++
CSSE1001/7030
Semester 2, 2018
"""

__author__ = "Neil Leiser - 45422470"

# Write your classes here
import random

class Card(object):
    """
    A class to define a basic card
    """
    def __init__(self,number,colour):
        """
        Define a card by its number and its colour

        Parameters:
        number(int): The number of the card
        colour(CardColour): The colour of the card
        """
        self._number = number
        self._colour = colour
        self._pick = 0

    def get_number(self):
        """
        Returns the number of the card
        """
        return self._number
    
    def get_colour(self):
        """
        Returns the colour of the card
        """
        return self._colour

    def set_number(self, number):
        """
        Sets the number of the card

        Parameters:
        number(int): The number assigned to the card
        """
        self._number = number

    def set_colour(self,colour):
        """
        Changes the colour of the card

        Parameters:
        colour(CardColour): The colour assigned to the card
        """
        self._colour = colour
        
    def get_pickup_amount(self):
        """
        Returns the amount of cards the next player should pickup
        """
        return self._pick

    def matches(self, card):
        """
        Determines if the next card to be placed on the pile matches this card
        Returns True if two cards match and False if they don't

        Parameters:
        card (Card): Card that has to be matched
        """
        #A card matches a base card if they have the same number or the same colour
        if (self._colour == card._colour) or (self._number == card._number):
            return True
        else:
            return False

    def play(self, player, game):
        """
        Perform a special card action
        (No speical action for base card)
        """
        return None

    def __str__(self):
        """
        Returns the string representation of this card
        Returns the card with its number and its colour
        """
        return "Card({0}, {1})".format(self._number,self._colour)

    def __repr__(self):
        """
        Same as __str__(self)
        Returns the card with its number and its colour
        """
        return "Card({0}, {1})".format(self._number,self._colour)

class SkipCard(Card):
    """
    Subclass of Card
    Special Card which skips the turn of the next player
    """
    def __init__(self,number,colour):
        """
        Define a card by its number and its colour

        Parameters:
        number(int): The number of the card
        colour(CardColour): The colour of the card
        """
        super().__init__(number,colour)

    def matches(self, card):
        """
        Determines if the next card to be placed on the pile matches this card
        Returns True if two cards match and False if they don't

        Parameters:
        card (Card): Card that has to be matched
        """
        #A card matches a SkipCard only if they have the same colour
        if (self._colour == card._colour):
            return True
        else:
            return False

    def play(self, player, game):
        """
        Perform a special card action
        Skips the turn of the next player
        """
        return game.skip()
    
    def __str__(self):
        """
        Returns the string representation of this card
        Returns the card with its number and its colour
        """
        return "SkipCard({0}, {1})".format(self._number,self._colour)
    
    def __repr__(self):
        """
        Returns the card with its number and its colour
        """
        return "SkipCard({0}, {1})".format(self._number,self._colour)

class ReverseCard(Card):
    """
    Subclass of Card
    Special Card which reverses the order of turns
    """
    def __init__(self,number,colour):
        """
        Define a card by its number and its colour

        Parameters:
        number(int): The number of the card
        colour(CardColour): The colour of the card
        """
        super().__init__(number,colour)
        
    def matches(self, card):
        """
        Determines if the next card to be placed on the pile matches this card
        Returns True if two cards match and False if they don't

        Parameters:
        card (Card): The card that has to be matched
        """
        #A card matches a ReverseCard only if they have the same colour
        if (self._colour == card._colour):
            return True
        else:
            return False

    def play(self, player, game):
        """
        Perform a special card action
        Reverses the order of turns
        """
        return game.reverse()

    def __str__(self):
        """
        Returns the string representation of this card
        Returns the card with its number and its colour
        """
        return "ReverseCard({0}, {1})".format(self._number,self._colour)

    def __repr__(self):
        """
        Returns the card with its number and its colour
        """
        return "ReverseCard({0}, {1})".format(self._number,self._colour)

  
class Pickup2Card(Card):
    """
    Subclass of Card
    Special Card which makes the next player pickup two cards
    """
    def __init__(self,number,colour):
        """
        Define a card by its number and its colour

        Parameters:
        number(int): The number of the card
        colour(CardColour): The colour of the card
        """
        super().__init__(number,colour)
        self._pick = 2 

    def matches(self, card):
        """
        Determines if the next card to be placed on the pile matches this card
        Returns True if two cards match and False if they don't

        Parameters:
        card (Card): The card that has to be matched
        """
        #A card matches a Pickup2Card only if they have the same colour
        if (self._colour == card._colour):
            return True
        else:
            return False

    def play(self, player, game):
        """
        Perform a special card action
        Makes the next player pickup two cards
        """
        game.get_turns().peak().get_deck().add_cards(game.pickup_pile.pick(2))

    def __str__(self):
        """
        Returns the string representation of this card
        Returns the card with its number and its colour
        """
        return "Pickup2Card({0}, {1})".format(self._number,self._colour)

    def __repr__(self):
        """
        Returns the card with its number and its colour
        """
        return "Pickup2Card({0}, {1})".format(self._number,self._colour)

class Pickup4Card(Card):
    """
    Subclass of Card
    Special Card which makes the next player pickup four cards
    """
    def __init__(self,number,colour):
        """
        Define a card by its number and its colour

        Parameters:
        number(int): The number of the card
        colour(CardColour): The colour of the card
        """
        super().__init__(number,colour)
        self._pick = 4
        
    def matches(self, card):
        """
        Determines if the next card to be placed on the pile matches this card
        Returns True if two cards match and False if they don't

        Parameters:
        card (Card): The card that has to be matched
        """
        #Pickup4Cards matches with any card
        return True

    def play(self, player, game):
        """
        Perform a special card action
        Makes the next player pickup four cards
        """
        game.get_turns().peak().get_deck().add_cards(game.pickup_pile.pick(4))

    def __str__(self):
        """
        Returns the string representation of this card
        Returns the card with its number and its colour
        """
        return "Pickup4Card({0}, {1})".format(self._number,self._colour)

    def __repr__(self):
        """
        Returns the card with its number and its colour
        """
        return "Pickup4Card({0}, {1})".format(self._number,self._colour)

class Deck(object):
    """
    A Collection of ordered Uno cards
    """
    def __init__(self,starting_cards=None):
        """
        Defines a deck

        Parameters:
        cards(list<Card>): A list of all the cards in the deck
        (None if deck is empty)
        """
        if starting_cards == None:
            self._cards = []
        else:
            self._cards = starting_cards
            
        self._length = len(self._cards)
        
    def get_cards(self):
        """
        Returns a list of cards in the deck
        """
        return self._cards

    def get_amount(self):
        """
        Returns the amount of cards in the deck
        """
        self._length = len(self._cards) 
        return self._length

    def shuffle(self):
        """
        Shuffle the order of the cards in the deck
        """
        random.shuffle(self._cards)

    def pick(self, amount=1):
        """
        Take the first 'amount' of cards off the deck and return them

        parameters:
        amount(int): the number of cards to be removed from the top of the deck
        """
        pick_cards = []
        
        if amount == None:
            pick_cards = []
            return None
        
        elif self._cards ==0:
            return None
        
        else:
            for i in range(0,amount):
                pick_cards.append(self._cards.pop(-1))
            self._length = len(self._cards)
            return pick_cards

    def add_card(self, card):
        """
        Place a card on top of the deck

        parameters:
        card(Card): card to be placed on top of the deck
        """
        self._cards.append(card)
        self._length = len(self._cards)

    def add_cards(self, cards):
        """
        Place a list of cards on top of the deck

        parameters:
        card(list<Card>): list of cards to be placed on top of the deck
        """
        for i in range(0,len(cards)):
            self._cards.append(cards[i])
        self._length = len(self._cards)

    def top(self):
        """
        Peaks the card on top of the deck and returns it
        Returns None if the deck is empty
        """
        if self._length < 1:
            return None
        else:
            return self._cards[-1]

class Player(object):
    """
    A player represents one of the players in a game of uno
    """
    def __init__(self,name):
        """
        Defines the base type of player

        parameters:
        name(str): player's name
        """
        self._name = name
        self._deck  = Deck()
        
    def get_name(self):
        """
        Returns the name of the player
        """
        return self._name

    def get_deck(self):
        """
        Returns the player deck of cards
        """
        return self._deck

    def is_playable(self):
        """
        Returns True if the players moves are not automatic
        """
        #raise error for base type of player
        raise NotImplementedError

    def has_won(self):
        """
        Returns True if the player has an empty deck and has won the game
        """
        if self._deck.get_cards() == []:
            return True
        else:
            return False
        
    def pick_card(self, putdown_pile):
        """
        Selects a card to play from the players deck

        parameters:
        putdown_pile(Deck): pile where the player has to play his cards
        """
        #raise error for base type of player
        raise NotImplementedError
    
class HumanPlayer(Player):
    """
    Subclass of Player
    Player that selects cards to play using the GUI
    """
    def __init__(self,name):
        """
        Defines the Human player

        parameters:
        name(str): player's name
        """
        super().__init__(name)
        
    def is_playable(self):
        """
        Returns True if the players moves are not automatic
        Returns False if players moves are automatic
        """
        return True
    
    def pick_card(self, putdown_pile):
        """
        Selects a card to play from the players deck
        Returns None for non-automated player

        parameters:
        putdown_pile(Deck): pile where the player has to play his cards
        """
        return None

class ComputerPlayer(Player):
    def __init__(self,name):
        """
        Defines the Computer player

        parameters:
        name(str): player's name
        """
        super().__init__(name)
        
    def is_playable(self):
        """
        Returns True if the players moves are not automatic
        Returns False if players moves are automatic
        """
        return False

    def pick_card(self, putdown_pile):
        """
        Selects a card to play from the players deck
        Returns None when a card connot be found
        Otherwise returns the first card found that can be played
        and removes the card from the deck

        parameters:
        putdown_pile(Deck): pile where the player has to play his cards
        """
        check_match = 0
        
        for i in range(0,self.get_deck().get_amount()):
            
            #match could be found
            if self.get_deck().get_cards()[i].matches(putdown_pile.top()):
                check_match+=1
                return self._deck.get_cards().pop(i)

        #No match could be found                
        if check_match == 0:
            return None
                


    
def main():
    print("Please run gui.py instead")


if __name__ == "__main__":
    main()
