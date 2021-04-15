"""
SCRIPT ZsProp
AUTHOR: Isaac Buzzola/isaac.buzzola@zombiestudio.com.br
DATE: Friday 11 December 2020 14:42

SCRIPT FOR ZOMBIE STUDIO
"""

## autoRig Prop Zombie

from maya import cmds

model = cmds.ls( sl = True )

if model == []:
    cmds.warning( "Seleciona um objeto para criar o rig" )
   
else:
    # criando grupos
    allGrp = cmds.group( em = True, name = "All_grp" )
    meshGrp = cmds.group( em = True, name = "MESH" )
    ctrlGrp = cmds.group( em = True, name = "CTRL" )
    dataGrp = cmds.group( em = True, name = "DATA" )
    
    # organizando a hierarquia dos grupos
    childGroup = meshGrp,ctrlGrp,dataGrp
    cmds.parent( childGroup, allGrp )
    
    # criando controles
    
    masterCtrl = cmds.circle( name = "master_ctrl", c = [0,0,0], sw = 360, d = 3, r = 80, nr = [0,1,0], ch = False)
    globalCtrl = cmds.circle( name = "global_ctrl", c = [0,0,0], sw = 360, d = 3, r = 100, nr = [0,1,0], ch = False)
    
    # organizando a hierarquia das curvas
    
    cmds.parent( masterCtrl, globalCtrl )
    cmds.parent( globalCtrl, ctrlGrp )
    
    # setando model no rig
    
    cmds.parent( model, meshGrp )

    # setando cores
    
    cmds.setAttr(str(masterCtrl[0]) + ".overrideEnabled", 1)
    cmds.setAttr(str(masterCtrl[0]) + ".overrideColor", 13)
    cmds.setAttr(str(globalCtrl[0]) + ".overrideEnabled", 1)
    cmds.setAttr(str(globalCtrl[0]) + ".overrideColor", 17)
    
    # setando layers
    cmds.select( "MESH" )
    geoLr = cmds.createDisplayLayer( noRecurse=True, name='GEO_lr' )
    cmds.select( clear = True )
    cmds.select( "CTRL" )
    ctrlLr = cmds.createDisplayLayer( noRecurse=True, name='CTRL_lr' )