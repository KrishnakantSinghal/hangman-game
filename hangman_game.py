"""
hangman_game
"""

# Import necessary modules
import random
from wonderwords import RandomWord
import nltk
from nltk.corpus import wordnet

# Check if WordNet is already downloaded and up-to-date
try:
    wordnet.ensure_loaded()
except LookupError:
    # WordNet is not downloaded or not up-to-date
    print("Downloading WordNet...")
    print("------------------------------------------ \n")
    nltk.download("wordnet")


def wordnet_synsets(word):
    """
    Get all word synsets for a word
    """
    return wordnet.synsets(word)


def get_word_meaning(word_dict):
    """
    Getting the meaning and description of a word
    """
    # Get the definition of the word's synset
    definition = word_dict["synset"].definition().capitalize()

    # Get the first example of the word's synset
    examples = word_dict["synset"].examples()

    # Print the meaning and example
    print(f"""Meaning of "{word_dict['word']}": {definition}""")
    if examples:
        print(f"Example: {examples[0].capitalize()}")


def choose_word():
    """Choose a random word for the game"""
    random_word = RandomWord()

    # Generate a random verb with length between 3 and 6 characters
    word = random_word.word(
        word_min_length=3,
        word_max_length=6,
        include_parts_of_speech=["verbs"],
    )

    # Get synsets for the chosen word
    synsets = wordnet.synsets(word)

    # Choose a random synset from the list
    random_index = random.randint(0, len(synsets) - 1)
    synset = synsets[random_index]

    # Use the lemma name of the first synset as the word
    word = synset.lemma_names()[0]

    # Create a dictionary with the word and its synset
    word_dict = {"word": word, "synset": synset}

    # Return the dictionary
    return word_dict


def display_word(word, guessed_letters):
    """
    Display the word with blanks for unguessed letters
    """
    display = ""
    for index, letter in enumerate(word):
        if index % 2 == 1 or letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "
    return display.strip()


def set_initial_guessed_letters(word):
    """
    Set guessed letters initially for odd positions of word
    """
    guessed_letters = []
    for letter in word:
        if word.find(letter) % 2 == 1:
            guessed_letters.append(letter)
    return guessed_letters


def hangman():
    """
    Main function for the Hangman game
    """
    print("Welcome to Hangman!")
    print("------------------------------------------ \n")
    print("Guess the word (verb)")
    print("------------------------------------------ \n")

    # Choose a word for the game
    word_dict = choose_word()
    word_to_guess = word_dict["word"]

    # Track guessed letters
    guessed_letters = set_initial_guessed_letters(word_to_guess)

    # Maximum number of incorrect guesses allowed
    max_attempts = 6
    attempts = 0

    # Print a hint using the definition of the word's synset
    print("HINT: ", word_dict["synset"].definition().capitalize())
    print("------------------------------------------ \n")

    # Main game loop
    while attempts < max_attempts:
        # Display current status of the word
        print("\nWord:", display_word(word_to_guess, guessed_letters))
        print("------------------------------------------ \n")

        # Prompt the user for a letter guess
        guess = input("Enter a letter: ").lower()

        # Check if the guess is a single letter
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a valid single letter.")
            print("------------------------------------------ \n")
            continue

        # Check if the letter has already been guessed
        if guess in guessed_letters:
            print("You've already guessed that letter. Try again.")
            print("------------------------------------------ \n")
            continue

        # Add the guessed letter to the list
        guessed_letters.append(guess)

        # Check if the guessed letter is in the word
        if guess not in word_to_guess:
            attempts += 1
            print("Incorrect guess! Attempts left:", max_attempts - attempts)
            print("------------------------------------------ \n")

        # Check if the word has been completely guessed
        if set(word_to_guess).issubset(set(guessed_letters)):
            print("Congratulations! You guessed the word:", word_to_guess)
            print("------------------------------------------ \n")
            get_word_meaning(word_dict)
            break

    # If all attempts are used up
    if attempts == max_attempts:
        print("Sorry, you ran out of attempts. The word was:", word_to_guess)
        print("------------------------------------------ \n")
        get_word_meaning(word_dict)


# Run the Hangman game
hangman()
