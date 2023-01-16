import sys

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (QApplication,
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
                             QDateTimeEdit,
                             QDial, QDoubleSpinBox, QFontComboBox,
                             QLabel, QLCDNumber, QLineEdit, QMainWindow,
                             QProgressBar, QPushButton,
                             QRadioButton, QSlider, QSpinBox, QTimeEdit, QVBoxLayout, QHBoxLayout,
                             QWidget, QDialog)
import random

stats = [0, 0, 0]
game_count = 0
name = ''

from board import Board


class PlayWindow(QDialog):

    def __init__(self, main_win_ref, pl, computer_random_start):
        super().__init__()
        self.setWindowTitle('TicTacToe - Play')
        self.main_win_ref = main_win_ref
        self.board = Board()
        self.computer_random_start = computer_random_start

        self.humanmove = abs(pl - 2)
        self.iswin = False
        self.isdrawn = False

        self.human_pl = pl
        self.comp_pl = 1 if self.human_pl == 2 else 2

        layouts = [QHBoxLayout(), QHBoxLayout(), QHBoxLayout()]

        self.buttons = [[QPushButton(), QPushButton(), QPushButton()],
                        [QPushButton(), QPushButton(), QPushButton()],
                        [QPushButton(), QPushButton(), QPushButton()]]

        self.fin_layout = QVBoxLayout()

        for x in range(3):
            for y in range(3):
                layouts[x].addWidget(self.buttons[x][y])
                self.buttons[x][y].setFixedSize(QSize(50, 50))

        widgets = []
        self.label0 = QLabel(f"Game Tic Tac Toe, {game_count} play")
        self.label1 = QLabel(f"")
        self.fin_layout.addWidget(self.label0)

        for i in range(3):
            widgets.append(QWidget())
            widgets[i].setLayout(layouts[i])
            self.fin_layout.addWidget(widgets[i])

        self.fin_layout.addWidget(self.label1)

        for x in range(3):
            for y in range(3):
                self.buttons[x][y].clicked.connect(self.field_clicked_wrap(y, x))

        self.setLayout(self.fin_layout)

        self.show_board()

        if not self.humanmove:
            self.computer_move()

    def show_board(self):
        for x in range(3):
            for y in range(3):
                self.buttons[x][y].setText(self.board.player_chars[self.board[x][y]])
                if (x, y) in self.board.win_cells:
                    font = self.buttons[x][y].font()
                    font.setBold(True)
                    font.setPointSize(20)
                    self.buttons[x][y].setFont(font)

    def gameover_check(self):
        self.iswin = self.board.checkwin_all_players(2)
        self.isdrawn = self.board.full()
        if self.iswin or self.isdrawn:
            self.finish()
            return True

    def finish(self):
        if self.comp_pl in self.board.win_players:
            text = 'Computer wins! Good luck next time!'
            stats[1] += 1
        elif self.human_pl in self.board.win_players:
            text = f'{name} you win! Congratulations!'
            stats[0] += 1
        else:
            text = "It's a DRAWN! Good luck next time!"
            stats[2] += 1
        self.main_win_ref.show_score()
        closebutton = QPushButton('Exit')
        self.fin_layout.addWidget(QLabel(text))
        self.fin_layout.addWidget(QLabel(""))
        self.fin_layout.addWidget(closebutton)
        closebutton.clicked.connect(self.close_win)
        for x in range(3):
            for y in range(3):
                self.buttons[x][y].clicked.disconnect()

    def close_win(self):
        self.close()

    def computer_move(self):
        if self.computer_random_start:
            comp_vars = []
            for xx in range(3):
                for yy in range(3):
                    if not self.board[xx][yy]:
                        comp_vars.append((xx, yy))
            self.computer_random_start = False
        else:
            comp_vars = self.board.computer_move(self.comp_pl, silent=True)

        xx, yy = random.choice(comp_vars)

        self.board[xx][yy] = self.comp_pl

        if not self.gameover_check():
            self.humanmove = True
        self.show_board()

    def field_clicked_wrap(self, x, y):
        def wrap():
            if self.humanmove:
                # self.label1.setText(f"x={x} , y={y}")
                if self.board.try_move(y, x, self.human_pl):
                    if not self.gameover_check():
                        self.humanmove = False
                        self.computer_move()
                    else:
                        self.show_board()
                else:
                    return

        return wrap


class MainWindow(QMainWindow):
    def __init__(self, user_name):
        super().__init__()
        self.setWindowTitle(f'Welcome to TicTacToe, {user_name}')
        self.isplay = False

        layoutH = QHBoxLayout()
        self.buttons = [QPushButton(), QPushButton(), QPushButton()]

        for button in self.buttons:
            layoutH.addWidget(button)

        self.buttons[0].setText(f"{name} first")
        self.buttons[0].clicked.connect(self.newgame_human)
        self.buttons[1].setText("Computer first")
        self.buttons[1].clicked.connect(self.newgame_comp)
        self.buttons[2].setText("exit")
        self.buttons[2].clicked.connect(self.press_exit)

        button_widget = QWidget()
        button_widget.setLayout(layoutH)

        layoutV = QVBoxLayout()
        self.labels = [QLabel() for i in range(5)]
        self.labels[0].setText(f"{user_name} welcome to Tic tac toe!")
        self.labels[0].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labels[0].setMinimumHeight(15)
        self.labels[4].setText(f"You played {game_count} games. New game ?")
        self.labels[4].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labels[4].setMinimumHeight(15)
        self.show_score()

        self.randomonchek = QCheckBox("First computer move is random")
        self.randomonchek.setCheckState(Qt.CheckState.Checked)

        widgets = [*self.labels, button_widget, self.randomonchek]

        for item in widgets:
            layoutV.addWidget(item)

        widget = QWidget()
        widget.setLayout(layoutV)

        self.setCentralWidget(widget)

    def show_score(self):
        self.labels[1].setText(f'{name} wins: {stats[0]}')
        self.labels[2].setText(f'Computer wins: {stats[1]}')
        self.labels[3].setText(f'Draws: {stats[2]}')
        self.labels[4].setText(f"You played {game_count} games. New game ?")

    def newgame(self, pl):
        global game_count
        game_count += 1
        computer_first_move_random = self.randomonchek.checkState() == Qt.CheckState.Checked
        self.play_window = PlayWindow(self, pl, computer_first_move_random)
        self.isplay = True

        self.play_window.setModal(True)
        self.play_window.show()

    def newgame_human(self):
        self.newgame(1)

    def newgame_comp(self):
        self.newgame(2)

    def press_exit(self):
        self.close()


class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TicTacToe - Main')

        self.textfield = QLineEdit()
        self.textfield.setMinimumWidth(70)

        self.textfield.returnPressed.connect(self.enter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('Welcome to Tic Tac Toe game'))
        main_layout.addWidget(QLabel('Please enter your name'))
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel('name:'))
        name_layout.addWidget(self.textfield)
        enter_button = QPushButton('Ok')
        name_layout.addWidget(enter_button)
        enter_button.clicked.connect(self.enter)
        name_widget = QWidget()
        name_widget.setLayout(name_layout)
        main_layout.addWidget(name_widget)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def enter(self):
        if len(self.textfield.text()) > 0:
            global name
            name = self.textfield.text()
            self.main_window = MainWindow(name)
            self.main_window.show()
            self.close()


app = QApplication(sys.argv)

welcome_window = WelcomeWindow()
welcome_window.show()
# main_window = MainWindow(name)
# main_window.show()
# play_window=PlayWindow(main_window,1)
# play_window.show()

app.exec()
