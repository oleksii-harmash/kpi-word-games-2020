# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Alexey Garmash
# Collaborators : -
# Time spent    : 6 h


from math import ceil
from random import choice
from functools import reduce


HAND_SIZE = 7
VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
WILDCARD = '*'
END_CHAR = '!!'
# max number of allowed hands
MAX_HANDS = 5

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1,
    'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1,
    's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10,
}


class Game:
    """
    Class  describing the launch of the game and interaction with objects of other classes

    Attributes:
        WORDLIST_FILENAME -> str
            Filename with words.

        self.__wordlist -> list
            List of valid words from file "words.txt".
            Calls function self.load_words() at initialization

        self.__word
            Current word in iteration.


        self.__hand_obj - object of class
            Object of class Hand

        self.__total_game_points - int
            Sum of points for all hands.

    Methods:
        __play_hand()
            Launch game for one hand

        play_game()
            Launch game for "n" numbers of hands.

        @classmethod
        load_words()
            Load words from file to list
    """
    WORDLIST_FILENAME = "words.txt"

    def __init__(self):
        self.__wordlist = self.load_words()
        self.__word = None
        self.__hand_obj = None
        self.__hand_copy = None
        self.__total_game_points = 0

    def play_game(self):
        """
        Waits for user to enter the number of hands
        and starts function call in cycle. Print informational messages for
        user.
        """
        print('Welcome! Prove that you god of words.')
        try:
            number_hands = int(input('Enter total numbers of hand: '))
            if int(number_hands) not in range(MAX_HANDS):
                return self.play_game()
        except ValueError:
            print('You entered invalid value')
            return self.play_game()

        for _ in range(number_hands):
            self.__hand_obj = Hand()
            self.__play_hand()

        print(f'Total score of game: {self.__total_game_points}')

    def __play_hand(self, ):
        """
        Makes a play for one hand.
        It prompts user to replace letter in the current hand, starts play cycle
        and at the end offers to replay hand.
        """
        print('Current Hand:', end=' ')
        self.__hand_copy = self.__hand_obj.hand.copy()
        self.__hand_obj.display_hand()

        if input('Would you like to substitute a letter? ') in ('yes', 'Yes'):
            self.__hand_obj.substitute_hand(input('Which letter would you like to replace: '))

        while sum(self.__hand_obj.hand.values()) > 0:
            print('Current Hand:', end=' ')
            self.__hand_obj.display_hand()
            self.__word = input('Enter word, or “!!” to indicate that you are finished: ').lower().replace(' ', '')
            # main process
            self.__hand_obj.input_processing(self.__word, self.__wordlist)

            if self.__word == END_CHAR:
                print(f'Total score for this hand: {self.__hand_obj.get_hand_score()}', '-' * 15, sep='\n')
                break

        if input('Would you like to replay the hand? ') in ('yes', 'Yes'):
            self.__hand_obj.hand = self.__hand_copy
            return self.__play_hand()
        else:
            self.__total_game_points += self.__hand_obj.get_hand_score()

    @classmethod
    def load_words(cls):
        """
        Returns a list of valid words. Words are strings of lowercase letters.
        Depending on the size of the word list, this function may
        take a while to finish.
        """
        return [line.strip().lower() for line in open(cls.WORDLIST_FILENAME, 'r')]


class Word:
    """
    The class describes the object of the game - a word

    Methods:
        @classmethod
        get_word_score(word, hard)
            Calculate score of word and calls function get_word_point for this.

        @classmethod
        get_word_point()
            Calculate score of letter in word by the points in dictionary
            SCRABBLE_LETTER_VALUES

        @staticmethod
        word_in_wordlist(word, wordlist)
            Checks if a word is in wordlist
    """
    @classmethod
    def get_word_score(cls, word, hand: dict):
        """
        Returns the score of the word by formula. Assumes the word is a
        valid word.
        """
        remaining_letters = sum(hand.values())
        expression = 7 * len(word) - 3 * (remaining_letters - len(word))
        return cls.get_word_point(word) * max(1, expression)

    @classmethod
    def get_word_point(cls, word):
        """
        Returns the score of the current word according to points
        in SCRABBLE_LETTER_VALUES
        """
        if not word:
            return 0
        point_list = list(map(lambda point: SCRABBLE_LETTER_VALUES[point] if point != WILDCARD else 0, word))
        word_point = reduce(lambda total, point: total + point, point_list)
        return word_point

    @staticmethod
    def word_in_wordlist(word, wordlist):
        """
        Returns a boolean if the word is in the list of valid words
        """
        return word in wordlist


class Hand:
    """
    The class describing the object is a hand.
    In the game, the hand represents a set of valid letters and one symbol WILDCARD.

    Attributes:
        self.hand
            Unchangeable letters from which you can make a word.

        self.__total
            Sum of score from all guessed words in current hand.

    Methods:
        @staticmethod
        get_frequency_dict(word)
        Returns a dictionary where the keys are elements of the sequence and the values are integer counts.

        display_hand()
            Displays the current hand as a line of letters.

        deal_hand()
            Create hand with letter from VOWELS and SCRABBLE_LETTER_VALUES, WILDCARD.

        update_hand()
            Updates the current hand based on the entered word.

        input_processing()
            Sends a word for checks to different methods.

        valid_output()
            Runs if the word passed the correctness check.
            Calculates the points for the current word and displays an informational message.

        wildcard_output()
            Runs if the word passed the correctness check with WILDCARD.
            Calculates the points for the current word and displays an informational message.

        is_valid_input()
            Function is run after being called from input_processing().
            Checks for the letters of the word in the hand and refreshes the hand.

        is_valid_wildcard()
            Function is run after being called from input_processing().
            Checks the correctness use WILDCARD in word. Returns a boolean value.

        substitute_hand()
            Replaces one letter in the hand with a user selected one.

        get_hand_score()
            Getter for self.__total
    """
    def __init__(self):
        self.hand = self.__deal_hand()
        self.__total = 0

    def display_hand(self):
        """
        Displays the letters currently in the hand.

        For example:
           display_hand({'a':1, 'x':2, 'l':3, 'e':1})
        Should print out something like:
           a x x l l l e
        The order of the letters is unimportant.

        hand: dictionary (string -> int)
        """
        for letter in self.hand.keys():
            for j in range(self.hand[letter]):
                print(letter, end=' ')
        print()

    def __deal_hand(self) -> dict:
        """
        Returns a random hand containing n lowercase letters.
        ceil(n/3) letters in the hand should be VOWELS (note,
        ceil(n/3) means the smallest integer not less than n/3).

        Hands are represented as dictionaries. The keys are
        letters and the values are the number of times the
        particular letter is repeated in that hand.

        n: int >= 0
        returns: dictionary (string -> int)
        """

        hand = dict()
        num_vowels = int(ceil(HAND_SIZE / 3))

        for _ in range(num_vowels - 1):
            key = choice(VOWELS)
            hand[key] = hand.get(key, 0) + 1

        for _ in range(num_vowels, HAND_SIZE):
            key = choice(CONSONANTS)
            hand[key] = hand.get(key, 0) + 1
        hand[WILDCARD] = 1

        self.hand = hand
        return hand

    def input_processing(self, word: str, wordlist: list):
        """
        The method coordinates checks.
        First, there is a check for the correctness of the input.
        Returns a call to function __valid_output(), if the word passed the check.

        Otherwise, there is a check for a word with a wildcard.
        Returns a function call __wildcard_output, if the word passed the wildcard check.

        Displays an informational message, if the word fails the check.
        """
        if self.is_valid_input(word, wordlist):
            return self.__valid_output(word)
        elif word.count(WILDCARD) == 1 and self.is_valid_wildcard(word, wordlist):
            return self.__wildcard_output(word)
        else:
            self.__update_hand(word)
            if sum(self.hand.values()) <= 0:
                print('Ran out of letters.')
                print(f'Total score for this hand: {self.__total}', '-' * 15, sep='\n')
                return None
            print('This is not a valid word. Please choose another word.')

    def is_valid_input(self, word: str, wordlist: list) -> bool:
        """
        Checks the presence of letters from the word in the hand
        and the presence of the word in the word list.
        Returns a boolean according to this.
        """
        word_dict = self.get_frequency_dict(word)
        for key in word_dict.keys():
            if key not in self.hand.keys() or word_dict[key] > self.hand.get(key, 0):
                return False

        return Word.word_in_wordlist(word, wordlist)

    @staticmethod
    def is_valid_wildcard(word: str, wordlist: list) -> bool:
        """
        Checks for words matching the input, where the WILDCARD is a VOWEL.
        Returns a boolean according to this.
        """
        matches = list()
        for other_word in wordlist:
            if len(other_word) == len(word):
                for char, other in zip(word, other_word):
                    if (char != other and char != WILDCARD) or (char == WILDCARD and other not in VOWELS):
                        break
                else:
                    matches.append(word)
        return bool(matches)

    def substitute_hand(self, letter: str):
        """
        Allow the user to replace all copies of one letter in the hand (chosen by user)
        with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
        should be different from user's choice, and should not be any of the letters
        already in the hand.

        If user provide a letter not in the hand, the hand should be the same.

        Has no side effects: does not mutate hand.

        For example:
            substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
        might return:
            {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
        The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
        already in the hand.

        hand: dictionary (string -> int)
        letter: string
        returns: dictionary (string -> int)
        """
        if letter not in set(self.hand):
            print('This letter not in hand.')
        else:
            self.hand[letter] -= 1
            if self.hand[letter] <= 0:
                del self.hand[letter]
            new = choice(list(set(CONSONANTS).union(set(VOWELS)).difference(set(self.hand))))
            self.hand[new] = 1

    @staticmethod
    def get_frequency_dict(word: str) -> dict:
        """
        Returns a dictionary where the keys are elements of the sequence
        and the values are integer counts, for the number of times that
        an element is repeated in the sequence.

        sequence: string or list
        return: dictionary
        """
        freq = dict()
        for char in word:
            freq[char] = freq.get(char, 0) + 1
        return freq

    def __update_hand(self, word: str) -> dict:
        """
        Does NOT assume that hand contains every letter in word at least as
        many times as the letter appears in word. Letters in word that don't
        appear in hand should be ignored. Letters that appear in word more times
        than in hand should never result in a negative count; instead, set the
        count in the returned hand to 0 (or remove the letter from the
        dictionary, depending on how your code is structured).

        Updates the hand: uses up the letters in the given word
        and returns the new hand, without those letters in it.

        Has no side effects: does not modify hand.

        word: string
        hand: dictionary (string -> int)
        returns: dictionary (string -> int)
        """
        word_dict = self.get_frequency_dict(word)

        for key in list(word_dict):
            try:
                self.hand[key] -= word_dict[key]
                if self.hand[key] <= 0:
                    del self.hand[key]
            except KeyError:
                del word_dict[key]

        return self.hand

    def __valid_output(self, word: str):
        """
        The function starts if the word passed input check.
        The function calculates points for current word and displays an informational message,
        after which it calls a function that updates the hand.
        """
        score = Word.get_word_score(word, self.hand)
        self.__update_hand(word)
        print(f'"{word}" earned: {score} points')
        self.__total += score
        print(f'Total: {score}')

    def __wildcard_output(self, word: str):
        """
        The function starts if the word passed input check with WILDCARD.
        The function calculates points for current word and displays an informational message,
        after which it calls a function that updates the hand.
        """
        score = Word.get_word_score(word, self.hand)
        self.__update_hand(word)
        print(f'"{word}" earned: {score}')
        self.__total += score
        print(f'Total: {score}')

    def get_hand_score(self) -> int:
        """
        Getter for private attribute self.__total.
        """
        return self.__total


if __name__ == '__main__':
    game = Game()
    game.play_game()
