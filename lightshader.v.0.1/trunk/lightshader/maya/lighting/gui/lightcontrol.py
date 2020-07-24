from lightshader.qt.interface import QtWidgets, QtCore, addBorder
from lightshader.maya.qt.base import BaseWindow
import sys


class LightControl(BaseWindow):
    def __init__(self, mainWindow):
        super(LightControl, self).__init__(mainWindow)
        self.title = 'Light Control'
        self.documentationUrl = self.documentationUrl + 'documentation/lightcontrol'
        self.resize(1350, 750)
        self.controlWidth = 300
        self._setupWindow()
        self._addWidgets()
        self._setupWidgets()
        self._setupConnections()

    def _setupWindow(self):
        super(LightControl, self)._setupWindow()
        self.baseLayout = QtWidgets.QHBoxLayout()
        self.controlLayout = QtWidgets.QVBoxLayout()
        self.lightList = QtWidgets.QListWidget()
        self.lightBox = QtWidgets.QGroupBox('Lights')
        self.lightBoxLayout = QtWidgets.QVBoxLayout()
        self.controlBox = QtWidgets.QGroupBox('Control')
        self.controlBoxLayout = QtWidgets.QVBoxLayout(self.controlBox)
        self.cameraBox = QtWidgets.QGroupBox('View')
        self.cameraBoxLayout = QtWidgets.QVBoxLayout(self.cameraBox)
        self.checkBoxLayout = QtWidgets.QHBoxLayout()
        self.lightEnableCheckbox = QtWidgets.QCheckBox('Enabled')
        self.useKelvinCheckbox = QtWidgets.QCheckBox('Kelvin')
        self.selectLightCheckbox = QtWidgets.QCheckBox('Select')
        self.lookThroughLightCheckbox = QtWidgets.QCheckBox('Look Through')
        self.lightCheckboxLayout = QtWidgets.QHBoxLayout()
        self.refreshButton = QtWidgets.QPushButton('Refresh')

    def _addWidgets(self):
        self.parentWidget.setLayout(self.baseLayout)
        self.baseLayout.addLayout(self.controlLayout)
        self.controlLayout.addWidget(self.lightBox)
        self.lightBox.setLayout(self.lightBoxLayout)
        self.controlLayout.addWidget(self.controlBox)
        self.baseLayout.addWidget(self.cameraBox)
        self.lightBoxLayout.addWidget(self.lightList)
        self.lightBoxLayout.addLayout(self.lightCheckboxLayout)
        self.lightCheckboxLayout.addWidget(self.selectLightCheckbox)
        self.lightCheckboxLayout.addWidget(self.lookThroughLightCheckbox)
        self.lightCheckboxLayout.addWidget(self.refreshButton)
        self.checkBoxLayout.addWidget(self.lightEnableCheckbox)
        self.checkBoxLayout.addWidget(self.useKelvinCheckbox)
        self.controlBoxLayout.addLayout(self.checkBoxLayout)

    def _setupWidgets(self):
        self.setObjectName('lcLightControl')
        self.baseLayout.setObjectName('lcBaseLayout')
        self.controlLayout.setObjectName('lcControlLayout')
        self.cameraBoxLayout.setObjectName('lcCameraBoxLayout')
        self.lightBoxLayout.setObjectName('lcLightBoxLayout')

        self.lightBox.setFixedHeight(self.height() / 3)
        self.controlBox.setFixedWidth(self.controlWidth)
        self.lightBox.setFixedWidth(self.controlWidth)
        self.lookThroughLightCheckbox.setChecked(True)
        self.selectLightCheckbox.setChecked(True)

        addBorder(self.lightBox)
        addBorder(self.controlBox)
        addBorder(self.cameraBox)
        self.lightList.setFocusPolicy(QtCore.Qt.NoFocus)

        self.cameraBox.setEnabled(False)
        self.controlBox.setEnabled(False)

        self.menuBar.editMenu.deleteLater()
        self.menuBar.viewMenu.deleteLater()

    def _setupConnections(self):
        self.Signal.addSignal(self.lightList, 'itemClicked', self.lightActivatedEvent)
        self.Signal.addSignal(self.lightList, 'itemChanged', self.lightActivatedEvent)
        self.Signal.addSignal(self.lightEnableCheckbox, 'toggled', self.lightEnableEvent)
        self.Signal.addSignal(self.useKelvinCheckbox, 'toggled', self.kelvinEnableEvent)
        self.Signal.addSignal(self.refreshButton, 'clicked', self.refreshLightListEvent)

    def lightActivatedEvent(self, *args, **kwargs):
        self.cameraBox.setEnabled(True)
        self.controlBox.setEnabled(True)
        pass

    def lightEnableEvent(self, *args, **kwargs):
        pass

    def kelvinEnableEvent(self, *args, **kwargs):
        pass

    def refreshLightListEvent(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    win = LightControl()
    win.show()
    sys.exit(app.exec_())
