# importing libraries:
import maya.cmds as cmds
import maya.OpenMaya as om

from Library import dpUtils as utils
import dpBaseClass as Base
import dpLayoutClass as Layout


# global variables to this module:    
CLASS_NAME = "Single"
TITLE = "m073_single"
DESCRIPTION = "m074_singleDesc"
ICON = "/Icons/dp_single.png"


class Single(Base.StartClass, Layout.LayoutClass):
    def __init__(self,  *args, **kwargs):
        #Add the needed parameter to the kwargs dict to be able to maintain the parameter order
        kwargs["CLASS_NAME"] = CLASS_NAME
        kwargs["TITLE"] = TITLE
        kwargs["DESCRIPTION"] = DESCRIPTION
        kwargs["ICON"] = ICON
        Base.StartClass.__init__(self, *args, **kwargs)
        #Returned data from the dictionnary
        self.mainJisList = []
        self.aStaticGrpList = []
        self.aCtrlGrpList = []
        self.detectedBug = False
    
    
    def createModuleLayout(self, *args):
        Base.StartClass.createModuleLayout(self)
        Layout.LayoutClass.basicModuleLayout(self)
    
    
    def getHasIndirectSkin(self):
        return cmds.getAttr(self.moduleGrp + ".indirectSkin")
    
    
    def getHasHolder(self):
        return cmds.getAttr(self.moduleGrp + ".holder")
        
        
    def createGuide(self, *args):
        Base.StartClass.createGuide(self)
        # Custom GUIDE:
        cmds.addAttr(self.moduleGrp, longName="flip", attributeType='bool')
        cmds.setAttr(self.moduleGrp+".flip", 0)
        
        cmds.addAttr(self.moduleGrp, longName="indirectSkin", attributeType='bool')
        cmds.setAttr(self.moduleGrp+".indirectSkin", 0)
        cmds.addAttr(self.moduleGrp, longName='holder', attributeType='bool')
        cmds.setAttr(self.moduleGrp+".holder", 0)
        
        cmds.setAttr(self.moduleGrp+".moduleNamespace", self.moduleGrp[:self.moduleGrp.rfind(":")], type='string')
        
        self.cvJointLoc = self.ctrls.cvJointLoc(ctrlName=self.guideName+"_JointLoc1", r=0.3, d=1, guide=True)
        self.jGuide1 = cmds.joint(name=self.guideName+"_JGuide1", radius=0.001)
        cmds.setAttr(self.jGuide1+".template", 1)
        cmds.parent(self.jGuide1, self.moduleGrp, relative=True)
        
        self.cvEndJoint = self.ctrls.cvLocator(ctrlName=self.guideName+"_JointEnd", r=0.1, d=1, guide=True)
        cmds.parent(self.cvEndJoint, self.cvJointLoc)
        cmds.setAttr(self.cvEndJoint+".tz", 1.3)
        self.jGuideEnd = cmds.joint(name=self.guideName+"_JGuideEnd", radius=0.001)
        cmds.setAttr(self.jGuideEnd+".template", 1)
        cmds.transformLimits(self.cvEndJoint, tz=(0.01, 1), etz=(True, False))
        self.ctrls.setLockHide([self.cvEndJoint], ['tx', 'ty', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz'])
        
        cmds.parent(self.cvJointLoc, self.moduleGrp)
        cmds.parent(self.jGuideEnd, self.jGuide1)
        cmds.parentConstraint(self.cvJointLoc, self.jGuide1, maintainOffset=False, name=self.jGuide1+"_PaC")
        cmds.parentConstraint(self.cvEndJoint, self.jGuideEnd, maintainOffset=False, name=self.jGuideEnd+"_PaC")
        cmds.scaleConstraint(self.cvJointLoc, self.jGuide1, maintainOffset=False, name=self.jGuide1+"_ScC")
        cmds.scaleConstraint(self.cvEndJoint, self.jGuideEnd, maintainOffset=False, name=self.jGuideEnd+"_ScC")
    
    
    def changeIndirectSkin(self, *args):
        """ Set the attribute value for indirectSkin.
        """
        indSkinValue = cmds.checkBox(self.indirectSkinCB, query=True, value=True)
        cmds.setAttr(self.moduleGrp+".indirectSkin", indSkinValue)
        if indSkinValue == 0:
            cmds.setAttr(self.moduleGrp+".holder", 0)
            cmds.checkBox(self.holderCB, edit=True, value=False, enable=False)
        else:
            cmds.checkBox(self.holderCB, edit=True, enable=True)
            

    def changeHolder(self, *args):
        """ Set the attribute value for holder.
        """
        cmds.setAttr(self.moduleGrp+".holder", cmds.checkBox(self.holderCB, query=True, value=True))
    
    
    def rigModule(self, *args):
        Base.StartClass.rigModule(self)
        # verify if the guide exists:
        if cmds.objExists(self.moduleGrp):
            try:
                hideJoints = cmds.checkBox('hideJointsCB', query=True, value=True)
            except:
                hideJoints = 1
            # start as no having mirror:
            sideList = [""]
            # analisys the mirror module:
            self.mirrorAxis = cmds.getAttr(self.moduleGrp+".mirrorAxis")
            if self.mirrorAxis != 'off':
                # get rigs names:
                self.mirrorNames = cmds.getAttr(self.moduleGrp+".mirrorName")
                # get first and last letters to use as side initials (prefix):
                sideList = [ self.mirrorNames[0]+'_', self.mirrorNames[len(self.mirrorNames)-1]+'_' ]
                for s, side in enumerate(sideList):
                    duplicated = cmds.duplicate(self.moduleGrp, name=side+self.userGuideName+'_Guide_Base')[0]
                    allGuideList = cmds.listRelatives(duplicated, allDescendents=True)
                    for item in allGuideList:
                        cmds.rename(item, side+self.userGuideName+"_"+item)
                    self.mirrorGrp = cmds.group(name="Guide_Base_Grp", empty=True)
                    cmds.parent(side+self.userGuideName+'_Guide_Base', self.mirrorGrp, absolute=True)
                    # re-rename grp:
                    cmds.rename(self.mirrorGrp, side+self.userGuideName+'_'+self.mirrorGrp)
                    # do a group mirror with negative scaling:
                    if s == 1:
                        if cmds.getAttr(self.moduleGrp+".flip") == 0:
                            for axis in self.mirrorAxis:
                                gotValue = cmds.getAttr(side+self.userGuideName+"_Guide_Base.translate"+axis)
                                flipedValue = gotValue*(-2)
                                cmds.setAttr(side+self.userGuideName+'_'+self.mirrorGrp+'.translate'+axis, flipedValue)
                        else:
                            for axis in self.mirrorAxis:
                                cmds.setAttr(side+self.userGuideName+'_'+self.mirrorGrp+'.scale'+axis, -1)
                # joint labelling:
                jointLabelAdd = 1
            else: # if not mirror:
                duplicated = cmds.duplicate(self.moduleGrp, name=self.userGuideName+'_Guide_Base')[0]
                allGuideList = cmds.listRelatives(duplicated, allDescendents=True)
                for item in allGuideList:
                    cmds.rename(item, self.userGuideName+"_"+item)
                self.mirrorGrp = cmds.group(self.userGuideName+'_Guide_Base', name="Guide_Base_Grp", relative=True)
                #for Maya2012: self.userGuideName+'_'+self.moduleGrp+"_Grp"
                # re-rename grp:
                cmds.rename(self.mirrorGrp, self.userGuideName+'_'+self.mirrorGrp)
                # joint labelling:
                jointLabelAdd = 0
            # store the number of this guide by module type
            dpAR_count = utils.findModuleLastNumber(CLASS_NAME, "dpAR_type") + 1
            # run for all sides
            for s, side in enumerate(sideList):
                self.base = side+self.userGuideName+'_Guide_Base'
                cmds.select(clear=True)
                # declare guide:
                self.guide = side+self.userGuideName+"_Guide_JointLoc1"
                self.cvEndJoint = side+self.userGuideName+"_Guide_JointEnd"
                self.radiusGuide = side+self.userGuideName+"_Guide_Base_RadiusCtrl"
                # create a joint:
                self.jnt = cmds.joint(name=side+self.userGuideName+"_Jnt", scaleCompensate=False)
                cmds.addAttr(self.jnt, longName='dpAR_joint', attributeType='float', keyable=False)
                utils.setJointLabel(self.jnt, s+jointLabelAdd, 18, self.userGuideName)
                # create a control:
                if not self.getHasIndirectSkin():
                    if self.curveDegree == 0:
                        self.curveDegree = 1
                # work with curve shape and rotation cases:
                indirectSkinRot = (0, 0, 0)
                if self.langDic[self.langName]['c058_main'] in self.userGuideName:
                    ctrlTypeID = "id_054_SingleMain"
                    if len(sideList) > 1:
                        if self.langDic[self.langName]['c041_eyebrow'] in self.userGuideName:
                            indirectSkinRot = (0, 0, -90)
                        else:
                            indirectSkinRot = (0, 0, 90)
                else:
                    ctrlTypeID = "id_029_SingleIndSkin"
                    if self.langDic[self.langName]['c045_lower'] in self.userGuideName:
                        indirectSkinRot=(0, 0, 180)
                    elif self.langDic[self.langName]['c043_corner'] in self.userGuideName:
                        if "00" in self.userGuideName:
                            indirectSkinRot=(0, 0, 90)
                        else:
                            indirectSkinRot=(0, 0, -90)
                self.singleCtrl = self.ctrls.cvControl(ctrlTypeID, side+self.userGuideName+"_Ctrl", r=self.ctrlRadius, d=self.curveDegree, rot=indirectSkinRot)
                utils.originedFrom(objName=self.singleCtrl, attrString=self.base+";"+self.guide+";"+self.cvEndJoint+";"+self.radiusGuide)
                # position and orientation of joint and control:
                cmds.delete(cmds.parentConstraint(self.guide, self.jnt, maintainOffset=False))
                cmds.delete(cmds.parentConstraint(self.guide, self.singleCtrl, maintainOffset=False))
                # zeroOut controls:
                zeroOutCtrlGrp = utils.zeroOut([self.singleCtrl], offset=True)[0]
                # hide visibility attribute:
                cmds.setAttr(self.singleCtrl+'.visibility', keyable=False)
                # fixing flip mirror:
                if s == 1:
                    if cmds.getAttr(self.moduleGrp+".flip") == 1:
                        cmds.setAttr(zeroOutCtrlGrp+".scaleX", -1)
                        cmds.setAttr(zeroOutCtrlGrp+".scaleY", -1)
                        cmds.setAttr(zeroOutCtrlGrp+".scaleZ", -1)
                if not self.getHasIndirectSkin():
                    cmds.addAttr(self.singleCtrl, longName='scaleCompensate', attributeType="bool", keyable=False)
                    cmds.setAttr(self.singleCtrl+".scaleCompensate", 1, channelBox=True)
                    cmds.connectAttr(self.singleCtrl+".scaleCompensate", self.jnt+".segmentScaleCompensate", force=True)
                if self.getHasIndirectSkin():
                    # create a fatherJoint in order to zeroOut the skinning joint:
                    cmds.select(clear=True)
                    jxtName = self.jnt.replace("_Jnt", "_Jxt")
                    self.jxt = cmds.duplicate(self.jnt, name=jxtName)[0]
                    utils.clearDpArAttr([self.jxt])
                    cmds.parent(self.jnt, self.jxt)
                    cmds.makeIdentity(self.jnt, apply=True, jointOrient=False)
                    attrList = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
                    for attr in attrList:
                        cmds.connectAttr(self.singleCtrl+'.'+attr, self.jnt+'.'+attr)
                    if s == 1:
                        if cmds.getAttr(self.moduleGrp+".flip") == 1:
                            cmds.setAttr(self.jxt+".scaleX", -1)
                            cmds.setAttr(self.jxt+".scaleY", -1)
                            cmds.setAttr(self.jxt+".scaleZ", -1)
                    if self.getHasHolder():
                        cmds.delete(self.singleCtrl+"0Shape", shape=True)
                        self.singleCtrl = cmds.rename(self.singleCtrl, self.singleCtrl+"_"+self.langDic[self.langName]['c046_holder']+"_Grp")
                        self.ctrls.setLockHide([self.singleCtrl], ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz'])
                        self.jnt = cmds.rename(self.jnt, self.jnt.replace("_Jnt", "_"+self.langDic[self.langName]['c046_holder']+"_Jis"))
                        self.ctrls.setLockHide([self.jnt], ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz'], True, True)
                    else:
                        self.jnt = cmds.rename(self.jnt, self.jnt.replace("_Jnt", "_Jis"))
                else: # like a fkLine
                    # create parentConstraint from ctrl to jnt:
                    cmds.parentConstraint(self.singleCtrl, self.jnt, maintainOffset=False, name=self.jnt+"_PaC")
                    # create scaleConstraint from ctrl to jnt:
                    cmds.scaleConstraint(self.singleCtrl, self.jnt, maintainOffset=True, name=self.jnt+"_ScC")
                # create end joint:
                cmds.select(self.jnt)
                self.endJoint = cmds.joint(name=side+self.userGuideName+"_JEnd", radius=0.5)
                cmds.delete(cmds.parentConstraint(self.cvEndJoint, self.endJoint, maintainOffset=False))
                self.mainJisList.append(self.jnt)
                # create a masterModuleGrp to be checked if this rig exists:
                self.toCtrlHookGrp = cmds.group(side+self.userGuideName+"_Ctrl_Zero_0_Grp", name=side+self.userGuideName+"_Control_Grp")
                if self.getHasIndirectSkin():
                    locScale = cmds.spaceLocator(name=side+self.userGuideName+"_Scalable_DO_NOT_DELETE_PLEASE_Loc")[0]
                    cmds.setAttr(locScale+".visibility", 0)
                    self.toScalableHookGrp = cmds.group(locScale, name=side+self.userGuideName+"_IndirectSkin_Grp")
                    jxtGrp = cmds.group(side+self.userGuideName+"_Jxt", name=side+self.userGuideName+"_Joint_Grp")
                    self.toStaticHookGrp   = cmds.group(jxtGrp, self.toScalableHookGrp, self.toCtrlHookGrp, name=side+self.userGuideName+"_Grp")
                else:
                    self.toScalableHookGrp = cmds.group(side+self.userGuideName+"_Jnt", name=side+self.userGuideName+"_Joint_Grp")
                    self.toStaticHookGrp   = cmds.group(self.toCtrlHookGrp, self.toScalableHookGrp, name=side+self.userGuideName+"_Grp")
                # create a locator in order to avoid delete static or scalable group
                loc = cmds.spaceLocator(name=side+self.userGuideName+"_DO_NOT_DELETE_PLEASE_Loc")[0]
                cmds.parent(loc, self.toStaticHookGrp, absolute=True)
                cmds.setAttr(loc+".visibility", 0)
                self.ctrls.setLockHide([loc], ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])
                # add hook attributes to be read when rigging integrated modules:
                utils.addHook(objName=self.toCtrlHookGrp, hookType='ctrlHook')
                utils.addHook(objName=self.toScalableHookGrp, hookType='scalableHook')
                utils.addHook(objName=self.toStaticHookGrp, hookType='staticHook')
                cmds.addAttr(self.toStaticHookGrp, longName="dpAR_name", dataType="string")
                cmds.addAttr(self.toStaticHookGrp, longName="dpAR_type", dataType="string")
                cmds.setAttr(self.toStaticHookGrp+".dpAR_name", self.userGuideName, type="string")
                cmds.setAttr(self.toStaticHookGrp+".dpAR_type", CLASS_NAME, type="string")
                self.aStaticGrpList.append(self.toStaticHookGrp)
                self.aCtrlGrpList.append(self.toCtrlHookGrp)
                # add module type counter value
                cmds.addAttr(self.toStaticHookGrp, longName='dpAR_count', attributeType='long', keyable=False)
                cmds.setAttr(self.toStaticHookGrp+'.dpAR_count', dpAR_count)
                if hideJoints:
                    cmds.setAttr(self.toScalableHookGrp+".visibility", 0)
                # delete duplicated group for side (mirror):
                cmds.delete(side+self.userGuideName+'_'+self.mirrorGrp)
            # check mirror indirectSkin bug in Maya2018:
            if (int(cmds.about(version=True)[:4]) == 2018):
                if self.mirrorAxis != 'off':
                    if self.getHasIndirectSkin():
                        meshList = cmds.ls(selection=False, type="mesh")
                        if meshList:
                            self.detectedBug = True
            # finalize this rig:
            self.integratingInfo()
            cmds.select(clear=True)
        # delete UI (moduleLayout), GUIDE and moduleInstance namespace:
        self.deleteModule()
    
    
    def integratingInfo(self, *args):
        Base.StartClass.integratingInfo(self)
        """ This method will create a dictionary with informations about integrations system between modules.
        """
        self.integratedActionsDic = {
                                    "module": {
                                                "mainJisList"   : self.mainJisList,
                                                "staticGrpList" : self.aStaticGrpList,
                                                "ctrlGrpList"   : self.aCtrlGrpList,
                                                "detectedBug"   : self.detectedBug,
                                              }
                                    }
