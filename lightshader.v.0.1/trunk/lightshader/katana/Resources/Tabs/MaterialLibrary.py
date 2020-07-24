from Katana import QtGui, QtCore, UI4, NodegraphAPI, QT4FormWidgets, KatanaFile, DrawingModule, RenderingAPI
import os
import re
from RenderingAPI import RenderPlugins
from UI4.Tabs import BaseTab


class pbMaterilLibrary(BaseTab):
    def __init__(self, parent):

        BaseTab.__init__(self, parent)

        # directories
        self.matlibPath = os.getenv('LIGHTSHADER_MATLIB')
        self.directory = os.path.join(self.matlibPath, 'material_library')
        self.resources = os.path.join(self.matlibPath, 'resources')
        #########################################################

        # functions
        self.buildUI()
        self.categories()
        self.populate()

        # for right click
        self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listWidget.connect(self.listWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                                self.listItemRightClicked)
        #########################################################

    @staticmethod
    def checkDir(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        else:
            return

    def categories(self):
        self.catedoryCB.clear()
        categories =[name for name in os.listdir(self.directory) if os.path.isdir(os.path.join(self.directory, name))]
        categories.insert(0,'ALL')
        for folder in categories:
            self.catedoryCB.addItem(folder)

    def buildUI(self):

        layout = QtGui.QVBoxLayout(self)

        #########################################################

        # upper row

        controlWidget = QtGui.QWidget()
        controlLayout = QtGui.QHBoxLayout(controlWidget)
        layout.addWidget(controlWidget)

        # reload
        reloadBtn=QtGui.QPushButton('RELOAD')
        reloadBtn.setStyleSheet("background-color: #1f366b;")

        reloadBtn.clicked.connect(self.clearSearch)
        reloadBtn.clicked.connect(self.populate)
        reloadBtn.clicked.connect(self.categories)


        # standard MTL
        createStd=QtGui.QPushButton('Standard Material')
        createStd.setStyleSheet("background-color: #36743f;")
        createStd.clicked.connect(self.createStandard)
        createStd.setMaximumWidth(110)

        # thumbnail size
        self.icon_size=QtGui.QSpinBox()
        self.icon_size.setRange(60, 260)
        self.icon_size.setValue(128)
        self.icon_size.setSingleStep(20)
        self.icon_size.valueChanged.connect(self.populate)
        self.icon_size.setMaximumWidth(50)

        label=QtGui.QLabel()
        label.setText('Thumbnail size:')
        label.setMaximumWidth(100)

        #layout
        controlLayout.addWidget(label)
        controlLayout.addWidget(self.icon_size)
        controlLayout.addWidget(reloadBtn)
        controlLayout.addWidget(createStd)

        #########################################################

        # second row

        searchWidget = QtGui.QWidget()
        searchLayout = QtGui.QHBoxLayout(searchWidget)
        layout.addWidget(searchWidget)

        # search field
        label1 = QtGui.QLabel()
        label1.setText('Search:')
        label1.setMaximumWidth(50)

        self.searchField = QtGui.QLineEdit()
        self.searchField.returnPressed.connect(self.populate)
        # self.searchField.textChanged.connect(self.searchCmd)
        self.searchField.setMaximumWidth(650)

        # categories

        label2 = QtGui.QLabel()
        label2.setText('Category:')
        label2.setMaximumWidth(80)

        self.catedoryCB=QtGui.QComboBox()
        self.catedoryCB.currentIndexChanged.connect(self.populate)
        self.catedoryCB.setMaximumWidth(100)


        # layout
        searchLayout.addWidget(label1)
        searchLayout.addWidget(self.searchField)
        searchLayout.addWidget(label2)
        searchLayout.addWidget(self.catedoryCB)

        #########################################################

        # main list view

        self.listWidget = QtGui.QListWidget()
        self.listWidget.setViewMode(QtGui.QListWidget.IconMode)

        self.listWidget.setResizeMode(QtGui.QListWidget.Adjust)
        self.listWidget.itemDoubleClicked.connect(self.doubleCkicked)

        self.listWidget.setStyleSheet(
            "QListWidget::item {"
            "border-style: solid;"
            "border-width:3px;"
            "background-color: #252525;"
            "}"
            "QListWidget::item:selected {"
            "background-color: #1e1e1e;"
            "}")

        layout.addWidget(self.listWidget)
        #########################################################

    def clearSearch(self):
        self.searchField.setText('')

    def createStandard(self):
        pos = NodegraphAPI.GetViewPortPosition(NodegraphAPI.GetRootNode())
        renderer = RenderingAPI.RenderPlugins.GetDefaultRendererPluginName()
        if renderer == 'arnold':
            fileName = os.path.join(self.resources, 'arnold_standard.katana')
        elif renderer == 'prman':
            fileName = os.path.join(self.resources, 'prman_standard.katana')
        else:
            QtGui.QMessageBox.warning(None, 'Error', '{} plugin not found!' .format(renderer.upper()))
            return

        if os.path.exists(fileName):
            KatanaFile.Import(fileName, floatNodes=False)
            imported = NodegraphAPI.GetAllSelectedNodes()[-1]
            NodegraphAPI.SetNodePosition(imported, ((pos[0][0]), pos[0][1]))
        else:
            QtGui.QMessageBox.warning(None, 'Error', 'There is no standard material saved!')

    def listItemRightClicked(self, QPos):
        self.listMenu = QtGui.QMenu()

        self.listMenu.setStyleSheet("""
            QMenu {
                background-color: #313131;
                border: 1px solid ;
            }
            QMenu::item::selected {
                background-color: #1e1e1e;
            }
        """)

        import_mtl = self.listMenu.addAction("Import Material")
        import_klf = self.listMenu.addAction("Import Lookfile")
        import_Lmtl = self.listMenu.addAction("Create Material")
        delete_mtl = self.listMenu.addAction("Delete Material")

        self.connect(import_mtl, QtCore.SIGNAL("triggered()"), self.importMtl)
        self.connect(import_klf, QtCore.SIGNAL("triggered()"), self.importKlf)
        self.connect(import_Lmtl, QtCore.SIGNAL("triggered()"), self.importLmtl)
        self.connect(delete_mtl, QtCore.SIGNAL("triggered()"), self.deleteMtl)
        parentPosition = self.listWidget.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()

    def doubleCkicked(self):
        currentItemName = str(self.listWidget.currentItem().text())
        checkCat=str(self.catedoryCB.currentText())

        if not checkCat == 'ALL':
            fileName = os.path.join(self.directory, checkCat, currentItemName)
        else:
            fileName = os.path.join(str(self.listWidget.currentItem().data(QtCore.Qt.UserRole).toPyObject()),
                                    currentItemName)

        if os.path.exists(fileName + '.katana'):
            self.importMtl()
        elif os.path.exists(fileName + '.klf'):
            self.importLmtl()

    def importMtl(self):
        pos = NodegraphAPI.GetViewPortPosition(NodegraphAPI.GetRootNode())
        currentItemName = str(self.listWidget.currentItem().text())
        checkCat=str(self.catedoryCB.currentText())

        if not checkCat == 'ALL':
            fileName = os.path.join(self.directory, checkCat, currentItemName + '.katana')
        else:
            fileName = os.path.join(str(self.listWidget.currentItem().data(QtCore.Qt.UserRole).toPyObject()),
                                    currentItemName + '.katana')

        if os.path.exists(fileName):
            KatanaFile.Import(fileName, floatNodes=False)
            imported = NodegraphAPI.GetAllSelectedNodes()[-1]
            DrawingModule.SetCustomNodeColor(imported, 0.2, 0.4, 0.1)
            NodegraphAPI.SetNodePosition(imported, ((pos[0][0]), pos[0][1]))
        else:
            QtGui.QMessageBox.information(None, currentItemName,
                                          'There is no Material for {}, try importing Look File!'
                                          .format(currentItemName))

    def importKlf(self):
        pos = NodegraphAPI.GetViewPortPosition(NodegraphAPI.GetRootNode())
        currentItemName = str(self.listWidget.currentItem().text())
        checkCat=str(self.catedoryCB.currentText())

        if not checkCat == 'ALL':
            klfName = os.path.join(self.directory, checkCat, currentItemName + '.klf')
            expression = 'path.join(getenv("MATLIB",0), "material_library", "{}", "{}")'.format(checkCat, currentItemName + '.klf')
        else:
            klfName = os.path.join(str(self.listWidget.currentItem().data(QtCore.Qt.UserRole).toPyObject()),
                                    currentItemName + '.klf')
            expression= 'path.join(getenv("MATLIB",0), "material_library", "{}", "{}")'\
                .format(str(self.listWidget.currentItem().data(QtCore.Qt.UserRole).toPyObject()).split(os.sep)[-1], currentItemName+'.klf')

        if os.path.exists(klfName):
            lfm = NodegraphAPI.CreateNode('LookFileMaterialsIn', NodegraphAPI.GetRootNode())
            lfm.setName('LFMI_' + currentItemName)
            DrawingModule.SetCustomNodeColor(lfm, 0.4, 0, 0.15)
            lfm.getParameter('lookfile').setExpression(expression)
            NodegraphAPI.SetNodePosition(lfm, ((pos[0][0]), pos[0][1]))
        else:
            QtGui.QMessageBox.information(None, currentItemName,
                                          'There is no Look File for {}, try importing Material!'
                                          .format(currentItemName))

    def importLmtl(self):
        pos = NodegraphAPI.GetViewPortPosition(NodegraphAPI.GetRootNode())
        currentItemName = str(self.listWidget.currentItem().text())
        checkCat=str(self.catedoryCB.currentText())

        if not checkCat == 'ALL':
            klfName = os.path.join(self.directory, checkCat, currentItemName + '.klf')
            expression = 'path.join(getenv("MATLIB",0), "material_library", "{}", "{}")'.format(checkCat, currentItemName + '.klf')
        else:
            klfName = os.path.join(str(self.listWidget.currentItem().data(QtCore.Qt.UserRole).toPyObject()),
                                    currentItemName + '.klf')
            expression= 'path.join(getenv("MATLIB",0), "material_library", "{}", "{}")'\
                .format(str(self.listWidget.currentItem().data(QtCore.Qt.UserRole).toPyObject()).split(os.sep)[-1], currentItemName+'.klf')

        if os.path.exists(klfName):
            materialNode = NodegraphAPI.CreateNode('Material', NodegraphAPI.GetRootNode())
            materialNode.getParameter('name').setValue(currentItemName, 0)
            DrawingModule.SetCustomNodeColor(materialNode, 0.2, 0.27, 0.4)
            materialNode.getParameter('action').setValue('create from Look File', 0)
            materialNode.getParameter('lookfile.lookfile').setExpression(expression)
            NodegraphAPI.SetNodePosition(materialNode, ((pos[0][0]), pos[0][1]))

            materialAssign = NodegraphAPI.CreateNode('MaterialAssign', NodegraphAPI.GetRootNode())
            materialAssign.setName('MA_'+currentItemName)
            materialAssign.getParameter('args.materialAssign.value').setExpression("scenegraphLocationFromNode(getNode('{}'))"
                                                                                   .format(materialNode.getName()))
            DrawingModule.SetCustomNodeColor(materialAssign, 0.2, 0.27, 0.4)
            NodegraphAPI.SetNodePosition(materialAssign, ((pos[0][0]), pos[0][1] - 50))
            materialNode.getOutputPort('out').connect(materialAssign.getInputPort('input'))
            NodegraphAPI.SetNodeEdited(materialAssign, edited=True, exclusive=True)

        else:
            QtGui.QMessageBox.information(None, currentItemName,
                                          'There in no Look File for {}, try importing Material!'
                                          .format(currentItemName))

    def deleteMtl(self):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Warning)
        msg.setText("Are you sure you want to delete this material?")
        msg.setWindowTitle("Warning!")
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        msg.buttonClicked.connect(self.deleteCmd)
        msg.exec_()

    def deleteCmd(self, i):
        checkCat=str(self.catedoryCB.currentText())
        if i.text() == '&Yes':
            currentItemName = str(self.listWidget.currentItem().text())

            if not checkCat == 'ALL':
                mtlName=os.path.join(self.directory, checkCat, currentItemName+'.katana')
                klfName=os.path.join(self.directory, checkCat, currentItemName+'.klf')
                icoName=os.path.join(self.directory, checkCat, currentItemName+'.png')
            else:
                mtlName=os.path.join(str(self.listWidget.currentItem().data(QtCore.Qt.UserRole).toPyObject()),
                                     currentItemName+'.katana')
                klfName=os.path.join(str(self.listWidget.currentItem().data(QtCore.Qt.UserRole).toPyObject()),
                                     currentItemName+'.klf')
                icoName=os.path.join(str(self.listWidget.currentItem().data(QtCore.Qt.UserRole).toPyObject()),
                                     currentItemName+'.png')

            if os.path.exists(mtlName):
                os.remove(mtlName)
            if os.path.exists(klfName):
                os.remove(klfName)
            if os.path.exists(icoName):
                os.remove(icoName)

            self.populate()
        else:
            return

    def populate(self):
        self.listWidget.clear()
        self.listWidget.setIconSize(QtCore.QSize(self.icon_size.value(), self.icon_size.value()))
        self.listWidget.setGridSize(QtCore.QSize(self.icon_size.value() + 20, self.icon_size.value() + 30))

        checkCat=str(self.catedoryCB.currentText())
        if not checkCat == 'ALL':
            directory = os.path.join(self.directory, checkCat)
            self.popItems(directory)


        else:
            for root, dirs, files in os.walk(self.directory):
                for dir in dirs:
                    directory= os.path.join(root, dir)
                    self.popItems(directory)

    def popItems(self, directory):
        mats = []
        searchText = str(self.searchField.text())
        for item in os.listdir(directory):
            if os.path.splitext(item)[-1] == '.katana' or os.path.splitext(item)[-1] == '.klf':
                if re.search(searchText, item, re.IGNORECASE):
                    mats.append(os.path.splitext(item)[0])

        mats = set(mats)
        self.makeItems(directory, mats)

    def makeItems(self, directory, mats):
        for mat in mats:
            material = QtGui.QListWidgetItem(mat)
            screenshot = os.path.join(directory, mat + '.png')

            if not mat + '.png' in os.listdir(directory):
                screenshot = os.path.join(self.resources, 'dummyIcon.png')

            icon = QtGui.QIcon(screenshot)

            material.setData(QtCore.Qt.UserRole, directory)
            material.setIcon(icon)

            self.listWidget.addItem(material)


PluginRegistry = [("KatanaPanel", 2.0, "Lightshader/Material Library",
                   pbMaterilLibrary)]