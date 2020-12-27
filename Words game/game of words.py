# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Alexey Garmash
# Collaborators : -
# Time spent    : 7 h


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


class Word:
    """
    The class describes the object of the game - a word

    Attributes:
        WORDLIST_FILENAME -> str
            Filename with words.

    Methods:
        @classmethod
        get_word_score(word, hard)
            Calculate score of word and calls function get_word_point for this.

        @classmethod
        get_word_point()
            Calculate score of letter in word by the points in dictionary
            SCRABBLE_LETTER_VALUES.

        @classmethod
        get_all_words()
            Getter with cashing for wordlist.
    """
    WORDLIST_FILENAME = "words.txt"
    __wordlist = None

    @classmethod
    def get_word_score(cls, word, hand: dict):
        """
        Returns the score of the word by formula. Assumes the word is a
        valid word.
        """
        remaining_letters = sum(hand.values())
        expression = 7 * len(word) - 3 * (remaining_letters - len(word))
        return cls.get_word_points(word) * max(1, expression)

    @classmethod
    def get_word_points(cls, word):
        """
        Returns the score of the current word according to points
        in SCRABBLE_LETTER_VALUES
        """
        if not word:
            return 0
        point_list = list(map(lambda point: SCRABBLE_LETTER_VALUES[point] if point != WILDCARD else 0, word))
        word_point = reduce(lambda total, point: total + point, point_list)
        return word_point

    @classmethod
    def get_all_words(cls) -> list:
        """
        Returns a list of valid words. Words are strings of lowercase letters.
        Depending on the size of the word list, this function may
        take a while to finish.
        """
        if not cls.__wordlist:
            cls.__wordlist = [line.strip().lower() for line in open(cls.WORDLIST_FILENAME, 'r')]
        return cls.__wordlist


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

        display()
            Displays the current hand as a line of letters.

        deal()
            Create hand with letter from VOWELS and SCRABBLE_LETTER_VALUES, WILDCARD.

        update()
            Updates the current hand based on the entered word.

        substitute()
            Replaces one letter in the hand with a user selected one.

        add_score()
            Adder for self.__total

        set_score()
            Adder for private attribute self.__total
    """
    def __init__(self):
        self.hand = self.__deal()
        self.__total = 0
        self.sum_hand_points = sum(self.hand.values())

    def display(self):
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

    def __deal(self) -> dict:
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

    def substitute(self, letter: str):
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
            return False
        else:
            self.hand[letter] -= 1
            if self.hand[letter] <= 0:
                del self.hand[letter]
            new = choice(list(set(CONSONANTS).union(set(VOWELS)).difference(set(self.hand))))
            self.hand[new] = 1
            return True

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

    def update(self, word: str) -> dict:
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
            if key in self.hand.keys():
                self.hand[key] -= word_dict[key]
                if self.hand[key] <= 0:
                    del self.hand[key]

        return self.hand

    def get_score(self) -> int:
        """
        Getter for private attribute self.__total.
        """
        return self.__total

    def add_score(self, score):
        """
        Adder for private attribute self.__total
        """
        self.__total += score

    def set_score(self, score):
        """
        Setter for private attribute self.__total
        """
        self.__total = score


class WordsGame:
    """
    Class  describing the launch of the game and interaction with objects of other classes

    Methods:
        play_game()
            Launch game for "n" numbers of hands.

        @classmethod
        load_words()
            Load words from file to list

        is_valid_input()
            Function is run after being called from input_processing().
            Checks for the letters of the word in the hand and refreshes the hand.

        is_valid_wildcard()
            Function is run after being called from input_processing().
            Checks the correctness use WILDCARD in word. Returns a boolean value.
    """

    def __init__(self):
        self.__total_game_points = 0

    def play_game(self):
        """
        Waits for user to enter the number of hands
        and starts function call in cycle. Print informational messages for
        user.
        """
        print('Welcome! Prove that you god of words.')
        try:
            number_hands = input('Enter total numbers of hand: ')
            if not (number_hands.isdecimal() and int(number_hands) in range(MAX_HANDS)):
                print('You entered invalid value')
                return self.play_game()
        except ValueError:
            print('You entered invalid value')
            return self.play_game()

        for _ in range(int(number_hands)):
            current_hand = Hand()
            self.__play_hand(current_hand)

        print(f'Total score of game: {self.__total_game_points}')

    def __play_hand(self, current: Hand):
        """
        Makes a play for one hand.
        It prompts user to replace letter in the current hand, starts play cycle
        and at the end offers to replay hand.
        param current - current object of hand.
        """
        for prompt in range(2):
            print('Current Hand:', end=' ')
            hand_copy = current.hand.copy()
            current.display()

            if input('Would you like to substitute a letter? ').lower() == 'yes':
                if not current.substitute(input('Which letter would you like to replace: ').lower()):
                    print('This letter not in hand.')

            while current.sum_hand_points > 0:
                print('Current Hand:', end=' ')
                current.display()
                word = input('Enter word, or “!!” to indicate that you are finished: ').lower().replace(' ', '')
                # main process
                self.__input_processing(word, Word.get_all_words(), current)
                # current.input_processing(word, Word.get_all_words())

                if word == END_CHAR:
                    print(f'Total score for this hand: {current.get_score()}')
                    print('-' * 15)
                    break

            if prompt == 0:
                if input('Would you like to replay the hand? ').lower() == 'yes':
                    current.hand = hand_copy
                    current.set_score(0)
                    continue
            self.__total_game_points += current.get_score()
            break

    def __input_processing(self, word: str, wordlist: list, current: Hand):
        """
        The method coordinates checks.
        First, there is a check for the correctness of the input.
        Call to function __valid_output(), if the word passed the check.

        Otherwise, there is a check for a word with a wildcard.
        Call to function __wildcard_output, if the word passed the wildcard check.

        Displays an informational message, if the word fails the check.
        """
        if self.is_valid_input(word, current) and word in Word.get_all_words():
            self.__output(word, current)
            current.update(word)
        elif word.count(WILDCARD) == 1 and self.is_valid_wildcard(word, wordlist):
            self.__output(word, current)
            current.update(word)
        else:
            current.update(word)
            if current.sum_hand_points <= 0:
                print('Ran out of letters.')
                print(f'Total score for this hand: {current.get_score()}', '-' * 15, sep='\n')
                return None
            print('This is not a valid word. Please choose another word.')

    @staticmethod
    def is_valid_input(word: str, current: Hand) -> bool:
        """
        Checks the presence of letters from the word in the hand
        and the presence of the word in the word list.
        Returns a boolean according to this.
        """
        word_dict = current.get_frequency_dict(word)
        for key in word_dict.keys():
            if key not in current.hand.keys() or word_dict[key] > current.hand.get(key, 0):
                return False
        return True

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

    @staticmethod
    def __output(word: str, current):
        """
        The function calculates points for current word and displays an informational message.
        """
        score = Word.get_word_score(word, current.hand)
        print(f'"{word}" earned: {score} points')
        current.add_score(score)
        print(f'Total: {score}')


if __name__ == '__main__':
    game = WordsGame()
    game.play_game()
