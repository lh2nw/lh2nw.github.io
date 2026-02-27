import random
import string
import os

WORDLIST_FILENAME = "words.txt"


def load_words():
    """ Returns a list of valid words. """
    # Marker to see if the file exists in the current folder
    if not os.path.exists(WORDLIST_FILENAME):
        print(f"ERROR: Cannot find '{WORDLIST_FILENAME}' in {os.getcwd()}")
        return ["apple", "banana", "cherry"]

    print("Loading word list from file... (Please wait)")
    try:
        with open(WORDLIST_FILENAME, 'r') as inFile:
            line = inFile.readline()
            wordlist = line.split()
        print("  ", len(wordlist), "words loaded.")
        return wordlist
    except Exception as e:
        print(f"ERROR: An error occurred: {e}")
        return ["apple", "banana", "cherry"]


def choose_word(wordlist):
    return random.choice(wordlist)


# --- Core Logic Functions ---

def is_word_guessed(secret_word, letters_guessed):
    """ Returns True if all letters of secret_word are in letters_guessed. """
    return all(letter in letters_guessed for letter in secret_word)


def get_guessed_word(secret_word, letters_guessed):
    """ Returns pattern like 'a _ _ l e'. """
    return "".join([char if char in letters_guessed else "_ " for char in secret_word])


def get_available_letters(letters_guessed):
    """ Returns remaining lowercase letters. """
    return "".join([char for char in string.ascii_lowercase if char not in letters_guessed])


def match_with_gaps(my_word, other_word):
    """ Helper for hints: matches word pattern to wordlist. """
    my_word = my_word.replace(" ", "")
    if len(my_word) != len(other_word):
        return False
    for i in range(len(my_word)):
        if my_word[i] == "_":
            if other_word[i] in my_word:
                return False
        elif my_word[i] != other_word[i]:
            return False
    return True


def show_possible_matches(my_word):
    """ Prints all possible words from wordlist that fit current pattern. """
    matches = [word for word in wordlist if match_with_gaps(my_word, word)]
    if matches:
        print("Possible word matches are:", " ".join(matches))
    else:
        print("No matches found")


# --- Game Implementation ---

def hangman_with_hints(secret_word):
    guesses_left = 6
    warnings_left = 3
    letters_guessed = []
    vowels = "aeiou"

    print("\n" + "=" * 30)
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print(f"You have {warnings_left} warnings left.")
    print("-" * 15)

    while guesses_left > 0:
        print(f"You have {guesses_left} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")

        user_input = input("Please guess a letter: ").lower().strip()

        # Hint Logic: User types '*'
        if user_input == "*":
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue

        # Input Validation (Warnings System)
        if not user_input.isalpha() or len(user_input) != 1:
            if warnings_left > 0:
                warnings_left -= 1
                msg = f"Oops! That is not a valid letter. You have {warnings_left} warnings left"
            else:
                guesses_left -= 1
                msg = "Oops! Not a valid letter. No warnings left, so you lose one guess"
            print(f"{msg}: {get_guessed_word(secret_word, letters_guessed)}")

        # Already Guessed Logic
        elif user_input in letters_guessed:
            if warnings_left > 0:
                warnings_left -= 1
                msg = f"Oops! You've already guessed that letter. You have {warnings_left} warnings left"
            else:
                guesses_left -= 1
                msg = "Oops! Already guessed. No warnings left, so you lose one guess"
            print(f"{msg}: {get_guessed_word(secret_word, letters_guessed)}")

        # Correct or Incorrect Guess
        else:
            letters_guessed.append(user_input)
            if user_input in secret_word:
                print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
            else:
                # Vowel Penalty: -2 guesses
                penalty = 2 if user_input in vowels else 1
                guesses_left -= penalty
                print(f"Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")

        print("-" * 15)

        # Win Condition
        if is_word_guessed(secret_word, letters_guessed):
            # Score = remaining guesses * unique letters
            unique_letters = len(set(secret_word))
            total_score = guesses_left * unique_letters
            print("Congratulations, you won!")
            print(f"Your total score for this game is: {total_score}")
            return True

    # Loss Condition
    print(f"Sorry, you ran out of guesses. The word was: {secret_word}")
    return False


# --- Main Entry Point with Play Again Loop ---

if __name__ == "__main__":
    print("DEBUG: Script started. Initializing...")
    wordlist = load_words()

    while True:
        secret_word = choose_word(wordlist)
        hangman_with_hints(secret_word)

        choice = input("\nWould you like to play again? (y/n): ").lower().strip()
        if choice != 'y':
            print("Thanks for playing! Goodbye.")
            break
        print("\n" + "=" * 30 + "\n")