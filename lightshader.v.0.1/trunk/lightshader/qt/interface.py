from PySide2 import QtGui, QtCore, QtWidgets
from functools import partial
import shiboken2
from lightshader.general import openUrl
import os
from lightshader.general import systemInfo
import warnings
import webbrowser

ROOT_DIR = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
ICON_DIR = os.path.join(ROOT_DIR, 'icons')


class LSMenu(QtWidgets.QMenu):
    def __init__(self, menuBar):
        super(LSMenu, self).__init__('Lightshader', parent=menuBar)
        # Setting class defaults
        self.setWindowTitle('Lightshader')
        self.setTearOffEnabled(True)
        self.menuBar = menuBar
        self.Signal = Signal()
        self.AboutDialog = AboutDialog()
        self.ReportDialog = ReportDialog()
        self._documentationUrl = 'http://lightshader.de/'
        self.setupMenu()

    def setupMenu(self):
        child = None
        for child in self.menuBar.children():
            if isinstance(child, QtWidgets.QMenu):
                if 'Help' in child.title():
                    break
        self.menuBar.insertMenu(child.menuAction(), self)
        self._addMenu()
        self._addActions()
        self._setupSignals()

    def _addMenu(self):
        self.debugMenu = QtWidgets.QMenu('Debug')

    def _addActions(self):
        self.addAction('Report')
        self.addAction('Documentation')
        self.addSeparator()
        self.addAction('About')

    def _setupSignals(self):

        self.Signal.addSignal(self, 'triggered', self.handleSignals)

    def handleSignals(self, obj, action, *args):
        if isinstance(action, QtWidgets.QAction):
            actionName = action.text()
            if actionName == 'Report':
                self.ReportDialog.openBrowser()
            elif actionName == 'Documentation':
                openUrl(self._documentationUrl)
            elif actionName == 'About':
                self.AboutDialog.show()
            else:
                print '{} triggered'.format(actionName)

class AboutDialog(QtWidgets.QDialog):
    def __init__(self):
        super(AboutDialog, self).__init__()
        self.setWindowTitle('About')
        self.setFixedSize(520, 400)
        self.Signal = Signal()

        self._setupWindow()

    def _setupWindow(self):
        self.aboutLayout = QtWidgets.QHBoxLayout(self)
        self.leftBox = QtWidgets.QGroupBox()
        self.infoBox = QtWidgets.QGroupBox()
        self.infoLayout = QtWidgets.QVBoxLayout(self.infoBox)
        self.leftLayout = QtWidgets.QVBoxLayout(self.leftBox)
        self.textField = QtWidgets.QTextEdit()
        self.closeButton = QtWidgets.QPushButton('Close')
        self.logoLabel = QtWidgets.QLabel()

        self._addWidgets()
        self._setupWidgets()

    def _addWidgets(self):
        self.aboutLayout.addWidget(self.leftBox)
        self.aboutLayout.addWidget(self.infoBox)
        self.infoLayout.addWidget(self.textField)
        self.leftLayout.addWidget(self.logoLabel)
        self.leftLayout.addWidget(QtWidgets.QWidget())
        self.leftLayout.addWidget(self.closeButton)

    def _setupWidgets(self):
        self.leftBox.setFixedWidth(150)
        self.Signal.addSignal(self.closeButton, 'clicked', self.closeButtonEvent)
        self.textField.setReadOnly(True)
        self.logoLabel.setFixedHeight(125)

        self.logoLabel.setPixmap(os.path.join(ICON_DIR, 'icon.png'))

        text = """
        Convenience Toolbox for Maya
        LightShader v.0.1
        
        Developed by: 
        Arvid Schneider
        
        Acknowledgements: 
        Rico Koschmitzky
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        This is an Open Source project, help me help you.
        
        """
        self.textField.setText(text)
        self.textField.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.textField.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.textField.setWordWrapMode(QtGui.QTextOption.NoWrap)

    def closeButtonEvent(self, *args):
        self.close()



class ReportDialog(QtWidgets.QDialog):
    def __init__(self):
        super(ReportDialog, self).__init__()
        self.setWindowTitle('Report')
        self.setFixedSize(500, 400)
        self.Signal = Signal()
        self._reportEmail = 'surface@lightshader.de'
        # Function calls
        self._setupWindow()

    @property
    def reportEmail(self):
        return self._reportEmail

    def openBrowser(self):
        recipient = 'tools@lightshader.de'
        subject = 'Report Email'

        body = '\n\nSystem Info:\n'

        for key, value in systemInfo().iteritems():
            body = body + '\n' + key + ':' + str(value)
        msg = 'mailto:?to=' + recipient + '&subject=' + subject + '&body=' + body
        webbrowser.open(msg, new=1)


    def _setupWindow(self):
        self.fromLabel = QtWidgets.QLineEdit()
        self.textField = QtWidgets.QTextEdit()
        self.sendButton = QtWidgets.QPushButton('Send')
        self.cancelButton = QtWidgets.QPushButton('Cancel')
        self.reportLayout = QtWidgets.QVBoxLayout(self)
        self.buttonLayout = QtWidgets.QHBoxLayout()

        self._addWidgets()
        self._setupWidgets()
        self._addSignals()

    def _addWidgets(self):
        self.reportLayout.addWidget(self.fromLabel)
        self.reportLayout.addWidget(self.textField)
        self.reportLayout.addLayout(self.buttonLayout)
        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.sendButton)

    def _setupWidgets(self):
        self.fromLabel.setFixedHeight(30)
        self.fromLabel.setPlaceholderText('Subject')
        self.textField.setPlaceholderText('Please enter relevant feedback here')

    def _addSignals(self):
        self.Signal.addSignal(self.sendButton, 'clicked', self.sendEmailEvent)
        self.Signal.addSignal(self.cancelButton, 'clicked', self.cancelEvent)

    def sendEmailEvent(self, *args, **kwargs):
        pass
        #
        # if len(self.fromLabel.text()) == 0:
        #     warnings.warn('Please enter valid email address')
        # if len(self.textField.toPlainText()) == 0:
        #     warnings.warn('Please add some relevant feedback text')
        #
        # sendToolsEmail(self.fromLabel.text(), self.textField.toPlainText(),
        #           'Report Email')
        # self.close()

    def cancelEvent(self, *args, **kwargs):
        self.close()

class Signal(object):
    def addSignal(self, obj, signal, function):
        if signal == 'clicked':
            obj.clicked.connect(partial(function, obj))
        elif signal == 'triggered':
            obj.triggered.connect(partial(function, obj))
        elif signal == 'itemActivated':
            obj.itemActivated.connect(partial(function, obj))
        elif signal == 'itemChanged':
            obj.itemChanged.connect(partial(function, obj))
        elif signal == 'itemClicked':
            obj.itemClicked.connect(partial(function, obj))
        elif signal == 'toggled':
            obj.toggled.connect(partial(function, obj))
        elif signal == 'itemSelectionChanged':
            obj.itemSelectionChanged.connect(partial(function, obj))
        else:
            warnings.warn('Signal: {} is not supported'.format(signal))


def wrapinstance(ptr, base=QtWidgets.QWidget):
    return shiboken2.wrapInstance(long(ptr), base)


def addBorder(object):
    if isinstance(object, QtWidgets.QGroupBox):
        object.setStyleSheet("""QGroupBox {
                                        border: 1px solid gray;
                                        border-radius: 9px;
                                        margin-top: 0.5em;
                                    }

                                    QGroupBox::title {
                                        subcontrol-origin: margin;
                                        left: 10px;
                                        padding: 0 3px 0 3px;

                                    }""")
    else:
        print type(object) + ' is not supported.'
