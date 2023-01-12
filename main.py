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

from board import Board


class PlayWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('TicTacToe - Play')
        self.board = Board()
        self.ismove = False

        layouts = [QVBoxLayout(), QVBoxLayout(), QVBoxLayout()]

        buttons = [[QPushButton(), QPushButton(), QPushButton()],
                   [QPushButton(), QPushButton(), QPushButton()],
                   [QPushButton(), QPushButton(), QPushButton()]]

        fin_layout =QHBoxLayout()

        for x in range(3):
            for y in range(3):
                layouts[x].addWidget(buttons[x][y])
                buttons[x][y].setFixedSize(QSize(50,50))


        widgets=[]
        for i in range(3):
            widgets.append(QWidget())
            widgets[i].setLayout(layouts[i])
            fin_layout.addWidget(widgets[i])

        # for x in range(2):
        #     for y in range(2):
        #         buttons[x][y].clicked.connect()

        widget = QWidget()
        widget.setLayout(fin_layout)

        self.setCentralWidget(widget)

    def field_clicked(self, x, y):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TicTacToe - Main')

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
        self.play_window=PlayWindow()
        self.play_window.show()

    def newgame_comp(self):
        self.play_window=PlayWindow()
        self.play_window.show()

    def press_exit(self):
        self.close()


app = QApplication(sys.argv)
# app=QApplication([])
main_window = MainWindow()
main_window.show()
app.exec()
