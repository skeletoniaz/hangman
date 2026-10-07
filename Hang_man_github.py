import random

hangman_art = {0:("   ",
                  "   ",
                  "   "),
               1:(" O ",
                  "   ",
                  "   "),
               2:(" O ",
                  " | ",
                  "   "),
               3:(" O ",
                  "/|", 
                  "   "),
               4:(" O ",
                  "/|\\",
                  "   "),
               5:(" O ",
                  "/|\\",
                  "/  "),
               6:(" O ",
                  "/|\\",
                  "/|\\"),}

import requests

url = requests.get('https://api.periodictableofelements.org/elements/')
elements = url.json()

random_element = random.choice(elements)
element_name = random_element['name']

def display_man(wrong_guesses):
    print("-----------------------------")
    for section in hangman_art[wrong_guesses]:
        print(section)
    print("-----------------------------")

def display_hint(hint):
    print(" ".join(hint))

def display_answer(answer):
    print(" ".join(answer))
    
    
def main():
    answer = element_name
    hint = ["_"] * len(answer)
    wrong_guesses = 0
    guessed = []

    while True:
        display_hint(hint)
        guess = input("Enter a letter: ").lower()
        while guess.isalpha() == False or len(guess)  > 1:
            print("Invalid guess")
            guess = input("Enter a letter: ").lower()
        while guess in guessed:
            print("Already guessed")
            guess = input("Enter a letter: ").lower()
        guessed.append(guess)
        if guess in answer:
            for index in range(len(answer)):
                if answer[index] == guess:
                    hint[index] = guess
        else:
            wrong_guesses += 1
        display_man(wrong_guesses)

        if wrong_guesses == len(hangman_art) -1:
            print("YOU LOSE")
            print(f"The answer was {answer.capitalize()}")
            break

        if "_" not in hint:
            print("YOU WIN")
            print(f"You took {len(guessed)} guesses")
            print(f"The answer was {answer.capitalize()}")
            break

if __name__ == '__main__':
    main()