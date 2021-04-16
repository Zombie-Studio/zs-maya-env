"""
SCRIPT ZsCreateAiShader
AUTHOR: Isaac Buzzola/isaac.buzzola@zombiestudio.com.br
DATE: Friday 11 December 2020 15:22

SCRIPT FOR ZOMBIE STUDIO
"""

try:
    from arnold import *
    from maya import cmds

    listGeo = []

    meshSelect = cmds.ls(sl=True, sn=True)

    for name in meshSelect:
        newName = name.split("Shape")[0]
        listGeo.append(newName)

    def applyMaterial(node):
        if cmds.objExists(node):
            shd = cmds.shadingNode('aiStandardSurface', name="%s_mat" % node, asShader=True)
            shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
            cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
            cmds.sets(node, e=True, forceElement=shdSG)
            aiCorrect = cmds.shadingNode('aiColorCorrect', name="%s_aiColorCorrect" % node, asShader=True)
            aiRange = cmds.shadingNode('aiRange', name="%s_aiRange" % node, asShader=True)
            cmds.connectAttr('%s.outColor' % aiCorrect, '%s.baseColor' % shd)
            cmds.connectAttr('%s.outColorR' % aiRange, '%s.specularRoughness' % shd)


    for mesh in listGeo:
        applyMaterial(mesh)

except Exception as error:
    print(error)
