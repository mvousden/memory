#!/usr/bin/python

import numpy as np
import os
import time
import sys


def clear_screen():
    print('\033c')


def generate_random_strinteger(N=1):
    """
    Generates a random integer and returns it as a string.
    """
    if N == 1:
        return str(np.random.randint(0, 10))
    else:
        return "".join(np.array(np.random.randint(0, 10, N), dtype=str))


def increment_rotator(rotator):
    if rotator == "|":
        return "/"
    elif rotator == "/":
        return "-"
    elif rotator == "-":
        return "\\"
    elif rotator == "\\":
        return "|"


def ver_input(message):
    """
    Cross-major-version input handling.
    """
    if sys.version_info.major < 3:
        return raw_input(message)
    else:
        return input(message)


def standard_game(timer, refreshMode=False):
    """
    Plays the standard memory game, with pauses equal to 'timer' seconds in
    length. Returns the player's score when finished.
    """

    initialLength = 3
    sequence = generate_random_strinteger(initialLength)
    failure = False
    while(failure is not True):

        # Reset rotator
        rotator = "|"

        # Manipulate sequence.
        if refreshMode == False:
            sequence += generate_random_strinteger(1)
        else:
            sequence = generate_random_strinteger(len(sequence) + 1)

        # Show the sequence with pauses.
        for value in sequence:
            clear_screen()
            print("    {} {}".format(rotator, value))
            rotator = increment_rotator(rotator)
            time.sleep(timer)

        # Prompt user for sequence.
        clear_screen()
        guess = ver_input("    What was the sequence? ")

        # Failure condition.
        if guess != sequence:
            failure = True

    # Commiserations
    print("    You guessed '{}'. The real sequence was '{}'. Bad luck!"
          .format(guess, sequence))

    # Computing score
    score = len(sequence) - 1
    if score == initialLength:
        score = 0
    return score


def main():

    # Print preamble and select difficulty.
    clear_screen()
    print("""
    Welcome to memory! Choose your difficulty.
    [A for easy, b for medium, or c for hard].
    """)
    difficulty = ver_input("    ")

    if difficulty == "c":
        difficultyText = "hard"
    elif difficulty == "b":
        difficultyText = "medium"
    else:
        difficulty = "a"
        difficultyText = "easy"

    difficultyTimer = {"a": 1., "b": 0.6, "c": 0.4}

    print("")
    if difficultyText == "easy":
        print("    Taking it easy then.")
    elif difficultyText == "medium":
        print("    A medium challenge for you.")
    else:
        print("    Hard it is. I hope you're prepared.")

    # Refresh mode?
    print("""
    Would you like to play refresh mode for extra challenge? [y/N]
    """)
    refreshMode = ver_input("    ")

    if refreshMode == "y":
        refresh = True
        if difficulty == "c":
            print("    Quite the baller I see.")
        else:
            print("    So be it.")

    else:
        refresh = False
        if difficulty == "c":
            print("    Not so brave after all.")
        else:
            print("    Fair enough.")

    # Postamble
    print("""
    You will have {} seconds to memorise each value.
    Press return when ready.
    """.format(difficultyTimer[difficulty]))

    ver_input(" ")
    clear_screen()

    # Load old high score, if any.
    scoreFilePath = ("{}/.memory_score_{}{}"
                     .format(os.path.expanduser("~"), difficultyText,
                             "_refresh" if refresh is True else ""))
    if os.path.exists(scoreFilePath):
        with open(scoreFilePath, "r") as scoreFile:
            highScoreString = scoreFile.read()
            if len(highScoreString) != 0:
                highScore = int(highScoreString)
            else:
                highScore = 0
    else:
        highScore = 0

    # Play the game.
    score = standard_game(difficultyTimer[difficulty], refresh)

    # Score reporting
    print("    Your score is {} on {}.".format(score, difficultyText))
    if score > highScore:
        if highScore > 0:
            print("    At least you beat the old high score of {} for this difficulty."
                  .format(highScore))
        with open(scoreFilePath, "w+") as scoreFile:
            scoreFile.write(str(score))
    else:
        print("    The old high score of '{}' still stands for this difficulty."
              .format(highScore))

    # Try again?
    again = ver_input("    Try again? [y/N] ")
    if again == "y":
        main()


if __name__ == "__main__":
    main()
