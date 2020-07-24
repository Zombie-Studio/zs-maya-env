
from Katana import NodegraphAPI, RenderingAPI, LayeredMenuAPI, DrawingModule, os
from RenderingAPI import RenderPlugins


def PopulateCallback(layeredMenu):

    # Obtain a list of names of available shaders from the renderer info plug-in
    renderer = RenderingAPI.RenderPlugins.GetDefaultRendererPluginName()
    rendererInfoPlugin = RenderPlugins.GetInfoPlugin(renderer)
    shaderType = RenderingAPI.RendererInfo.kRendererObjectTypeShader
    shaderNames = rendererInfoPlugin.getRendererObjectNames(shaderType)
    redColor = (0.62, 0.02, 0.04)
    yellowColor = (0.92, 0.82, 0.24)
    for shaderName in shaderNames:
        if "light" in shaderName:
            layeredMenu.addEntry(shaderName, text=shaderName, color=yellowColor)
        else:
            layeredMenu.addEntry(shaderName, text=shaderName, color=redColor)

def ActionCallback(value):

    renderer = RenderingAPI.RenderPlugins.GetDefaultRendererPluginName()
    if renderer == 'dl':
        shadingNodeType = 'DlShadingNode'
        suffix='DSN'
    elif renderer == 'arnold':
        shadingNodeType = 'ArnoldShadingNode'
        suffix='ASN'
    elif renderer == 'prman':
        shadingNodeType = 'PrmanShadingNode'
        suffix='PSN'
    elif renderer == 'vray':
        shadingNodeType = 'VrayShadingNode'
        suffix='VSN'
    elif renderer == 'Redshift':
        shadingNodeType = 'RedshiftShadingNode'
        suffix='RSN'


    # Create the node, set its shader, and set the name with the shader name
    node = NodegraphAPI.CreateNode(shadingNodeType)
    node.getParameter('nodeType').setValue(value, 0)
    node.setName(value)
    DrawingModule.SetCustomNodeColor(node, 0.31, 0.26, 0.18)
    node.getParameter('name').setValue(node.getName(), 0)
    node.checkDynamicParameters()
    return node


# Create and register a layered menu using the above callbacks
# This is where you can set the hotkey
layeredMenu = LayeredMenuAPI.LayeredMenu(PopulateCallback, ActionCallback,
                                         'S', alwaysPopulate=False,
                                         onlyMatchWordStart=False)
LayeredMenuAPI.RegisterLayeredMenu(layeredMenu, 'getShadingNodes')

