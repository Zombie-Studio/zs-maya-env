"""
SCRIPT ZsCopyskin
AUTHOR: Isaac Buzzola/isaac.buzzola@zombiestudio.com.br
DATE: Friday 11 December 2020 15:50

SCRIPT FOR ZOMBIE STUDIO
"""

import maya.cmds as cmds

skins = cmds.ls(sl=1)
inf = cmds.skinCluster(skins[0],q=1,inf=1)

for obj in skins[1:]:
	cmds.skinCluster( inf, obj, tsb=1,ibp=1)
	cmds.select(skins[0])
	cmds.select(obj,tgl=1)
	print cmds.ls(sl=1)
	cmds.copySkinWeights(nm=1,sa="closestPoint", ia="closestJoint")
