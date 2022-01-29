'''
Command line wordle game

Author: Kamron Cole kjc8084@rit.edu
'''
import os
import random

# Colours used in output
RED = '\033[1;31m'
GREEN = '\033[1;32m'
WHITE = '\033[0m'
YELLOW = '\033[1;33m'

# Numerical values too handle guess results easier
CORRECT_ALL = 100 # correct letter and position.
CORRECT_LETTER = 50 # correct letter wrong position.
WRONG = 0 # Wrong letter and position.

# Assign colour to guess result
GUESS_RESULT_DICT = {
    CORRECT_ALL: GREEN,
    CORRECT_LETTER: YELLOW,
    WRONG: WHITE
}

# Game Constants
WORD_LEN = 5
MAX_GUESSES = 6
ASSETS_PATH = '/assets'
ALLOWED_GUESSES_PATH = f'.{ASSETS_PATH}/wordle-allowed-guesses.txt'
POSSIBLE_ANSWERS_PATH = f'.{ASSETS_PATH}/wordle-answers.txt'

ALLOWED_WORDS = sorted([word.strip() for word in open(ALLOWED_GUESSES_PATH).readlines()]) # Possible guesses including answers
WORDS = sorted([word.strip() for word in open(POSSIBLE_ANSWERS_PATH).readlines()]) # Possible answers


class Guess:
    '''
    A players single guess in a wordle game
    '''
    __slots__ = ['__guess', '__answer', '__feedback']


    def __init__(self, guess: str, answer: str):
        self.__guess = guess
        self.__answer = answer
        self.__feedback = self.__build_feedback()


    def __str__(self):
        string = ''
        for letter, result in self.__feedback:
            string += f'{GUESS_RESULT_DICT[result]}[{letter}]{WHITE}'
        return string


    def __backward_check_result(self, flag, result):
        if flag in result:
            for j in range(len(result)):
                if result[j] == flag:
                    result[j][1] = WRONG
                    break

    def __build_feedback(self) -> list:
        '''
        Build a list<str, int> containing (letter in word, hint result) where the index is a letter's position and 
        hint result is decided depending on the answer.
        '''
        answer_dict = dict()
        for i in range(len(self.__answer)):
            letter = self.__answer[i]
            if letter not in answer_dict:
                answer_dict[letter] = []
            answer_dict[letter].append(i)

        result = []
        for i in range(len(self.__guess)):
            letter = self.__guess[i]
            if letter in answer_dict and i in answer_dict[letter]:
                item = [letter, CORRECT_ALL]
                self.__backward_check_result([letter, CORRECT_LETTER], result)
                result.append(item)
                answer_dict[letter].remove(i)
            elif letter in answer_dict and len(answer_dict[letter]) > 0:
                flag = [letter, CORRECT_LETTER]
                self.__backward_check_result(flag, result)
                result.append(flag)
            else:
                result.append([letter, WRONG])
        return result


    def get_feedback(self) -> list: return self.__feedback
    def is_answer(self) -> bool: return self.__guess == self.__answer
        

class Board:
    '''
    Wordle game board that keeps track of player's previous guesses
    '''
    __slots__ = ['__board', '__guesses']


    def __init__(self):
        self.__board = ['[ ][ ][ ][ ][ ]' for _ in range(MAX_GUESSES)]
        self.__guesses = 0


    def __str__(self) -> str:
        string = ''
        for guess in self.__board:
            string += f'{guess}\n'
        return string


    def make_guess(self, guess: Guess):
        '''
        insert guess into the board and prepare it for next guess.
        '''
        self.__board[self.__guesses] = guess
        self.__guesses += 1


class Wordle:
    '''
    Wordle game where a player attempts to guess a certain length word within a certain number of guesses and is given feedback on the letter's position and whether the word contains it for each guess
    '''
    __slots__ = ['__allowed_words', '__words', '__answer', '__guesses', '__board']

    
    def __init__(self):
        self.__board = Board()
        self.__allowed_words = ALLOWED_WORDS
        self.__words = WORDS
        self.__answer = random.choice(self.__words)
        self.__guesses = 0

    
    def __str__(self):
        return str(self.__board)
    

    def make_guess(self, raw_guess: str) -> Guess:
        '''
        given a word, make a guess and
        '''
        raw_guess = raw_guess.lower()
        if raw_guess not in self.__allowed_words:
            self.__clear_screen()
            print(f'{RED}"{raw_guess}" is not on the word list.{WHITE}')
            return None

        guess = Guess(raw_guess, self.__answer)
        self.__board.make_guess(guess)

        return guess


    def play(self):
        '''
        Play the game through a command line, prompting for a guess MAX_GUESSES number of times, invalid guesses arent counted
        '''
        self.__clear_screen()
        while self.__guesses < MAX_GUESSES:
            print(self.__board)
            print()
            raw_guess = input('Make a guess: ')
            guess = self.make_guess(raw_guess)
            if guess == None:
                continue

            self.__guesses += 1
            if guess.is_answer():
                print(self.__board)
                print(f'{GREEN}Congratulations! {self.__guesses}/{MAX_GUESSES}{WHITE}')
                return

            self.__clear_screen()
            print()
        print(self.__board)
        print(f'{RED}Unluckers! Maybe next time.{WHITE}')

    
    def __clear_screen(self):
        '''
        clear terminal based on operating system
        '''
        if os.name == 'nt':
             os.system('cls')
        else: 
            os.system('clear')


    def get_answer(self):
        return self.__answer


    def get_board(self):
        return self.__board


def main():
    game = Wordle()
    game.play()
    # print(game.get_answer())


if __name__ == '__main__':
    main()
