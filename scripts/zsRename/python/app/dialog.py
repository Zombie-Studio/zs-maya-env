from PySide2 import QtWidgets
from maya import OpenMayaUI, cmds, mel
from shiboken2 import wrapInstance

from .ui import dialog

reload(dialog)

from .ui.dialog import Ui_Dialog

class Dialog:
    name = 'zsRenameControl'

    type_rename = 'hierarchy'

    def __init__(self):
        self.main = QtWidgets
        self.widget = self.main.QWidget

        if cmds.workspaceControl(self.name, query=True, exists=True):
            cmds.workspaceControl(self.name, edit=True, close=True)
            cmds.deleteUI(self.name)

        control = cmds.workspaceControl(self.name)
        cmds.workspaceControl(self.name, edit=True, label='ZS Rename v0.1', ttc=["AttributeEditor", 0], restore=True, iw=300, mw=True, wp='preferred')
        control_widget = OpenMayaUI.MQtUtil.findControl(control)
        control_wrap = wrapInstance(long(control_widget), self.widget)

        control_wrap.setObjectName(self.name)
        self.ui = Ui_Dialog()
        self.ui.setupUi(control_wrap)

        self.ui.buttonRenameNumber.clicked.connect(self.renameNumber)
        self.ui.buttonRemoveFirst.clicked.connect(lambda x: self.removeCharacter('first'))
        self.ui.buttonRemoveLast.clicked.connect(lambda x: self.removeCharacter('last'))
        self.ui.buttonHash.clicked.connect(self.renameHash)
        self.ui.buttonAddAfter.clicked.connect(lambda x: self.addCharacter('after'))
        self.ui.buttonAddBeffore.clicked.connect(lambda x: self.addCharacter('before'))

        self.ui.optionHirearchy.clicked.connect(lambda x: self.setTypeRename('hierarchy'))
        self.ui.optionSelected.clicked.connect(lambda x: self.setTypeRename('selected'))
        self.ui.optionAll.clicked.connect(lambda x: self.setTypeRename('all'))
        self.ui.buttonApply.clicked.connect(self.renameReplace)

        self.ui.buttonGrp.clicked.connect(lambda x: self.setType('grp'))
        self.ui.buttonGeo.clicked.connect(lambda x: self.setType('geo'))
        self.ui.buttonCtrl.clicked.connect(lambda x: self.setType('ctrl'))
        self.ui.buttonJnt.clicked.connect(lambda x: self.setType('jnt'))
        self.ui.buttonDrv.clicked.connect(lambda x: self.setType('drv'))

    def renameNumber(self):
        name = self.ui.inputRename.text()
        start = int(self.ui.inputStart.text())
        padding = int(self.ui.inputPadding.text())
        name = '{}{}'.format(name, str(start).zfill(padding))
        selecteds = cmds.ls(selection=True)
        if selecteds:
            for sel in selecteds:
                cmds.rename(sel, name)

    def removeCharacter(self, type):
        selecteds = cmds.ls(selection=True)
        if selecteds:
            for sel in selecteds:
                if type is 'first':
                    name = sel[1:]
                else:
                    name = sel[:-1]
                cmds.rename(sel, name)

    def renameHash(self):
        hash = self.ui.inputHash.text()
        counter = self.counterHash(hash)
        getHash = self.extractHash(hash)

        selecteds = cmds.ls(selection=True)
        if selecteds:
            i = 1
            for sel in selecteds:
                name = str(i).zfill(counter)
                name = hash.replace(getHash, name)
                cmds.rename(sel, name)
                i += 1

    def counterHash(self, name):
        counter = 0
        for x in range(len(name)):
            if name[x] == '#':
                counter += 1
        return counter

    def extractHash(self, name):
        hash = ''
        for x in range(len(name)):
            if name[x] == '#':
                hash += name[x]
        return hash

    def addCharacter(self, type):
        after = self.ui.inputAfter.text()
        before = self.ui.inputBefore.text()
        selecteds = cmds.ls(selection=True)
        if selecteds:
            for sel in selecteds:
                if before not in sel and type == 'before':
                    name = '{before}{name}'.format(before=before, name=sel)
                    cmds.rename(sel, name)
                if after not in sel and type == 'after':
                    name = '{name}{after}'.format(after=after, name=sel)
                    cmds.rename(sel, name)

    def setType(self, prefix):
        selecteds = cmds.ls(sl=True)

        options = ['grp', 'geo', 'ctrl', 'jnt', 'drv']
        types = {'grp': 'transform', 'geo': 'mesh', 'ctrl': 'nurbsCurve', 'jnt': 'joint', 'drv': 'transform'}

        if prefix == 'ctrl':
            index = -4
            remove = -5
        else:
            index = -3
            remove = -4

        if selecteds:
            for sel in selecteds:
                type = cmds.ls(sel, st=True, dag=True)[-1:][0]

                if type not in types[prefix]:
                    cmds.select(sel, d=True)
                else:
                    if sel[index:] in options:
                        newName = sel[:remove]
                        name = '{name}_{prefix}'.format(name=newName, prefix=prefix)
                        cmds.rename(sel, name)
                    else:
                        name = '{name}_{prefix}'.format(name=sel, prefix=prefix)
                        cmds.rename(sel, name)

    def setTypeRename(self, name):
        self.type_rename = name

    def renameReplace(self):
        search = self.ui.inputSearch.text()
        replace = self.ui.inputReplace.text()
        typeRename = self.type_rename
        mel.eval('searchReplaceNames "{}" "{}" "{}"'.format(search, replace, typeRename))
        self.ui.inputSearch.setText('')
        self.ui.inputReplace.setText('')
