import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMaya as OpenMaya
import random
import os

path = cmds.workspace(q=True, rootDirectory=True)
path = "{}screenshots/".format(path)

if not os.path.exists(path):
	os.mkdir(path)

view = OpenMayaUI.M3dView.active3dView()
img = OpenMaya.MImage()
view.readColorBuffer(img, 1)
img.writeToFile("{}{}.jpg".format(path, int(random.random() * 10000)), "jpg")