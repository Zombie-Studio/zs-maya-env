"""
SCRIPT ZsControl
AUTHOR: Isaac Buzzola/isaac.buzzola@zombiestudio.com.br
DATE: Thursday 04 February 2021 17:51

SCRIPT FOR ZOMBIE STUDIO
"""
try:
    from maya import cmds

    sel = cmds.ls(sl=True)
    number = 0
    joints = []
    controls = []
    controlador = input("digite o nome do controlador:")
    for i in sel:
        pos = [cmds.getAttr(i + ".center.boundingBoxCenterX"), cmds.getAttr(i + ".center.boundingBoxCenterY"), cmds.getAttr(i + ".center.boundingBoxCenterZ")]
        cmds.select(clear=True)
        jnt = cmds.joint(name=controlador + "_%d_jnt" % number)
        cmds.xform(jnt, t=pos)
        ctrlGrp = cmds.group(em=True, name=controlador + "_%d_grp" % number)
        ctrls = cmds.circle(name=controlador + "_%d_ctrl" % number, c=[0, 0, 0], sw=360, d=3, r=5, nr=[0, 0, 1], ch=False)
        cmds.parent(ctrls, ctrlGrp)
        cmds.xform(ctrlGrp, t=pos)
        cmds.parentConstraint(ctrls, jnt)
        cmds.scaleConstraint(ctrls, jnt)
        number = number + 1
        joints.append(jnt)
        controls.append(ctrlGrp)

    jointGrp = cmds.group(em=True, name=controlador + "_joints_grp")
    cmds.parent(joints, jointGrp)
except Exception as error:
    print(error)
