# Problem Set 2, hangman.py
# Name: Alexey Garmash
# Students group: KM-04
# Collaborators: -
# Time spent: 9 h
from random import choice
from string import ascii_lowercase
import time
from enum import Enum

VOWELS = {'a', 'e', 'i', 'o', 'u'}
UNKNOWN_LETTER = '_'
HINT_LETTER = '*'


class GameMode(Enum):
    """
    Class describe game mode of game.

    Attributes:
        hard_mode - without hints
        easy_mode - with hints
    """
    HARD_MODE = 0
    EASY_MODE = 1


class Hangman:
    """
    Class describe game of the same name - Hangman.

    ATTRIBUTES:
        __wordlist = None
            List of words from word.txt file.
            Will get the value of the list when the game starts

        __word = None
            Secret word of game.
            Will get the value of the list when the game starts

        __warnings = 3
            Warnings that has user according to rules of game.

        __guesses = 6
            Prompts that has user getting in the start.

        __available_letters = set(ascii_lowercase)
            Letters that remaining at the stage of game.

        __is_end_game = False
            Flag that indicate process of game. (True if game had end)

        __word_letters_guessed = set()
            Letters which will be added if user guess.

        __game_mode = GameMode.(EASY/HARD)_MODE.value
            Game mode of game. With hints or without hints. Uses class
            attribute of class GameMode(Enum).


    METHODS:
        __get_words(self)
            Opens .txt file and reads it

        __choose_word(self)
            Uses method choice() from the module "random"

        get_complexity
            Uniqueness of word it's number of unique words multiply to number of guesses remaining

        is_guessed_word(self)
            Checks if a word is guessed

        __get_guessed_word(self, letter: str)
            Returns string, comprised of letters, underscores (_)

        __get_available_letters(self)
            Returns  comprised of letters that represents which
        letters have not yet been guessed

        @staticmethod
        is_ascii_symbol(letter)
            Returns boolean, True, if input is letter, otherwise False

        warnings_left(self, letter)
            Func checks user input for invalid values and repeated letters

        guesses_left(self, letter)
           Returns boolean - otherwise False, information message and
           take away attempts (guesses)

        @staticmethod
        match_with_gaps(my_word, other_word)
            Returns boolean, True if all the actual letters of my_word match the
            corresponding letters of other_word, or the letter is the special symbol
            _ , and my_word and other_word are of the same length. False otherwise

        __show_possible_matches(self, my_word)
            Returns an string of similar words if matches are True
            if matches are False - returns information message(string)

        hangman(self)
            Function that initialize process of game. Connect all functions and get
            information's messages.

        start(self)
            Function that start hangman function and initialize self.word & self.wordlist
            Shows welcome words.

    """
    WORDLIST_FILENAME = 'words.txt'
    __wordlist = None

    def __init__(self, game_mode, word=None, guesses=6, warnings=3):
        """
        Init block for initialization attributes
        """
        self.__word = word
        self.__warnings = warnings
        self.__guesses = guesses
        self.__available_letters = set(ascii_lowercase)
        self.__is_end_game = False
        self.__game_mode = game_mode

        # successful guessed letters
        self.__word_letters_guessed = set()

        if not self.__word:
            self.__word = self.__choose_word()

    @classmethod
    def __get_words(cls) -> list:
        """
        Opens .txt file and reads it;
        :return: list of words from 'words.txt'
        """
        if not cls.__wordlist:
            cls.__wordlist = open(cls.WORDLIST_FILENAME, 'r').readline().split()
        return cls.__wordlist

    @classmethod
    def __choose_word(cls) -> str:
        """
        Uses method choice() from the module "random";
        :return: word from wordlist at random;
        """
        return choice(cls.__get_words())

    def get_score(self) -> int:
        """
        Uniqueness of word it's number of unique words multiply to number of guesses remaining;
        :return: uniqueness of word;
        """
        if self.__is_end_game:
            return len(set(self.__word)) * self.__guesses
        else:
            raise StartError("Game hasn't been started.")

    def __is_word_guessed(self) -> bool:
        """
        :return: boolean, True if all the letters of secret_word are in letters_guessed and
        prints information word for the winner. False otherwise;
        """
        return set(self.__word) == set(self.__word_letters_guessed)

    def __get_guessed_word(self, letter: str) -> str:
        """
        :param: letter: guess letter from user
        :return: string, comprised of letters, underscores (_), and spaces that represents
        which letters in secret_word have been guessed so far;
        """
        return ''.join([letter if letter not in self.__available_letters else f'{UNKNOWN_LETTER} '
                        for letter in self.__word]).strip()

    def __get_available_letters(self) -> str:
        """
        :return: string (of letters), comprised of letters that represents which
        letters have not yet been guessed;
        """
        return ''.join(sorted(self.__available_letters))

    @staticmethod
    def __is_latin_letter(letter: str) -> bool:
        """
        :param letter: input the user is trying to guess;
        :return: boolean, True, if input is letter, otherwise False;
        """
        return letter != '' and letter.isalpha() and letter.isascii()

    def __warnings_left(self, letter: str) -> bool:
        """
        Func checks user input for invalid values and repeated letters;
        :param letter: input the user is trying to guess;
        :return: boolean - True and append letter to list available letters, if check_letter() True,
        boolean - otherwise False, print information message about
        repetition of a letter or use of a banned symbol
        and take away warnings;
        """

        # var is_warning has boolean value
        is_warning = self.__is_latin_letter(letter) and letter in self.__available_letters

        if is_warning:
            if letter in self.__word:
                self.__word_letters_guessed.add(letter)
            self.__available_letters.remove(letter)
        else:
            self.__warnings -= 1
            if self.__warnings >= 0:
                print(f'Oops! That is not a valid symbol or you already entered that letter.')
                print(f'You have {self.__warnings} warnings left: ', self.__get_guessed_word(self.__word))
            else:
                self.__guesses -= 1
        return is_warning

    def __guesses_left(self, letter: str) -> bool:
        """
        :param letter: input the user is trying to guess;
        :return: boolean - True, prints information message
        and calls func get_guessed_word, if letter in word,
        boolean - otherwise False, information message and take away attempts (guesses);
        """

        # var is_guessed has boolean value
        is_guessed = letter in self.__word

        if is_guessed:
            print('Good guess:', self.__get_guessed_word(self.__word))
        else:
            self.__guesses -= 2 if letter in VOWELS else 1
            if self.__guesses >= 0:
                print(f'Oops! That letter is not in my word.')
                print(f'Please guess a letter: {self.__get_guessed_word(self.__word)}')
        return is_guessed

    @staticmethod
    def __match_with_gaps(my_word: str, other_word: str) -> bool:
        """
        :param my_word: string with _ characters, current guess of secret word
        :param other_word: string, regular English word
        :return: boolean, True if all the actual letters of my_word match the
            corresponding letters of other_word, or the letter is the special symbol
            _ , and my_word and other_word are of the same length. False otherwise;
        """
        if len(my_word) != len(other_word):
            return False
        for char, new_char in zip(my_word, other_word):
            if (char == UNKNOWN_LETTER and new_char in set(my_word)) \
                    or (char != new_char and char != UNKNOWN_LETTER):
                return False
        return True

    def __show_possible_matches(self, my_word: str) -> str:
        """
        :param my_word: string with _ characters, current guess of secret word
        :return: returns an string of similar words if matches are True,
                 if matches are False - returns information message(string)
                 Keep in mind that in hangman when a letter is guessed, all the positions
                 at which that letter occurs in the secret word are revealed.
                 Therefore, the hidden letter(_ ) cannot be one of the letters in the word
                 that has already been revealed.
        """

        # var contains a list of words that match the condition
        # if there are no words it returns "No matches found"
        show_matches = list()

        temp_word = my_word.replace(' ', '')

        for other_word in self.__get_words():
            if self.__match_with_gaps(temp_word, other_word):
                show_matches.append(other_word)
        if not show_matches:
            return 'No matches found'
        return ' '.join(show_matches)

    def __game_process(self):
        """
        Starts up an interactive game of Hangman.
        * At the start of the game, let the user know how many
          letters the secret_word contains and how many guesses s/he starts with.
        * The user should start with 6 guesses
        * Before each round, you should display to the user how many guesses
          s/he has left and the letters that the user has not yet guessed.
        * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
        * The user should receive feedback immediately after each guess
          about whether their guess appears in the computer's word.
        * After each guess, you should display to the user the
          partially guessed word so far.
        * If the guess is the symbol *, print out all words in wordlist that
          matches the current guessed word.
        Follows the other limitations detailed in the problem write-up.
        """
        self.__is_end_game = True

        while self.__guesses > 0:
            print('-' * 20)
            print(f'You have {self.__guesses} guesses left.')
            print(f'Available letters: {self.__get_available_letters()}')
            letter = str(input('Please guess a letter: ')).lower()

            # for more comfortable work with user - add delay
            time.sleep(1)

            if letter == HINT_LETTER and self.__game_mode == GameMode.EASY_MODE:
                print('Possible word matches are: ', end='')
                print(self.__show_possible_matches(self.__get_guessed_word(letter)))
            elif not self.__warnings_left(letter) or not self.__guesses_left(letter):
                continue

            if self.__is_word_guessed():
                print('-' * 20)
                print('\nCongratulations, you won!')
                print(f'Total score: {self.get_score()}')
                break

        if self.__warnings < 0 or self.__guesses < 0:
            print('-' * 20)
            print('\nSorry, you ran out of guesses/warnings.', end='')
            print(f'The word was else: \n "{self.__word}"')

    def start(self):
        """
        Function initialize attribute self.word and self.wordlist.
        Show welcome words and start the process of game
        """

        if self.__is_end_game:
            raise RestartError('Game can be ran only once')

        # welcome words
        print(f'Welcome to the game Hangman!')
        print(f'I am thinking of a word that is {len(self.__word)} letters long.')
        print(f'You have {self.__warnings} warnings and {self.__guesses} guesses left')

        # for more comfortable work with user - add delay
        time.sleep(1)
        self.__game_process()


class RestartError(Exception):
    pass


class StartError(Exception):
    pass


if __name__ == "__main__":
    game = Hangman(GameMode.EASY_MODE)
    game.start()
