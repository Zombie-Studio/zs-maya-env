from lightshader.qt.interface import QtWidgets, QtCore, addBorder, Signal


class ListWidget(QtWidgets.QListWidget):
    def __init__(self):
        super(ListWidget, self).__init__()
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet("""

        QListWidget::item {
            background: rgb(30,30,30); 
            color: rgb(70,70,70);
        }

        QListWidget::item:selected {
            background: rgb(45,45,45);
            color: rgb(200,200,200);

        }

        QListWidget {
            background: rgb(45,45,45);
        }

        """)

    def allItems(self):
        allItems = list()
        for row in range(self.count()):
            allItems.append(self.item(row))
        return allItems


class RandomDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(RandomDialog, self).__init__(parent)
        self.Signal = Signal()
        self.__value = None
        self._setupWidgets()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def _setupWidgets(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.controlLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.minSlider = QtWidgets.QDoubleSpinBox()
        self.maxSlider = QtWidgets.QDoubleSpinBox()
        self.cancelButton = QtWidgets.QPushButton('Cancel')
        self.setButton = QtWidgets.QPushButton('Set')

        self._addWidgets()
        self._editWidgets()

    def _addWidgets(self):
        self.layout.addLayout(self.controlLayout)
        self.layout.addLayout(self.buttonLayout)
        self.controlLayout.addWidget(self.minSlider)
        self.controlLayout.addWidget(self.maxSlider)
        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.setButton)

    def _editWidgets(self):
        self.setLayout(self.layout)

        for control in [self.minSlider, self.maxSlider]:
            control.setFixedSize(100, 25)
            control.setMaximum(999999)
            control.setMinimum(-999999)
            control.setSingleStep(0.01)
            control.setDecimals(3)

        self.Signal.addSignal(self.cancelButton, 'clicked', self.closeSignalEvent)
        self.Signal.addSignal(self.setButton, 'clicked', self.setSignalEvent)

    def closeSignalEvent(self, *args):
        self.close()

    def setSignalEvent(self, *args):
        self.value = random.uniform(self.minSlider.value(), self.maxSlider.value())
        self.close()

    def randomize(self):
        return random.uniform(self.minSlider.value(), self.maxSlider.value())