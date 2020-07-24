from Katana import QtGui, QtCore, QT4FormWidgets, UI4, NodegraphAPI, DrawingModule
import os
import UI4.App.Tabs
import UI4.App.Layouts
import UI4.Widgets
from UI4.Tabs import BaseTab
from UI4.Widgets.SceneGraphView import SceneGraphViewIconManager


class pbTxManager(BaseTab):
    def __init__(self, parent):

        BaseTab.__init__(self, parent)

        self.buildUI()

    def buildUI(self):

        layout = QtGui.QVBoxLayout(self)

        self.openDil = QtGui.QPushButton('...')
        self.openDil.setMaximumWidth(20)
        self.openDil.clicked.connect(self.openDilog)

        saveWidget = QtGui.QWidget()
        saveLayout = QtGui.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        label3 = QtGui.QLabel()
        label3.setText('Path:')
        label3.setMaximumWidth(45)
        saveLayout.addWidget(label3)

        self.pathField = QtGui.QLineEdit()
        saveLayout.addWidget(self.pathField)

        saveLayout.addWidget(self.openDil)

        findBtn = QtGui.QPushButton('RELOAD')
        findBtn.setStyleSheet("background-color: #36743f;")
        findBtn.clicked.connect(self.populate)
        saveLayout.addWidget(findBtn)

        secWidget = QtGui.QWidget()
        secLayout = QtGui.QHBoxLayout(secWidget)
        layout.addWidget(secWidget)

        label2 = QtGui.QLabel()
        label2.setText('Conversion:')
        label2.setMaximumWidth(100)
        secLayout.addWidget(label2)

        self.progress = QtGui.QProgressBar()
        #self.progress.setMaximumWidth(500)
        secLayout.addWidget(self.progress)

        self.showCon = QtGui.QCheckBox('Show Converted')
        self.showCon.setChecked(1)
        secLayout.addWidget(self.showCon)

        self.listWidget = QtGui.QListWidget()
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        layout.addWidget(self.listWidget)

        makeWidget = QtGui.QWidget()
        makeLayout = QtGui.QHBoxLayout(makeWidget)
        layout.addWidget(makeWidget)

        label1 = QtGui.QLabel()
        label1.setText('Plugin:')
        label1.setMaximumWidth(45)
        makeLayout.addWidget(label1)

        self.rendererCB = QtGui.QComboBox()
        for renderer in ["Arnold", "Prman"]:
            self.rendererCB.addItem(renderer)
        self.rendererCB.setMaximumWidth(70)
        makeLayout.addWidget(self.rendererCB)

        makeBtn = QtGui.QPushButton('MAKE TX')
        makeBtn.setStyleSheet("background-color: #1f366b;")
        makeBtn.clicked.connect(self.makeCmd)
        makeLayout.addWidget(makeBtn)

        readBtn = QtGui.QPushButton('Read')
        readBtn.setMaximumWidth(50)
        # readBtn.setStyleSheet("background-color: #36743f;")
        readBtn.clicked.connect(self.readCmd)
        makeLayout.addWidget(readBtn)

        delBtn = QtGui.QPushButton('Delete')
        delBtn.setStyleSheet("background-color: #861b1b;")
        delBtn.setMaximumWidth(50)
        delBtn.clicked.connect(self.msgBox)
        makeLayout.addWidget(delBtn)

    ########################
    def openDilog(self):
        filename = UI4.Util.AssetId.BrowseForAsset('', 'Textures Path', True,
                                                   {'fileTypes': 'none', 'acceptDir': True, 'acceptFile': False})

        if filename:
            self.pathField.setText(filename)

        self.populate()

    ########################

    def readCmd(self):
        root = NodegraphAPI.GetRootNode()
        pos = NodegraphAPI.GetViewPortPosition(root)
        trans = 10
        checkRend = self.rendererCB.currentText()

        if checkRend == 'Arnold':
            nodeName = 'ArnoldShadingNode'
            nodeType = 'image'
        else:
            nodeName = 'PrmanShadingNode'
            nodeType = 'PxrTexture'

        directory = self.pathField.text()
        if str(directory).endswith('/'):
            directory = str(directory)[:-1]
        else:
            pass

        itemList = [item.text() for item in self.listWidget.selectedItems()]
        for item in itemList:
            trans += 300
            if not str(item).endswith('[CONVERTED]'):
                path = directory + '/' + str(item)
                name = os.path.splitext(str(item))[0]

                imageNode = NodegraphAPI.CreateNode(nodeName, NodegraphAPI.GetRootNode())
                imageNode.getParameter('nodeType').setValue(nodeType, 0)
                imageNode.getParameter('name').setValue(name + '_ORIG', 0)
                NodegraphAPI.SetNodePosition(imageNode, ((pos[0][0]+trans), pos[0][1]))
                DrawingModule.SetCustomNodeColor(imageNode, 0.4, 0, 0.15)
                imageNode.checkDynamicParameters()
                imageNode.getParameter('parameters.filename.enable').setValue(1, 0)
                imageNode.getParameter('parameters.filename.value').setValue(str(path), 0)

            else:
                name = str(item).replace(' [CONVERTED]', '')
                name = name.replace('  ', '')
                path = directory + '/' + str(name)

                texture = os.path.splitext(str(name))
                name = texture[0]
                if texture[1] == '.tx':
                    nodeName = 'ArnoldShadingNode'
                    nodeType = 'image'
                else:
                    nodeName = 'PrmanShadingNode'
                    nodeType = 'PxrTexture'

                imageNode = NodegraphAPI.CreateNode(nodeName, NodegraphAPI.GetRootNode())
                imageNode.getParameter('nodeType').setValue(nodeType, 0)
                imageNode.getParameter('name').setValue(name + '_tex', 0)
                NodegraphAPI.SetNodePosition(imageNode, ((pos[0][0]+trans), pos[0][1]))
                DrawingModule.SetCustomNodeColor(imageNode, 0.2, 0.4, 0.1)
                imageNode.checkDynamicParameters()
                imageNode.getParameter('parameters.filename.enable').setValue(1, 0)
                imageNode.getParameter('parameters.filename.value').setValue(str(path), 0)

    def msgBox(self):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Question)
        msg.setText("Du you really want to delete this files?")
        msg.setWindowTitle("Are you sure?")
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        msg.buttonClicked.connect(self.deleteCmd)
        msg.exec_()

    def deleteCmd(self, i):
        self.completed = 0
        self.progress.setValue(self.completed)
        if i.text() == '&Yes':
            itemList = [item.text() for item in self.listWidget.selectedItems()]
            for item in itemList:
                self.completed += (100 / len(itemList))
                self.progress.setValue(self.completed)
                if not str(item).endswith('[CONVERTED]'):
                    path = self.pathField.text() + '/' + str(item)
                    os.remove(str(path))
                else:
                    path = str(item).replace(' [CONVERTED]', '')
                    path = path.replace('  ', '')
                    path = self.pathField.text() + '/' + str(path)

                    os.remove(str(path))

            self.populate()
        else:
            return

    def populate(self):
        self.completed = 0
        self.progress.setValue(self.completed)
        self.listWidget.clear()
        myList = []
        myDir = self.pathField.text()
        if myDir == "":
            return
        included_extenstions = ['.jpg', '.bmp', '.png', '.gif', '.tif', '.tx', '.tex', '.exr', '.tga', '.dpx', '.hdr']
        textures = [fn for fn in os.listdir(myDir) if any(fn.endswith(ext) for ext in included_extenstions)]

        for item in textures:
            if item.endswith('.tx') or item.endswith('.tex'):
                item = '  ' + item + ' [CONVERTED]'
            myList.append(item)

        for tex in myList:
            if tex.endswith('[CONVERTED]'):
                if self.showCon.isChecked():
                    item = QtGui.QListWidgetItem(tex)
                    self.listWidget.addItem(item)
                    item.setBackground(QtGui.QColor('#246524'))
                else:
                    pass
            else:
                item = QtGui.QListWidgetItem(tex)
                self.listWidget.addItem(item)

    def makeCmd(self):

        self.completed = 2
        self.progress.setValue(self.completed)
        settings = ''

        checkRend = self.rendererCB.currentText()

        if checkRend == 'Prman':
            #######################################
            dataSource = {
                'Wrap Mode': 'black',
                'Mipmap Pattern': 'diagonal',
                'Blur': 1.0,
                'Env Map': int(False),
                'Data Compression': 'zip',
                '__childOrder': ['Wrap Mode', 'Mipmap Pattern', 'Blur', 'Env Map',
                                 'Data Compression'],
                '__childHints': {
                    'blur': {
                        'min': 1,
                    },
                    'Env Map': {
                        'widget': 'checkBox',
                    },
                    'Data Compression': {
                        'widget': 'popup',
                        'options': ['none', 'rle', 'zip', 'pxr24', 'b44',
                                    'b44a'],
                    },
                    'Wrap Mode': {
                        'widget': 'capsule',
                        'exclusive': True,
                        'delimiter': ' ',
                        'options': ['clamp', 'black', 'periodic'],
                    },
                    'Mipmap Pattern': {
                        'widget': 'capsule',
                        'exclusive': True,
                        'delimiter': ' ',
                        'options': ['diagonal', 'single', 'all'],
                    },
                }
            }

            d = QT4FormWidgets.FormDialog(dataSource, title='Prman tex settings')
            d.setMinimumSize(400, 250)

            if d.exec_() == QtGui.QDialog.Accepted:
                val = ''
                for keyName, value in dataSource.iteritems():
                    if keyName.startswith('__'):
                        continue
                    val += ("{1}_".format(keyName, value))  # ex:dataSource['Number']
            else:
                return
            val = val.split('_')
            envMap = ''
            if float(val[0]) == 1:
                envMap = ' -envlatl'
            else:
                envMap = ''
            settings = '-compression {} -mode {} -blur {}{} -pattern {}'.format(val[1], val[4], val[3], envMap, val[2])

            #######################################
        else:
            dataSource = {
                'Wrap Mode': 'black',
                'Configuration Presets': 'oiio',
                'Env Map': int(False),
                'Data Compression': 'zip',
                'Additional Options': '-u --unpremult',
                '__childOrder': ['Wrap Mode', 'Configuration Presets', 'Env Map',
                                 'Data Compression', 'Additional Options'],
                '__childHints': {
                    'Env Map': {
                        'widget': 'checkBox',
                    },
                    'Data Compression': {
                        'widget': 'popup',
                        'options': ['none', 'rle', 'zip', 'pxr24', 'b44',
                                    'b44a'],
                    },
                    'Wrap Mode': {
                        'widget': 'capsule',
                        'exclusive': True,
                        'delimiter': ' ',
                        'options': ['clamp', 'black', 'periodic', 'mirror'],
                    },
                    'Configuration Presets': {
                        'widget': 'capsule',
                        'exclusive': True,
                        'delimiter': ' ',
                        'options': ['oiio', 'prman'],
                    },
                    'Additional Options': {
                        'help': """Specify additional options for Make Tx. <strong>Do not repeat existing ones!</strong>"""
                    },
                }
            }

            d = QT4FormWidgets.FormDialog(dataSource, title='Arnold tx settings')
            d.setMinimumSize(400, 250)

            if d.exec_() == QtGui.QDialog.Accepted:
                val = ''
                for keyName, value in dataSource.iteritems():
                    if keyName.startswith('__'):
                        continue
                    val += ("{1}_".format(keyName, value))
            else:
                return
            val = val.split('_')

            env = ''
            if float(val[1]) == 1:
                envMap = ' --envlatl'
            else:
                envMap = ''
            settings = '{} --{} --wrap {}{} --compression {}'.format(val[3], val[0], val[4], envMap, val[2])
            #######################################

        itemList = [item.text() for item in self.listWidget.selectedItems()]
        for item in itemList:
            self.completed += (100/len(itemList))
            self.progress.setValue(self.completed-(100/len(itemList)))
            if not str(item).endswith('[CONVERTED]'):
                tex = os.path.splitext(str(item))
                texP = self.pathField.text() + '/' + tex[0] + '.tex'
                path = self.pathField.text() + '/' + tex[0] + tex[1]
                if checkRend == 'Prman':
                    os.system('txmake {} {} {}'.format(settings, path, texP))
                else:
                    os.system('maketx {} {}'.format(settings, path))
            else:
                print 'file {} is already converted'.format(item)

        self.populate()
        # self.completed = 100
        # self.progress.setValue(self.completed)


PluginRegistry = [("KatanaPanel", 2.0, "Lightshader/Tx Manager",
                   pbTxManager)]