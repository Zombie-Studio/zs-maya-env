import os
import sys
import maya.cmds as cmds
import maya.mel as mel

unknownNodes = cmds.ls(type="unknown")
for item in unknownNodes:
    if cmds.objExists(item):
        cmds.delete(item)
try:
    cmds.unknownPlugin("Mayatomr", remove=True)
    cmds.lockNode('TurtleDefaultBakeLayer', lock=False)
    cmds.delete('TurtleDefaultBakeLayer')
except:
    pass

cmds.SavePreferences()
cmds.savePrefs()
cmds.saveToolSettings()
cmds.saveViewportSettings()
cmds.file(save=True, force=True)