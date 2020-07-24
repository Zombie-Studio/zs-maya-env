import lightshader.maya.lighting.gui.aovcontrol as aovgui
from lightshader.maya.qt.helper import mayaMainWindow, wrapinstance, getQObject
from lightshader.maya.api.api import API
from lightshader.qt.interface import QtCore, QtWidgets
import pymel.core as pmc
from lightshader.maya.core import Scene, Renderer, Attribute
import random


class AovControl(aovgui.AovControl):
    def __init__(self):
        self.Renderer = Renderer()
        super(AovControl, self).__init__(mayaMainWindow())

    def _populateLightList(self):
        self.lightList.addItems([light.fullPath() for light in Scene.getLights()])

    def _populateAovList(self):
        self.aovList.addItems([aov.name() for aov in Scene.getAovs()])
