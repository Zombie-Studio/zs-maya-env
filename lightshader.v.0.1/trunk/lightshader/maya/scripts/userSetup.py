from lightshader.qt.interface import LSMenu
from lightshader.maya.qt.helper import mayaMenuBar, QtWidgets
from lightshader.maya.lighting.source.lightcontrol import LightControl
from lightshader.maya.lighting.source.attributecontrol import AttributeControl
from lightshader.maya.lighting.source.aovcontrol import AovControl
import lightshader.maya.scripts.helper as helper
import pymel.core as pmc

pmc.evalDeferred('LightShaderMenu()')


class LightShaderMenu(LSMenu):
    def __init__(self):
        self.lightControl = 'Light Control'
        self.attributeControl = 'Attribute Control'
        self.aovControl = 'AOV Control'

        # Super needs to be called last, so maya specific actions are added at the top
        super(LightShaderMenu, self).__init__(mayaMenuBar())

    def _addActions(self):
        self.addHelperMenu()
        self.addAction(self.attributeControl)
        self.addAction(self.lightControl)
        self.addAction(self.aovControl)
        self.addSeparator()
        # Super needs to be called last, so maya specific actions are added at the top
        super(LightShaderMenu, self)._addActions()

    def handleSignals(self, obj, action, *args):
        super(LightShaderMenu, self).handleSignals(obj, action, args)

        if isinstance(action, QtWidgets.QAction):
            actionName = action.text()

            if actionName == self.lightControl:
                LightControl().show(dockable=True)
            elif actionName == self.attributeControl:
                AttributeControl().show(dockable=True)
            elif actionName == self.aovControl:
                AovControl().show(dockable=True)
            elif actionName == self.renameTextureSelected:
                helper.rename('textureInput', selected=True)
            elif actionName == self.renameTextureAll:
                helper.rename('textureInput', selected=False)
            elif actionName == self.renameShadingEngineSelected:
                helper.rename('shadingEngine', selected=True)
            elif actionName == self.renameShadingEngineAll:
                helper.rename('shadingEngine', selected=False)
            elif actionName == self.focusRig:
                helper.focusRig()

    def addHelperMenu(self):
        self.helperMenu = QtWidgets.QMenu('Helper')
        self.helperMenu.setWindowTitle('Lightshader Helper')
        self.helperMenu.setTearOffEnabled(True)
        self.addMenu(self.helperMenu)
        self.addSeparator()
        self.focusRig = 'Focus Rig (Camera then Object)'
        self.renameTextureSelected = 'Automatic Texture Rename (selected)'
        self.renameTextureAll = 'Automatic Texture Rename (all)'
        self.renameShadingEngineSelected = 'Automatic ShadingEngine Rename (selected)'
        self.renameShadingEngineAll = 'Automatic ShadingEngine Rename (all)'
        self.helperMenu.addAction(self.focusRig)
        self.helperMenu.addSeparator()
        self.helperMenu.addAction(self.renameTextureSelected)
        self.helperMenu.addAction(self.renameTextureAll)
        self.helperMenu.addSeparator()
        self.helperMenu.addAction(self.renameShadingEngineSelected)
        self.helperMenu.addAction(self.renameShadingEngineAll)