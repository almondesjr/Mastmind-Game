'''
Agesandro Almondes 
CS 5001 Fall 2023
Final Project Mastermind Gam Test Suite
'''

import unittest
from mastermind_game import ColorGuessGame

def check_guess(pattern, guesses):
    '''
    Checks if the color is in the right place, if so corect place gets
    +1, and if not in correct place but correct color, correct color gets
    +1 this is mimicing the logic behind check guess. I was uncertain what to do
    here so i created this stand alone and directly called the other
    '''
    results = {"correct_place": 0, "correct_color": 0}
    pattern_copy = pattern[:]
    guesses_copy = guesses[:]

    for i in range(len(guesses)):
        if guesses[i] == pattern[i]:
            results["correct_place"] += 1
            pattern_copy[i] = None
            guesses_copy[i] = None
    for color in range(len(guesses_copy)):
        if guesses_copy[i] is not None and guesses_copy[i] in pattern_copy:
            results["correct_color"] += 1
            pattern_copy[pattern_copy.index(color)] = None
    return results

class TestColorGuessGame(unittest.TestCase):
    '''
    Test class that calls the functions, logic above to test in the
    if logic works. This method is used because im uncertain how i 
    would mimic a users click
    '''
    
    def test_compare(self):
        test_cases = [
            (['red', 'blue', 'green', 'yellow'], ['red', 'purple', 'green', 'black'], {'correct_place': 2, 'correct_color': 0}),
            (['blue', 'black', 'green', 'yellow'], ['red', 'blue', 'yellow', 'black'], {'correct_place': 1, 'correct_color': 2}),
        ]
        for secret_guess, user_guess, expected in test_cases:
            result = check_guess(secret_guess, user_guess)
            self.assertEqual(result, expected)
    
    def test_evaluate_guesses(self):
        test_cases = [
            (["red", "blue", "green", "yellow"], ["red", "purple", "green", "black"], {"correct_place": 2, "correct_color": 0}),
            (["blue", "black", "green", "yellow"], ["red", "blue", "yellow", "black"], {"correct_place": 1, "correct_color": 2}),
        ]
        for pattern, guesses, expected in test_cases:
            result = check_guess(pattern, guesses)
            self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()