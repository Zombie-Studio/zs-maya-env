#
#    ngSkinTools
#    Copyright (c) 2009-2017 Viktoras Makauskas.
#    All rights reserved.
#    
#    Get more information at 
#        http://www.ngskintools.com
#    
#    --------------------------------------------------------------------------
#
#    The coded instructions, statements, computer programs, and/or related
#    material (collectively the "Data") in these files are subject to the terms 
#    and conditions defined by EULA.
#         
#    A copy of EULA can be found in file 'LICENSE.txt', which is part 
#    of this source code package.
#    

from maya import cmds, mel


def install_shelf():
    """
    checks if there's ngSkintTools shelf installed, and if not, creates one.

    this runs each time Maya starts (via Autoloader's ngSkinTools_load.mel) - avoid duplication, like creating things
    that already exist.
    """
    maya_shelf = mel.eval("$tempngSkinToolsVar=$gShelfTopLevel")
    existing_shelves = cmds.shelfTabLayout(maya_shelf, q=True, tabLabel=True)

    parent_shelf = 'ngSkinTools'

    if parent_shelf in existing_shelves:
        return

    mel.eval('addNewShelfTab ' + parent_shelf)
    cmds.shelfButton(
        parent=parent_shelf,
        enable=1,
        visible=1,
        preventOverride=0,
        label="ngst",
        annotation="ngSkinTools UI",
        image="ngSkinToolsShelfIcon.png",
        style="iconOnly",
        noBackground=1,
        align="center",
        marginWidth=1,
        marginHeight=1,
        command="from ngSkinTools.ui.mainwindow import MainWindow\nMainWindow.open()",
        sourceType="python",
        commandRepeatable=0,
    )
