# importing libraries:
import maya.cmds as cmds
import maya.mel as mel
from functools import partial

# global variables to this module:
CLASS_NAME = "TargetMirror"
TITLE = "m055_tgtMirror"
DESCRIPTION = "m056_tgtMirrorDesc"
ICON = "/Icons/dp_targetMirror.png"

DPTM_VERSION = "2.4"

class TargetMirror():
    def __init__(self, dpUIinst, langDic, langName, *args, **kwargs):
        self.langDic = langDic
        self.langName = langName
        # call main function
        self.dpTargetMirrorUI(self)
    
    
    def dpTargetMirrorUI(self, *args):
        """ Create a window in order to load the original model and targets to be mirrored.
        """
        # creating targetMirrorUI Window:
        if cmds.window('dpTargetMirrorWindow', query=True, exists=True):
            cmds.deleteUI('dpTargetMirrorWindow', window=True)
        targetMirror_winWidth  = 305
        targetMirror_winHeight = 250
        dpTargetMirrorWin = cmds.window('dpTargetMirrorWindow', title=self.langDic[self.langName]["m055_tgtMirror"]+" "+DPTM_VERSION, widthHeight=(targetMirror_winWidth, targetMirror_winHeight), menuBar=False, sizeable=True, minimizeButton=False, maximizeButton=False, menuBarVisible=False, titleBar=True)

        # creating layout:
        targetMirrorLayout = cmds.columnLayout('targetMirrorLayout')
        doubleLayout = cmds.rowColumnLayout('doubleLayout', numberOfColumns=2, columnWidth=[(1, 120), (2, 190)], columnAlign=[(1, 'left'), (2, 'left')], columnAttach=[(1, 'left', 10), (2, 'left', 20)], parent=targetMirrorLayout)
        cmds.button(label=self.langDic[self.langName]["i043_origModel"]+" >", annotation=self.langDic[self.langName]["i044_origDesc"], backgroundColor=(1.0, 1.0, 0.7), width=120, command=self.dpLoadOriginalModel, parent=doubleLayout)
        self.originalModelTextField = cmds.textField('originalModelTextField', width=160, text="", parent=doubleLayout)
        listMirrorLayout = cmds.columnLayout('listMirrorLayout', columnOffset=('left', 10), width=310, parent=targetMirrorLayout)
        cmds.text(label=self.langDic[self.langName]["i047_targetList"], height=30, parent=listMirrorLayout)
        self.targetScrollList = cmds.textScrollList('targetScrollList', width=290, height=100, allowMultiSelection=True, parent=listMirrorLayout)
        cmds.separator(style='none', parent=listMirrorLayout)
        middleLayout = cmds.rowColumnLayout('middleLayout', numberOfColumns=2, columnWidth=[(1, 150), (2, 150)], columnAlign=[(1, 'left'), (2, 'left')], columnAttach=[(1, 'left', 0), (2, 'left', 0)], parent=listMirrorLayout)
        cmds.button(label=self.langDic[self.langName]["i045_add"], annotation=self.langDic[self.langName]["i048_addDesc"], width=140, command=self.dpAddSelect, parent=middleLayout)
        cmds.button(label=self.langDic[self.langName]["i046_remove"], annotation=self.langDic[self.langName]["i051_removeDesc"], width=140, command=self.dpRemoveSelect, parent=middleLayout)
        cmds.separator(style='none', height=15, parent=middleLayout)
        renameLayout = cmds.rowColumnLayout('renameLayout', numberOfColumns=3, columnWidth=[(1, 100), (2, 100), (3, 100)], columnAlign=[(1, 'left'), (2, 'left'), (3, 'left')], columnAttach=[(1, 'left', 0), (2, 'left', 0), (3, 'left', 0)], parent=listMirrorLayout)
        self.autoRenameCB = cmds.checkBox('autoRenameCB', label=self.langDic[self.langName]["i056_autoRename"], value=1, onCommand=partial(self.dpChangeRename, 1), offCommand=partial(self.dpChangeRename, 0), parent=renameLayout)
        self.fromTxt = cmds.text('fromTxt', label="from", parent=renameLayout)
        self.toTxt = cmds.text('toTxt', label="to", parent=renameLayout)
        cmds.separator(style='none', height=15, parent=renameLayout)
        self.fromNameTF = cmds.textField('fromNameTF', width=80, text="L_", parent=renameLayout)
        self.toNameTF = cmds.textField('toNameTF', width=80, text="R_", parent=renameLayout)
        cmds.text(label="Axis:", height=20, parent=listMirrorLayout)
        tripleLayout = cmds.rowColumnLayout('tripleLayout', numberOfColumns=3, columnWidth=[(1, 100), (2, 100), (3, 100)], columnAlign=[(1, 'left'), (2, 'left'), (3, 'left')], columnAttach=[(1, 'left', 0), (2, 'left', 0), (3, 'left', 0)], parent=listMirrorLayout)
        self.mirrorAxisRC = cmds.radioCollection('mirrorAxisRC', parent=tripleLayout)
        rbX = cmds.radioButton("rbX", label="X = YZ", annotation="X", align="left", collection="mirrorAxisRC", parent=tripleLayout)
        rbY = cmds.radioButton("rbY", label="Y = XZ", annotation="Y", align="left", collection="mirrorAxisRC", parent=tripleLayout)
        rbZ = cmds.radioButton("rbZ", label="Z = XY", annotation="Z", align="left", collection="mirrorAxisRC", parent=tripleLayout)
        cmds.radioCollection('mirrorAxisRC', edit=True, select="rbX")
        cmds.separator(style='none', height=15, parent=listMirrorLayout)
        self.mirrorPosCB = cmds.checkBox('mirrorPosCB', label=self.langDic[self.langName]["i057_mirrorPosition"], value=1, parent=listMirrorLayout)
        self.cleanUndoCB = cmds.checkBox('cleanUndoCB', label=self.langDic[self.langName]["i049_clearUndo"], annotation=self.langDic[self.langName]["i050_clearUndoDesc"], align="left", value=1, parent=listMirrorLayout)
        self.checkHistoryCB = cmds.checkBox('checkHistoryCB', label=self.langDic[self.langName]["i162_checkHistory"], annotation=self.langDic[self.langName]["i161_historyMessage"], align="left", value=0, parent=listMirrorLayout)
        cmds.button(label=self.langDic[self.langName]["i054_targetRun"], annotation=self.langDic[self.langName]["i053_targetRunDesc"], width=290, backgroundColor=(0.6, 1.0, 0.6), command=self.dpRunMirror, parent=listMirrorLayout)

        # call targetMirrorUI Window:
        cmds.showWindow(dpTargetMirrorWin)
    
    
    def dpLoadOriginalModel(self, *args):
        """ Load selected object as original model
        """
        selectedList = cmds.ls(selection=True)
        if selectedList:
            if self.dpCheckGeometry(selectedList[0]):
                cmds.textField(self.originalModelTextField, edit=True, text=selectedList[0])
        else:
            print "Original Model > None"
    
    
    def dpAddSelect(self, *args):
        """ Add selected items to target textscroll list
        """
        # declare variables
        selMeshList = []
        # get selection
        selList = cmds.ls(selection=True)
        # check if there is any selected object in order to continue
        if selList:
            # find meshes transforms
            for item in selList:
                if not item in selMeshList:
                    if self.dpCheckGeometry(item):
                        selMeshList.append(item)
                    else:
                        return
            if selMeshList:
                # get current list
                currentList = cmds.textScrollList(self.targetScrollList, query=True, allItems=True)
                if currentList:
                    # clear current list
                    cmds.textScrollList(self.targetScrollList, edit=True, removeAll=True)
                    # avoid repeated items
                    for item in selMeshList:
                        if not item in currentList:
                            currentList.append(item)
                    # refresh textScrollList
                    cmds.textScrollList(self.targetScrollList, edit=True, append=currentList)
                else:
                    # add selected items in the empyt target scroll list
                    cmds.textScrollList(self.targetScrollList, edit=True, append=selMeshList)
            else:
                mel.eval("warning \""+self.langDic[self.langName]["i055_tgtSelect"]+"\";")
        else:
            mel.eval("warning \""+self.langDic[self.langName]["i055_tgtSelect"]+"\";")
    
    
    def dpRemoveSelect(self, *args):
        """ Remove selected items from target scroll list.
        """
        selItemList = cmds.textScrollList(self.targetScrollList, query=True, selectItem=True)
        if selItemList:
            for item in selItemList:
                cmds.textScrollList(self.targetScrollList, edit=True, removeItem=item)
    
    
    def dpChangeRename(self, value, *args):
        """ Enable or disable text fields
        """
        cmds.text(self.fromTxt, edit=True, enable=value)
        cmds.text(self.toTxt, edit=True, enable=value)
        cmds.textField(self.fromNameTF, edit=True, enable=value)
        cmds.textField(self.toNameTF, edit=True, enable=value)
    
    
    def dpCheckGeometry(self, item, *args):
        isGeometry = False
        if item:
            if cmds.objExists(item):
                childList = cmds.listRelatives(item, children=True)
                if childList:
                    try:
                        itemType = cmds.objectType(childList[0])
                        if itemType == "mesh" or itemType == "nurbsSurface" or itemType == "subdiv":
                            if cmds.checkBox(self.checkHistoryCB, query=True, value=True):
                                historyList = cmds.listHistory(childList[0])
                                if len(historyList) > 1:
                                    dialogReturn = cmds.confirmDialog(title=self.langDic[self.langName]["i159_historyFound"], message=self.langDic[self.langName]["i160_historyDesc"]+"\n\n"+item+"\n\n"+self.langDic[self.langName]["i161_historyMessage"], button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')
                                    if dialogReturn == "Yes":
                                        isGeometry = True
                                else:
                                    isGeometry = True
                            else:
                                isGeometry = True
                        else:
                            mel.eval("warning \""+item+" "+self.langDic[self.langName]["i058_notGeo"]+"\";")
                    except:
                        mel.eval("warning \""+self.langDic[self.langName]["i163_sameName"]+" "+item+"\";")
                else:
                    mel.eval("warning \""+self.langDic[self.langName]["i059_selTransform"]+" "+item+" "+self.langDic[self.langName]["i060_shapePlease"]+"\";")
            else:
                mel.eval("warning \""+item+" "+self.langDic[self.langName]["i061_notExists"]+"\";")
        else:
            mel.eval("warning \""+self.langDic[self.langName]["i062_notFound"]+" "+item+"\";")
        return isGeometry
    
    
    def dpRunMirror(self, *args):
        """ Create the mirrored targets.
        """
        # declaring variables
        attrList = ["tx", "ty", "tz"]
        # get loaded original node
        origNode = cmds.textField(self.originalModelTextField, query=True, text=True)
        if self.dpCheckGeometry(origNode):
            # get target list:
            targetList = cmds.textScrollList(self.targetScrollList, query=True, allItems=True)
            if targetList:
                # progress window
                progressAmount = 0
                cmds.progressWindow(title=self.langDic[self.langName]["m055_tgtMirror"], progress=progressAmount, status='Doing: 0%', isInterruptable=True)
                cancelled = False
                nbTarget = len(targetList)
                # get mirror information from UI
                selectedMirror = cmds.radioCollection(self.mirrorAxisRC, query=True, select=True)
                axis = cmds.radioButton(selectedMirror, query=True, annotation=True)
                clearUndo = cmds.checkBox(self.cleanUndoCB, query=True, value=True)
                # clear selection
                cmds.select(clear=True)
                for item in targetList:
                    # update progress window
                    progressAmount += 1
                    # check if the dialog has been cancelled
                    if cmds.progressWindow(query=True, isCancelled=True):
                        cancelled = True
                        break
                    cmds.progressWindow(edit=True, maxValue=nbTarget, progress=progressAmount, status=('Doing: ' + `progressAmount` + ' target'))
                    if not item == origNode:
                        # start copying
                        if self.dpCheckGeometry(item):
                            # naming
                            newTargetName = item+"_Mirror"+axis
                            if cmds.checkBox(self.autoRenameCB, query=True, value=True):
                                fromName = cmds.textField(self.fromNameTF, query=True, text=True)
                                toName = cmds.textField(self.toNameTF, query=True, text=True)
                                if fromName in item:
                                    newTargetName = item.replace(fromName, toName)
                            # duplicate original model
                            tempDup = cmds.duplicate(origNode, name="temp_dupOrig")[0]
                            # create a temporary blendShape node
                            tmpToWrapBS = cmds.blendShape(item, tempDup, topologyCheck=False, name="temp_toWRAP_BS")[0]
                            # make a duplicated model group
                            bsMirrorGrp = cmds.group(tempDup, name="temp_bsMirrorGrp")
                            # apply mirror
                            cmds.setAttr(bsMirrorGrp+".scale"+axis, -1)
                            # create a new copy of the original model in order to be the mirrored target
                            newTarget = cmds.duplicate(origNode, name=newTargetName)[0]
                            # create a wrap deformer from bsMirrorGrp to newTarget
                            cmds.select([newTarget, bsMirrorGrp])
                            mel.eval("CreateWrap;")
                            # set blendShape slider as 1
                            cmds.setAttr(tmpToWrapBS+"."+item, 1)
                            # clear history and temporary  group
                            cmds.delete(newTarget, constructionHistory=True)
                            cmds.delete(bsMirrorGrp)
                            # position:
                            if cmds.checkBox(self.mirrorPosCB, query=True, value=True):
                                try:
                                    for attr in attrList:
                                        cmds.setAttr(newTarget+"."+attr, cmds.getAttr(item+"."+attr))
                                    axisValue = cmds.getAttr(item+".translate"+axis)*(-1)
                                    cmds.setAttr(newTarget+".translate"+axis, axisValue)
                                except:
                                    pass
                            # clear undo
                            if clearUndo:
                                mel.eval("flushUndo;")
                cmds.progressWindow(endProgress=True)
            cmds.select(clear=True)