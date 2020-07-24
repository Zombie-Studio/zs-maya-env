import sys
from lightshader.qt.interface import QtWidgets, QtCore, Signal
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from lightshader.qt.interface import AboutDialog, ReportDialog
from lightshader.general import openUrl


class BaseWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, mainWindow):
        super(BaseWindow, self).__init__(mainWindow)
        self.setParent(mainWindow)
        self.setWindowTitle('Base Window')
        self.resize(500, 400)
        self.menuBar = BaseMenu()
        self.Signal = Signal()
        self._setupWindow()
        self.setupSignals()
        self.setWindowFlags(QtCore.Qt.Window)
        self.setProperty("saveWindowPref", True)
        self.AboutDialog = AboutDialog()
        self.ReportDialog = ReportDialog()
        self._documentationUrl = 'http://lightshader.de/'

    @property
    def documentationUrl(self):
        return self._documentationUrl

    @documentationUrl.setter
    def documentationUrl(self, value):
        self._documentationUrl = value

    def _dockCleanUp(self):
        import pymel.core as pmc
        control = self.objectName() + 'WorkspaceControl'
        if pmc.workspaceControl(control, q=True, exists=True):
            pmc.workspaceControl(control, e=True, close=True)
            pmc.deleteUI(control, control=True)

    def _setupWindow(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)
        self._mainLayout = QtWidgets.QVBoxLayout(centralWidget)
        self._mainLayout.setContentsMargins(2, 2, 2, 2)
        centralWidget.setLayout(self._mainLayout)
        self.parentWidget = QtWidgets.QGroupBox()
        self.parentWidget.setObjectName("parentWidgetBox")
        centralWidget.setObjectName('centralWidget')
        self._mainLayout.setObjectName('baseMainLayout')
        self._mainLayout.addWidget(self.parentWidget)
        self.setMenuBar(self.menuBar)
        self.statusBar()

    def setupSignals(self):
        self.Signal.addSignal(self.menuBar.fileMenu, 'triggered', self.handleSignals)
        self.Signal.addSignal(self.menuBar.viewMenu, 'triggered', self.handleSignals)
        self.Signal.addSignal(self.menuBar.helpMenu, 'triggered', self.handleSignals)

    def handleSignals(self, obj, *args):
        msg = 'Signal fired'
        if isinstance(args[0], QtWidgets.QAction):
            actionName = args[0].text()
            msg = '{} triggered'.format(actionName)
            if actionName == 'Exit':
                self.close()
            elif actionName == 'About':
                self.AboutDialog.show()
            elif actionName == 'Documentation':
                openUrl(self.documentationUrl)
            elif actionName == 'Report':
                self.ReportDialog.openBrowser()
        self.statusBar().showMessage(msg, 2000)

    @property
    def title(self):
        return self.windowTitle()

    @title.setter
    def title(self, windowTitle):
        self.setWindowTitle(windowTitle)


class BaseMenu(QtWidgets.QMenuBar):
    def __init__(self):
        super(BaseMenu, self).__init__()
        self.fileMenu = QtWidgets.QMenu('File')
        self.editMenu = QtWidgets.QMenu('Edit')
        self.viewMenu = QtWidgets.QMenu('View')
        self.helpMenu = QtWidgets.QMenu('Help')
        self.addMenu(self.fileMenu)
        self.addMenu(self.editMenu)
        self.addMenu(self.viewMenu)
        self.addMenu(self.helpMenu)
        self.setNativeMenuBar(False)
        self.Signal = Signal()
        self.addMenuItems()

    def addMenuItems(self):
        self.viewMenu.addAction('Reset')
        self.fileMenu.addAction('Exit')
        self.helpMenu.addAction('Report')
        self.helpMenu.addAction('Documentation')
        self.helpMenu.addSeparator()
        self.helpMenu.addAction('About')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    win = BaseWindow(mainWindow)
    win.show()
    sys.exit(app.exec_())
