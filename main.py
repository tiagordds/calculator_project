import sys

from main_window import MainWindow
from display import Display, setupTheme, Info
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from variables import WINDOW_ICON_PATH
from buttons import ButtonsGrid

if __name__ == '__main__':

    # Cria a aplicação
    app = QApplication(sys.argv)
    window = MainWindow()
    setupTheme()

    # Define o ícone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # Info
    info = Info('Your equation')
    window.addWidgetToVLayout(info)

    # Display
    display = Display()
    window.addWidgetToVLayout(display)
    # Grid
    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)

    # Button

    # Executa a aplicação
    window.adjustFixedSize()
    window.show()
    app.exec()
