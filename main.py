import sys
from PyQt5.QtWidgets import QApplication
from kiwoom.kiwoom import Kiwoom


class Main():

    def __init__(self):

        # 프로그램이 종료되지 않는 동시성 처리가 가능하도록 구성
        self.app = QApplication(sys.argv)
        self.kiwoom = Kiwoom()
        self.app.exec_()


if __name__ == "__main__":
    Main()