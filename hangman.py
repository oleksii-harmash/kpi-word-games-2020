# Problem Set 2, hangman.py
# Name: Alexey Garmash
# Students group: KM-04
# Collaborators: -
# Time spent: 5 h

from random import choice
from string import ascii_lowercase
import time


def get_words() -> list:
    '''
    Opens .txt file and reads it;
    :return: list of words from 'words.txt'
    '''
    return open('words.txt', 'r').readline().split()


def choose_word(wordlist: list) -> str:
    '''
    :param wordlist: Uses method choice() from the module "random";
    :return: word from wordlist at random;
    '''
    return choice(wordlist)


def get_complexity(secret_word: str, guesses_remaining: int) -> int:
    '''
    Uniqueness of word it's number of unique words multipy to number of guesses remaining;
    :return: uniqueness of word;
    :param secret_word: hidden word from worlist;
    '''
    return len(set(secret_word)) * guesses_remaining


def is_word_guessed(secret_word: str, letters_guessed: list) -> bool:
    '''
    :param secret_word: string, the word the user is guessing;
    :param letters_guessed: list (of letters), which letters have been guessed so far;
    :return: boolean, True if all the letters of secret_word are in letters_guessed. False otherwise;
    '''

    if set(secret_word) == set(letters_guessed):
        print('-' * 20, f'\nGongratulations, you won!\nTotal score: {get_complexity(WORD, guesses)}')
        return True
    else:
        return False


def get_guessed_word(secret_word: str, letters_guessed: list, letter: str) -> str:

    '''
    :param secret_word: string, the word the user is guessing;
    :param letters_guessed: list (of letters), which letters have been guessed so far;
    :return: string, comprised of letters, underscores (_), and spaces that represents
    which letters in secret_word have been guessed so far;
    '''
    return ''.join([letter if letter in letters_guessed else '_ ' for letter in secret_word])


def get_available_letters(letters_guessed: list, letter: str) -> str:
    '''
    :param letters_guessed: list (of letters), which letters have been guessed so far;
    :return: string (of letters), comprised of letters that represents which
    letters have not yet been guessed;
    '''
    return ''.join([letter for letter in avail_lttrs if letter not in letters_guessed])


def check_letter(letter: str) -> bool:
    '''
    :param letter: input the user is trying to guess;
    :return: boolean, True, if input is letter, otherwise False;
    '''
    return letter != '' and letter.lower() in ascii_lowercase


def warnings_left(letter: str) -> bool:
    '''
    Func checks user input for invalid values and repeated letters;
    :param letter: input the user is trying to guess;
    :return: boolean - True and append letter to list available letters, if check_letter() True,
    boolean - otherwise False and take away warnings;
    '''
    global avail_lttrs, letters_guessed, WORD, warnings

    is_warning = check_letter(letter) and letter in avail_lttrs
    if is_warning:
        if letter in WORD:
            word_letters_guessed.append(letter)
        letters_guessed.append(letter)
        avail_lttrs = get_available_letters(letters_guessed, letter)
    else:
        warnings -= 1
        if warnings >= 0:
            print( f'Oops! That is not a valid symbol or you already entered that letter. '
                   f'You have {warnings} warnings left: ', get_guessed_word(WORD, letters_guessed, letter))
    return is_warning


def guesses_left(letter: str) -> bool:
    '''
    :param letter: input the user is trying to guess;
    :return: boolean - True and calls func get_guesset_word, if letter in word,
    boolean - otherwise False and take away attempts (guesses);
    '''
    global WORD, letters_guessed, guesses

    is_guessed = letter in WORD
    if is_guessed:
        print('Good guess:', get_guessed_word(WORD, letters_guessed, letter))
    else:
        guesses -= 2 if letter in ['a', 'e', 'i', 'o'] else 1
        if guesses >= 0:
            print(f'Oops! That letter is not in my word.\n'
                  f'Please guess a letter: {get_guessed_word(WORD, letters_guessed, letter)}')
    return is_guessed


def match_with_gaps(my_word: str, other_word: str) -> bool:
    '''
    :param my_word: string with _ characters, current guess of secret word
    :param other_word: string, regular English word
    :return: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length. False otherwise;
    '''
    match, match_word = [], ''.join(my_word.split(' '))

    for i in range(len(match_word)):
        if match_word[i] == other_word[i] and match_word[i] != '_' and len(match_word) == len(other_word):
            match.append('1')
        elif match_word[i] != other_word[i] and match_word[i] != '_':
            match.append('0')

    match = False if '0' in ''.join(match) else True
    return bool(match)


def show_possible_matches(my_word: str) -> str:
    '''
    :param my_word: string with _ characters, current guess of secret word
    :return: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    '''
    global show
    show.clear()

    for i in WORDLIST:
        if len(i) == len(''.join(my_word.split(' '))) and match_with_gaps(my_word, i):
            show.append(i)
    if not(show):
        return 'No matches found'
    return ' '.join(show)


def hangman(secret_word: str, game_mode: int) -> str:
    '''
    :param secret_word: string, the secret word to guess.
    :param game_mode: 1 - without hints, 2 - with hints
    :return:

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
    '''
    global warnings, guesses, avail_lttrs, WORD, letters_guessed
    if warnings < 0 or guesses < 0:
        return print('-' * 20, f'\nSorry, you ran out of guesses/warnings. The word was else:\n"{WORD}"')

    print('-'*20, f'\nYou have {guesses} guesses left.\nAvailable letters: {avail_lttrs}')
    letter = str(input('Pless guess a letter: ')).lower()

    time.sleep(1)
    if letter == '*' and game_mode == 2:
        print(f'Possible word matches are: {show_possible_matches(get_guessed_word(WORD, letters_guessed, letter))}')
        return hangman(WORD, game_mode)

    elif not warnings_left(letter) or not guesses_left(letter) or not is_word_guessed(WORD, word_letters_guessed):
        return hangman(WORD, game_mode)


if __name__ == "__main__":
    # get wordlist from txt and create constants (word)
    WORDLIST = get_words()
    WORD = choose_word(WORDLIST)

    #creating variables
    warnings, guesses = 3, 6
    avail_lttrs = ascii_lowercase
    letters_guessed, word_letters_guessed, show = [], [], []

    # welcome words
    print(f'Welcome to the game Hangman!\nI am thinking of a word that is {len(WORD)} letters long.\nYou have '
          f'{warnings} warnings and {guesses} guesses left')
    time.sleep(1)

    # second if for choosing game mode (1 - without hints, 2 - with hints)
    hangman(WORD, 1)
