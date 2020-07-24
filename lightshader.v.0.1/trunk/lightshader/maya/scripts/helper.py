import pymel.core as pmc
import os
from lightshader.maya.core import Renderer


def rename(objectType, selected=True):
    activeSelection = []
    if selected:
        activeSelection = pmc.selected()

    if objectType == 'shadingEngine':
        # Renames ShadingEngines based on surfaceShader input connection
        # rename('shadingEngine', selected=False)
        # Works on selected or on all SGs

        def _renameSG(se):
            for shader in se.surfaceShader.connections():
                se.rename('{}SG'.format(shader.name()))

        if selected:
            pmc.undoInfo(openChunk=True)
            for se in activeSelection:
                _renameSG(se)
            pmc.undoInfo(closeChunk=True)


        else:
            # all se's except the default ones
            pmc.undoInfo(openChunk=True)
            for se in pmc.ls(type='shadingEngine'):
                if se.name() in ['initialParticleSE', 'initialShadingGroup']:
                    continue
                _renameSG(se)
            pmc.undoInfo(closeChunk=True)


    if objectType == 'textureInput':

        def _renameTexture(texture):
            attribute = None
            if hasattr(texture, 'filename'):
                attribute = texture.filename
            elif hasattr(texture, 'fileTextureName'):
                attribute = texture.fileTextureName
            textureName = attribute.get()
            if len(textureName) == 0:
                return
            fileName = os.path.split(textureName)[1]
            fileNameBase = os.path.splitext(fileName)[0]

            texture.rename(texture.type() + '_' + fileNameBase)

        if selected:
            pmc.undoInfo(openChunk=True)
            for texture in activeSelection:
                _renameTexture(texture)
            pmc.undoInfo(closeChunk=True)

        else:
            # all se's except the default ones
            textures = pmc.ls(type='file')
            if Renderer.isArnold:
                textures = textures + pmc.ls(type='aiImage')
            elif Renderer.isPrman:
                textures = textures + pmc.ls(type=['PxrTexture', 'PxrPtexture'])

            pmc.undoInfo(openChunk=True)
            for texture in textures:
                _renameTexture(texture)
            pmc.undoInfo(closeChunk=True)

def focusRig():
    currentSelection = pmc.selected()
    warningMsg = "Please make a valid selection, first camera and then focus geometry!"
    if len(currentSelection) != 2:
        return pmc.displayWarning(warningMsg)
    cameraTransform, focusTransform = currentSelection
    cameraShape = cameraTransform.getShape()

    if cameraShape.type() != "camera":
        return pmc.displayWarning(warningMsg)

    distance = pmc.distanceDimension(sp=focusTransform.getRotatePivot(space='world'),
                                     ep=cameraTransform.getRotatePivot(space='world'))
    distance.rename('lsFocusRigShape')
    distance.getParent().rename('lsFocusRig')
    focusLocator, nodalLocator = distance.listConnections()
    focusLocator.rename('lsFocusPoint')
    nodalLocator.rename('lsCameraNodal')
    pmc.parent(nodalLocator, cameraTransform)
    pmc.parent(distance.getParent(), cameraTransform)
    # Needs to only continue if arnold is valid

    if Renderer.isArnold:
        cameraShape.aiEnableDOF.set(1)
        cameraShape.aiApertureSize.set(1)
        distance.distance >> cameraShape.aiFocusDistance
    else:
        cameraShape.depthOfField.set(1)
        distance.distance >> cameraShape.focusDistance










