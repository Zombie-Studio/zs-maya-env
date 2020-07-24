from lightshader.qt.interface import QtWidgets, QtCore, addBorder, Signal
from lightshader.maya.qt.base import BaseWindow
import lightshader.maya.lighting.gui.subclass as subclass


class AovControl(BaseWindow):
    def __init__(self, mainWindow):
        super(AovControl, self).__init__(mainWindow)
        self.title = 'AOV Control'
        self.documentationUrl = self.documentationUrl + 'documentation/aovcontrol/'
        self.resize(550, 800)
        self.lightBoxHeight = 150
        self._setupWindow()
        self._addWidgets()
        self._setupWidgets()
        self._extendMenu()

    def _setupWindow(self):
        super(AovControl, self)._setupWindow()
        self.baseLayout = QtWidgets.QVBoxLayout()
        self.lightList = QtWidgets.QListWidget()
        self.aovList = QtWidgets.QListWidget()
        self.lightBox = QtWidgets.QGroupBox('Lights')
        self.aovBox = QtWidgets.QGroupBox('AOVs')
        self.lightBoxLayout = QtWidgets.QVBoxLayout(self.lightBox)
        self.aovBoxLayout = QtWidgets.QVBoxLayout(self.aovBox)

    def _addWidgets(self):
        self.parentWidget.setLayout(self.baseLayout)
        self.baseLayout.addWidget(self.aovBox)
        self.baseLayout.addWidget(self.lightBox)
        self.lightBoxLayout.addWidget(self.lightList)
        self.aovBoxLayout.addWidget(self.aovList)

    def _setupWidgets(self):
        self.lightBox.setFixedHeight(self.lightBoxHeight)
        addBorder(self.lightBox)
        addBorder(self.aovBox)

    def _extendMenu(self):
        pass