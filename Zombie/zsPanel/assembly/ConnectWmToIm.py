"""
SCRIPT ConnectWmToIm
AUTHOR: Isaac Buzzola/isaac.buzzola@zombiestudio.com.br
DATE: Monday 05 April 2021 15:58

SCRIPT FOR ZOMBIE STUDIO
"""

try:
    from maya import cmds
    sel = cmds.ls( sl = 1 )
    ## conectar World Mesh em InMesh
    cmds.connectAttr( sel[0] + ".worldMesh[0]", sel[1] + ".inMesh"  )
except Exception as error:
    print(error)