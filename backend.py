import random
import threading
import time

class HangmanGame:
    def __init__(self, words, word_clues):
        self.words = words
        self.word_clues = word_clues
        self.word = ""
        self.clues = []
        self.clue_index = 0
        self.guesses_left = 6
        self.guessed_letters = []
        self.game_over = False
        self.winner = None
        self.hangman_stages = [
            """
              +---+
                  |
                  |
                  |
                 ===
            """,
            """
              +---+
              |   |
                  |
                  |
                 ===
            """,
            """
              +---+
              |   |
              O   |
                  |
                 ===
            """,
            """
              +---+
              |   |
              O   |
              |   |
                 ===
            """,
            """
              +---+
              |   |
              O   |
             /|   |
                 ===
            """,
            """
              +---+
              |   |
              O   |
             /|\\  |
                 ===
            """,
            """
              +---+
              |   |
              O   |
             /|\\  |
             /    ===
            """,
            """
              +---+
              |   |
              O   |
             /|\\  |
             / \\  ===
            """
        ]

    def generate_word(self):
        return random.choice(self.words)

    def start_game(self):
        self.word = self.generate_word()
        self.clues = self.word_clues.get(self.word, ["No clue available"])
        self.clue_index = 0
        self.guesses_left = 6
        self.guessed_letters = []
        self.game_over = False
        self.winner = None

    def guess_letter(self, letter):
        if self.game_over:
            return "Game Over. Please start a new game."

        if letter in self.guessed_letters:
            return "You've already guessed that letter."

        self.guessed_letters.append(letter)

        if letter in self.word:
            if all(letter in self.guessed_letters for letter in self.word):
                self.game_over = True
                self.winner = "Team"
                return "Congratulations! You guessed the word: " + self.word
            return "Correct guess! Keep going."
        else:
            self.guesses_left -= 1
            if self.guesses_left == 0:
                self.game_over = True
                return "Sorry, you're out of guesses. The word was: " + self.word
            return "Incorrect guess. Try again."


# Sample words and clues
words = ["apple", "banana", "orange", "grape", "strawberry"]
word_clues = {
    "apple": ["A fruit", "Grows on trees", "Comes in various colors", "Has seeds", "Used in pies"],
    "banana": ["Yellow fruit", "Rich in potassium", "Commonly eaten", "Peels easily", "Tropical fruit"],
    "orange": ["Citrus fruit", "Round in shape", "Rich in Vitamin C", "Juicy and sweet", "Orange peel"],
    "grape": ["Small fruit", "Grows in clusters", "Used to make wine", "Seedless varieties available", "Green or purple"],
    "strawberry": ["Red fruit", "Has seeds on the outside", "Sweet and juicy", "Often used in desserts", "Grows on vines"]
}

# Initialize the game
hangman_game = HangmanGame(words, word_clues)


def clue_thread():
    global hangman_game
    time.sleep(10)  # Wait for 10 seconds for the team to guess
    if not hangman_game.game_over:
        return hangman_game.clue


def check_guess(guess):
    global hangman_game
    return hangman_game.guess_letter(guess)


if __name__ == "__main__":
    choice = input("Enter 'moderator' or 'participant': ").lower()

    if choice == "participant":
        num_participants = int(input("Enter the number of participants (max 4): "))
        team_name = input("Enter team name: ")
        print(f"Team {team_name}, get ready to play!")
        hangman_game.start_game()
        print(f"Clue: {hangman_game.clues[0]}")
        print(f"Guesses left: {hangman_game.guesses_left}")

        while not hangman_game.game_over:
            guess = input("Guess a letter: ").lower()
            result = check_guess(guess)
            print(result)
            print(f"Guesses left: {hangman_game.guesses_left}")
            print(hangman_game.hangman_stages[6 - hangman_game.guesses_left])

            hangman_game.clue_index += 1
            if hangman_game.clue_index < len(hangman_game.clues):
                print(f"Next clue: {hangman_game.clues[hangman_game.clue_index]}")

        print(f"Game Over! {hangman_game.winner} wins!")

    elif choice == "moderator":
        word = input("Enter the word for the game: ")
        clues = []
        for i in range(6):
            clue = input(f"Enter clue {i+1}: ")
            clues.append(clue)

        print("Word and clues set. Let's play Hangman!")
        hangman_game.word = word
        hangman_game.clues = clues
        print(f"Clue: {hangman_game.clues[0]}")

        while not hangman_game.game_over:
            guess = input("Guess a letter: ").lower()
            result = check_guess(guess)
            print(result)
            print(f"Guesses left: {hangman_game.guesses_left}")
            print(hangman_game.hangman_stages[6 - hangman_game.guesses_left])

            hangman_game.clue_index += 1
            if hangman_game.clue_index < len(hangman_game.clues):
                print(f"Next clue: {hangman_game.clues[hangman_game.clue_index]}")

        print(f"Game Over! {hangman_game.winner} wins!")


