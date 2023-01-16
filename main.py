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
                             QWidget, )

stats = [0, 0, 0]
game_count = 0
name = ''

from board import Board


class PlayWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('TicTacToe - Play')
        self.board = Board()
        self.ismove = False

        layouts = [QHBoxLayout(), QHBoxLayout(), QHBoxLayout()]

        self.buttons = [[QPushButton(), QPushButton(), QPushButton()],
                        [QPushButton(), QPushButton(), QPushButton()],
                        [QPushButton(), QPushButton(), QPushButton()]]

        fin_layout = QVBoxLayout()

        for x in range(3):
            for y in range(3):
                layouts[x].addWidget(self.buttons[x][y])
                self.buttons[x][y].setFixedSize(QSize(50, 50))

        widgets = []
        self.label0 = QLabel(f"Game Tic Tac Toe, {game_count} play")
        self.label1 = QLabel(f"---")
        fin_layout.addWidget(self.label0)

        for i in range(3):
            widgets.append(QWidget())
            widgets[i].setLayout(layouts[i])
            fin_layout.addWidget(widgets[i])

        fin_layout.addWidget(self.label1)

        for x in range(3):
            for y in range(3):
                self.buttons[x][y].clicked.connect(self.field_clicked_wrap(y, x))

        widget = QWidget()
        widget.setLayout(fin_layout)

        self.setCentralWidget(widget)

    # @xy_decor_wrap()
    def field_clicked_wrap(self, x, y):
        x_in = x
        y_in = y

        def wrap():
            self.label1.setText(f"x={x} , y={y}")
            pass

        return wrap


class MainWindow(QMainWindow):
    def __init__(self, user_name):
        super().__init__()
        self.setWindowTitle(f'Welcome to TicTacToe, {user_name}')
        self.isplay = False

        layoutH = QHBoxLayout()
        buttons = [QPushButton(), QPushButton(), QPushButton()]

        for button in buttons:
            layoutH.addWidget(button)

        buttons[0].setText("Human first")
        buttons[0].clicked.connect(self.newgame_human)
        buttons[1].setText("Computer first")
        buttons[1].clicked.connect(self.newgame_comp)
        buttons[2].setText("exit")
        buttons[2].clicked.connect(self.press_exit)

        button_widget = QWidget()
        button_widget.setLayout(layoutH)

        layoutV = QVBoxLayout()
        self.labels = [QLabel() for i in range(5)]
        self.labels[0].setText("Tic tac toe game!")
        self.labels[0].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labels[0].setMinimumHeight(15)
        self.labels[4].setText("New game ?")
        self.labels[4].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labels[4].setMinimumHeight(15)
        self.show_score()

        widgets = [*self.labels, button_widget]

        for item in widgets:
            layoutV.addWidget(item)

        widget = QWidget()
        widget.setLayout(layoutV)

        self.setCentralWidget(widget)

    def show_score(self):
        self.labels[1].setText(f'You wins: {stats[0]}')
        self.labels[2].setText(f'Computer wins: {stats[1]}')
        self.labels[3].setText(f'Draws: {stats[2]}')

    def newgame_human(self):
        self.play_window = PlayWindow(self, human)
        self.play_window.show()
        self.isplay = True

    def newgame_comp(self):
        self.play_window = PlayWindow()
        self.play_window.show()

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
            name=self.textfield.text()
            self.main_window = MainWindow(name)
            self.main_window.show()
            self.close()


app = QApplication(sys.argv)
# app=QApplication([])
welcome_window = WelcomeWindow()
welcome_window.show()
# main_window = MainWindow()
# main_window.show()
# play_window=PlayWindow()
# play_window.show()
app.exec()
