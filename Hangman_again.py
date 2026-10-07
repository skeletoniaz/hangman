import sys
import random
import requests
from PyQt5.QtWidgets import QApplication , QLabel , QPushButton , QTextEdit, QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

class Hangman(QWidget):
    def __init__(self):
        super().__init__ ()
        self.output_screen = QLabel("",self)
        self.output_screen.setObjectName("output_screen")
        self.hint_screen = QLabel("",self)
        self.hint_screen.setObjectName("hint_screen")

        self.input = QTextEdit()
        self.input.setObjectName("input")
        self.submit_button = QPushButton("SUBMIT",self)
        self.submit_button.setObjectName("submit_button")

        self.hangman_art = {
            0: """
               
               
               """,
            1: """
                O 
               
               """,
            2: """
                O 
                | 
               """,
            3: """
                O 
               /| 
               """,
            4: """
                O 
               /|\\
               """,
            5: """
                O 
               /|\\
               /  
               """,
            6: """
                O 
               /|\\
               / \\
               """
        }

        
        self.CSS()

    def CSS(self):
        self.output_screen.setFixedSize(450,250)
        self.hint_screen.setFixedSize(300,50)

        self.input.setFixedSize(200,50)
        self.input.setPlaceholderText("Enter a letter")

        self.submit_button.setFixedSize(50,50)
        self.setStyleSheet("""
                            Hangman{
                                background-color : #42f5a7;
                            }
                            QTextEdit{
                                font-size : 20 px
                            }
                            QPushButton#submit_button{
                                        min-width: 50px;
                                        max-width: 50px;
                                        min-height: 50px;
                                        max-height: 50px;
                            
                                        background-color : #a3c4fa;
                            }
                            QLabel#hint_screen{
                                        background-color : #ed4e4e;
                                        font-size : 25 px;
                            }
                            QLabel#output_screen{
                                background-color : #5cb0ff;
                                font-size : 25 px;
                            }
                            QTextEdit{
                                background-color : #5cb0ff;
                            }
                            """)
        
        self.setWindowTitle("HANGMAN")
        self.setGeometry(1400,200,500,400)
        self.setFixedSize(500,400)
        self.setWindowIcon(QIcon("Python/GUI/smug face.png"))

        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox1.addWidget(self.output_screen)
        hbox2.addWidget(self.hint_screen)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.input)
        hbox3.addWidget(self.submit_button)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        self.setLayout(vbox)
        self.output_screen.setAlignment(Qt.AlignCenter)
        self.hint_screen.setAlignment(Qt.AlignCenter)
        self.randomize()

    def randomize(self):
        url = requests.get('https://api.periodictableofelements.org/elements/')
        elements = url.json()

        random_element = random.choice(elements)
        self.element_name = str(random_element['name'])

        self.answer = str(self.element_name).lower()
        self.hint = ["_"] * len(self.answer)
        self.wrong_guesses = int(0)
        self.guessed = []
        self.hint_screen.setText(" ".join(self.hint))
        self.submit_button.clicked.connect(self.game)
        self.start()

    def start(self):
        self.input.clear()

    def display_man(self,wrong_guesses):
        art = "".join(self.hangman_art[wrong_guesses])
        self.output_screen.setText(art)

    def game(self):
        guess = self.input.toPlainText()
        self.input.clear()
        if guess.isalpha() == False or len(guess) > 1:
            self.output_screen.setText("Invalid guess")
            return
        if guess in self.guessed:
            self.output_screen.setText("Already guessed")
            return
        self.guessed.append(guess)
        if guess in self.answer:
            for index in range(len(self.answer)):
                if self.answer[index] == guess:
                        self.hint[index] = guess
        else:
            self.wrong_guesses += 1
            self.display_man(self.wrong_guesses)

        if self.wrong_guesses == len(self.hangman_art) -1:
            self.output_screen.setText(f"YOU LOSE answer was {self.answer.capitalize()}")
            self.input.hide()
            self.submit_button.hide()

        if "_" not in self.hint:
            self.output_screen.setText(f"YOU WIN, Took {len(self.guessed)} guesses, Answer was {self.answer.capitalize()}")
            self.input.hide()
            self.submit_button.hide()
        self.hint_screen.setText(" ".join(self.hint))
        return

def main():
    app = QApplication(sys.argv) 
    window = Hangman() 
    window.show() 
    sys.exit(app.exec_()) 

if __name__ == '__main__':
    main()