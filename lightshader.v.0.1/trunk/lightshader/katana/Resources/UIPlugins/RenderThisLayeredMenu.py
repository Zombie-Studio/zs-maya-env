from Katana import NodegraphAPI, LayeredMenuAPI, RenderManager, UI4


def PopulateCallback(layeredMenu):
    primitiveNames=[]
    for node in NodegraphAPI.GetAllNodes():
        if node.getType() == "Render" or node.getType() == "ImageWrite" or 'pbRend' in node.getName():
            primitiveNames.append(node.getName())
        else:
            pass

    for primitiveName in primitiveNames:
        layeredMenu.addEntry(primitiveName, text=primitiveName,
                             color=(0.8, 0.24, 0.26))


def ActionCallback(value):
    RenderNode=NodegraphAPI.GetNode(str(value))
    NodegraphAPI.SetNodeViewed(RenderNode, viewed=True, exclusive=True)

    if UI4.App.Tabs.FindTopTab('Monitor'):
        RenderManager.StartRender('previewRender', node=RenderNode)
    else:
        pass



layeredMenu=LayeredMenuAPI.LayeredMenu(PopulateCallback, ActionCallback,
                                       'Alt+R', alwaysPopulate=True,
                                       onlyMatchWordStart=False)
LayeredMenuAPI.RegisterLayeredMenu(layeredMenu, 'RenderThis')
