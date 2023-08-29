from PySide6.QtWidgets import QPushButton, QGridLayout
import math
from variables import MEDIUM_FONT_SIZE
from utils import isEmpty, isNumOrDot, isValidNumber
from PySide6.QtCore import Slot
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from display import Display
    from main_window import MainWindow
    from display import Info


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow',
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitialValue = ' '
        self._left = None
        self._right = None
        self._operator = None

        self.equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._equal)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insterToDisplay)
        self.display.operatorPressed.connect(self._configLeftOperation)

        for rowNumber, row in enumerate(self._gridMask):
            for columnNumber, buttonText in enumerate(row):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                self.addWidget(button, rowNumber, columnNumber)
                slot = self._makeSlot(self._insterToDisplay, buttonText)
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        if text == '◀':
            self._connectButtonClicked(button, self.display.backspace)

        if text == 'N':
            self._connectButtonClicked(button, self._invertNumber)

        if text in '+-/*^':
            self._connectButtonClicked(
                button,
                self._makeSlot(self._configLeftOperation, text)
            )

        if text == '=':
            self._connectButtonClicked(button, self._equal)

    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        new_Number = (float(displayText) * -1)
        self.display.setText(str(new_Number))

    @Slot()
    def _insterToDisplay(self, text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._operator = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _backspace(self):
        self.display.backspace()

    @Slot()
    def _configLeftOperation(self, text):
        displayText = self.display.text()  # The left number of the equation
        self.display.clear()  # This clears the display

        # If the display is empty or not a number
        if not isValidNumber(displayText) and self._left is None:
            self._showError('No number to operate.')
            return

        # If the left value is a number,
        # wait for the right value.
        if self._left is None:
            self._left = float(displayText)

        self._operator = text
        self.equation = f'{self._left} {self._operator} ?'

        self.display.setFocus()

    @Slot()
    def _equal(self):
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None:
            self._showError('Please, enter a valid operation.')
            return

        self._right = float(displayText)
        self.equation = f'{self._left} {self._operator} {self._right}'
        result = 'error'
        try:
            if '^' in self.equation and isinstance(self._left, float):
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError('Division by zero')
            self._clear()
        except OverflowError:
            self._showError('Infinity')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None
        self.display.setFocus()

        if result == 'error':
            self._left = None

    # @Slot()
    # def _backspace(self):
    #     self.display.backspace()
    #     print('to no backspace')

    def _showError(self, text):
        msgBox = self.window.MakeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.NoIcon)

        msgBox.setStandardButtons(
            msgBox.StandardButton.Ok
        )

        msgBox.exec()
        self.display.setFocus()
