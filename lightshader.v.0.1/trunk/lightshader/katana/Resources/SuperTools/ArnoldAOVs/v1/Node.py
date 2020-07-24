from Katana import NodegraphAPI, Utils, UniqueName

from Upgrade import Upgrade
import ScriptActions as SA
import logging

log = logging.getLogger("ArnoldAOVs_LS.Node")

class ArnoldAOVsNode(NodegraphAPI.SuperTool):
    def __init__(self):
        self.hideNodegraphGroupControls()
        self.addInputPort('in')
        self.addOutputPort('out')

        # Hidden version parameter to detect out-of-date internal networks and upgrade it.
        self.getParameters().createChildNumber('version', 1)

        # Parameters
        paramFile = self.getParameters().createChildString('Filename', 'untitled_<aov>_####.<ext>')
        paramFile.setHintString("{'widget': 'assetIdInput'}")

        paramFormat = self.getParameters().createChildString('Format', 'exr')
        paramFormat.setHintString(
            "{'options__order': ['TIFF', 'OpenEXR', 'OpenEXR (deep)'], 'widget': 'mapper', 'options': "
            "{'OpenEXR': 'exr', 'TIFF': 'tif', 'OpenEXR (deep)': 'deepexr'}}")

        paramBitDepth = self.getParameters().createChildString('BitDepth', '16')
        paramBitDepth.setHintString("{'widget': 'popup', 'options': ['16', '32']}")

        paramTiled = self.getParameters().createChildNumber('Tiled', 0)
        paramTiled.setHintString("{'widget': 'checkBox', 'constant': 'True'}")

        paramMerge = self.getParameters().createChildNumber('MergeAOVs', 0)
        paramMerge.setHintString("{'widget': 'checkBox', 'constant': 'True', 'help': 'Combine all AOVs into one EXR."
                                 "Turn off tiled before merging!'}")

        self.__buildDefaultNetwork()

    def __buildDefaultNetwork(self):
        self.__mergeGrp = NodegraphAPI.CreateNode('Group', self)
        self.__mergeGrp.setName('_MERGE_SETUP_')
        self.__mergeGrp.addInputPort('in')
        self.__mergeGrp.addOutputPort('out')
        disableParameter = self.__mergeGrp.getParameters().createChildNumber('disable', 0)
        disableParameter.setHintString('{"widget": "checkBox"}')
        disableParameter.setExpression("getParent().MergeAOVs-1")

        #AOCD
        prim_aocd = NodegraphAPI.CreateNode('ArnoldOutputChannelDefine', self.__mergeGrp)

        prim_aocd.setName('AOCD_primary')
        prim_aocd.getParameter('name').setValue('primary', 0)
        prim_aocd.getParameter('channel').setValue('primary', 0)
        prim_aocd.getParameter('lightPathExpression').setValue('C.*', 0)

        driver = prim_aocd.getParameter('nodes').createChildGroup('driverParameters')
        #####
        parameter = driver.createChildGroup('half_precision')
        parameter.createChildNumber('enable', 1)
        value = parameter.createChildNumber('value', 0)
        parameter.createChildString('type', 'IntAttr')
        value.setExpression("1 if getParent().getParent().BitDepth=='16' else 0")
        parameter = driver.createChildGroup('tiled')
        parameter.createChildNumber('enable', 1)
        parameter.createChildNumber('value', 0)
        parameter.createChildString('type', 'IntAttr')

        #ROD
        prim_rod = NodegraphAPI.CreateNode('RenderOutputDefine', self.__mergeGrp)
        prim_rod.setName('ROD_primary')
        prim_rod.getParameter('outputName').setValue('primary', 0)
        prim_rod.checkDynamicParameters()

        prim_rod.getParameter('args.renderSettings.outputs.outputName.rendererSettings.channel.enable').setValue(1, 0)
        prim_rod.getParameter('args.renderSettings.outputs.outputName.rendererSettings.channel.value')\
            .setValue('primary', 0)

        ######
        mergeRod = NodegraphAPI.CreateNode('RenderOutputDefine', self.__mergeGrp)
        mergeRod.setName('ROD_MERGE')
        mergeRod.getParameter('outputName').setValue('merged', 0)
        mergeRod.getParameter('args.renderSettings.outputs.outputName.type.enable').setValue(1, 0)
        mergeRod.getParameter('args.renderSettings.outputs.outputName.type.value').setValue('merge', 0)
        mergeRod.getParameter('args.renderSettings.outputs.outputName.locationType.enable').setValue(1, 0)
        mergeRod.getParameter('args.renderSettings.outputs.outputName.locationType.value').setValue('file', 0)

        mergeRod.checkDynamicParameters()
        mergeRod.getParameter('args.renderSettings.outputs.outputName.locationSettings.renderLocation.enable')\
            .setValue(1, 0)
        mergeRod.getParameter('args.renderSettings.outputs.outputName.locationSettings.renderLocation.value')\
            .setExpression("(str(getParent().getParent().Filename).replace('<aov>', 'merged')).replace('<ext>', 'exr')")

        self.__mergeGrp.getSendPort(self.__mergeGrp.getInputPortByIndex(0).getName()).connect(prim_aocd.getInputPortByIndex(0))
        prim_aocd.getOutputPortByIndex(0).connect(prim_rod.getInputPortByIndex(0))
        prim_rod.getOutputPortByIndex(0).connect(mergeRod.getInputPortByIndex(0))
        mergeRod.getOutputPortByIndex(0).connect(self.__mergeGrp.getReturnPort(self.__mergeGrp.getOutputPortByIndex(0).getName()))

        NodegraphAPI.SetNodePosition(prim_aocd, (0, 0))
        NodegraphAPI.SetNodePosition(prim_rod, (0, -50))
        NodegraphAPI.SetNodePosition(mergeRod, (0, -100))
        ######

        self.sendPort = self.getSendPort(self.getInputPortByIndex(0).getName())
        self.__mergeGrp.getOutputPortByIndex(0).connect(self.getReturnPort(self.getOutputPortByIndex(0).getName()))
        returnPort = self.__mergeGrp.getInputPortByIndex(0)

        self.sendPort.connect(returnPort)

    def __createAOVgroup(self, aovName, filter='gaussian_filter'):

        grp = NodegraphAPI.CreateNode('Group', self)

        grp.addInputPort('in')

        grp.addOutputPort('out')

        grp.setName('_AOV_%s' % aovName)

        grp.getParameters().createChildString('aov', aovName)

        aocd = NodegraphAPI.CreateNode('ArnoldOutputChannelDefine', grp)

        aocd.getParameter('name').setValue(aovName, 0)
        aocd.getParameter('channel').setValue(aovName, 0)
        aocd.setName('AOCD_%s' % aovName)
        aocd.getParameter('driver').setExpression('"driver_"+str(getParent().getParent().Format).replace("tif", "tiff")')
        aocd.getParameter('filter').setValue(filter, 0)
        #####
        driver = aocd.getParameter('nodes').createChildGroup('driverParameters')
        #####
        parameter = driver.createChildGroup('half_precision')
        parameter.createChildNumber('enable', 1)
        value = parameter.createChildNumber('value', 0)
        parameter.createChildString('type', 'IntAttr')
        value.setExpression("1 if getParent().getParent().BitDepth=='16' else 0")
        #####
        parameter = driver.createChildGroup('format')
        parameter.createChildNumber('enable', 1)
        value = parameter.createChildNumber('value', 0)
        parameter.createChildString('type', 'IntAttr')
        value.setExpression("1 if getParent().getParent().BitDepth=='16' else 2")
        #####
        parameter = driver.createChildGroup('tiled')
        parameter.createChildNumber('enable', 1)
        value = parameter.createChildNumber('value', 0)
        parameter.createChildString('type', 'IntAttr')
        value.setExpression("getParent().getParent().Tiled")
        #####
        parameter = driver.createChildGroup('autocrop')
        parameter.createChildNumber('enable', 1)
        parameter.createChildNumber('value', 1)
        parameter.createChildString('type', 'IntAttr')
        #####

        rod = NodegraphAPI.CreateNode('RenderOutputDefine', grp)
        rod.setName('ROD_%s' % aovName)
        rod.getParameter('outputName').setValue(aovName, 0)
        rod.getParameter('args.renderSettings.outputs.outputName.locationType.enable').setValue(1, 0)
        rod.getParameter('args.renderSettings.outputs.outputName.locationType.value')\
            .setExpression("'file' if getParent().getParent().MergeAOVs == 0 else 'local'")

        #####
        parameter = rod.getParameter('args.renderSettings.outputs.outputName.locationSettings').createChildGroup('renderLocation')
        #####
        parameter.createChildNumber('enable', 1)
        value = parameter.createChildString('value', '')
        parameter.createChildString('type', 'StringAttr')
        value.setExpression("str(str(getParent().getParent().Filename).replace('<aov>', str(outputName)))."
                            "replace('<ext>', str(args.renderSettings.outputs.outputName.rendererSettings."
                            "fileExtension.value).replace('deepexr', 'exr'))")

        rod.checkDynamicParameters()

        rod.getParameter('args.renderSettings.outputs.outputName.rendererSettings.channel.enable').setValue(1, 0)
        rod.getParameter('args.renderSettings.outputs.outputName.rendererSettings.channel.value').setValue(aovName, 0)

        rod.getParameter('args.renderSettings.outputs.outputName.rendererSettings.fileExtension.enable').setValue(1, 0)
        rod.getParameter('args.renderSettings.outputs.outputName.rendererSettings.fileExtension.value').setExpression(
            'str(getParent().getParent().Format).replace("deepexr", "exr")')


        NodegraphAPI.SetNodePosition(rod, (0, -50))
        grp.getSendPort('in').connect(aocd.getInputPortByIndex(0))
        aocd.getOutputPortByIndex(0).connect(rod.getInputPortByIndex(0))
        rod.getOutputPortByIndex(0).connect(grp.getReturnPort('out'))

        return grp

    def addLayer(self, aovName, filter='gaussian_filter'):
        Utils.UndoStack.OpenGroup('Add "%s" AOV' % aovName)
        try:
            mergeGrp = SA.getMergeGrp(self)
            returnPort = mergeGrp.getInputPortByIndex(0)
            lastPort = returnPort.getConnectedPort(0)
            lastNode = lastPort.getNode()
            if '_MERGE_SETUP_' in lastNode.getName():
                pos = (0, 0)
            else:
                pos = NodegraphAPI.GetNodePosition(lastNode)

            aovLayer = self.__createAOVgroup(aovName, filter)
            aovLayer.getInputPortByIndex(0).connect(lastPort)
            aovLayer.getOutputPortByIndex(0).connect(returnPort)
            NodegraphAPI.SetNodePosition(aovLayer, (pos[0], pos[1] - 50))
            p1 = NodegraphAPI.GetNodePosition(aovLayer)
            NodegraphAPI.SetNodePosition(mergeGrp, (p1[0], p1[1] - 80))
            mergeRod = mergeGrp.getChildByIndex(2)
            aovList = []
            for aov in self.getChildren():
                if '_MERGE_SETUP_' not in aov.getName():
                    name = str(aov.getName()).replace('_AOV_', '')
                    aovList.append(name)
            aovList.append('primary')
            names = ",".join(aovList)
            mergeRod.getParameter('args.renderSettings.outputs.outputName.mergeOutputs.enable').setValue(1, 0)
            mergeRod.getParameter('args.renderSettings.outputs.outputName.mergeOutputs.value').setValue(names, 0)

        finally:
            Utils.UndoStack.CloseGroup()

    def addParameterHints(self, attrName, inputDict):
        inputDict.update(_ExtraHints.get(attrName, {}))

    def upgrade(self):
        if not self.isLocked():
            Upgrade(self)
        else:
            log.warning('Cannot upgrade locked ArnoldAOVs_LS node "%s".'
                        % self.getName())

_ExtraHints = {
    'ArnoldAOVs_LS.location':{
        'widget':'newScenegraphLocation',
    },
}