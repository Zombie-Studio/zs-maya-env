"""
SCRIPT ZsBlinn
AUTHOR: Isaac Buzzola/isaac.buzzola@zombiestudio.com.br
DATE: Friday 11 December 2020 15:41

SCRIPT FOR ZOMBIE STUDIO
"""

try:
    from maya import cmds

    listGeo = []
    meshSelect = cmds.ls(sl=True, sn=True)

    for name in meshSelect:
        newName = name.split("Shape")[0]
        listGeo.append(newName)

    def applyMaterial(node):
        if cmds.objExists(node):
            shd = cmds.shadingNode('blinn', name="%s_mat" % node.split("_geo")[0], asShader=True)
            shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
            cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
            cmds.sets(node, e=True, forceElement=shdSG)

    for mesh in listGeo:
        applyMaterial(mesh)

except Exception as error:
    print(error)
