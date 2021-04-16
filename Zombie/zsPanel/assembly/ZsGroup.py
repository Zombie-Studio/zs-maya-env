"""
SCRIPT ZsGroup
AUTHOR: Isaac Buzzola/isaac.buzzola@zombiestudio.com.br
DATE: Friday 11 December 2020 15:42

SCRIPT FOR ZOMBIE STUDIO
"""

try:
    from maya import cmds

    selCurve = cmds.ls(sl=True)

    for i in selCurve:
        grp = cmds.group(em=True, name=i.split("_geo")[0] + "_grp")
        cmds.parent(i, grp)
except Exception as error:
    print(error)
