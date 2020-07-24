import maya.OpenMayaUI as openMayaUI
import shiboken2
from lightshader.qt.interface import wrapinstance
from lightshader.qt.interface import QtWidgets


def mayaMainWindow():
    mainWindowPtr = openMayaUI.MQtUtil.mainWindow()
    mainWindow = shiboken2.wrapInstance(long(mainWindowPtr), QtWidgets.QMainWindow)
    return mainWindow


def getQObject(mayaUI):
    ptr = openMayaUI.MQtUtil.findControl(mayaUI)
    qobject = wrapinstance(ptr)
    return qobject


def mayaMenuBar():
    for eachChild in mayaMainWindow().children():
        if type(eachChild) == QtWidgets.QMenuBar:
            return eachChild
