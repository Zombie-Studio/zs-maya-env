import os
import sys
import maya.cmds as cmds
import maya.standalone
import maya.mel as mel

zombieEnv = os.path.join(os.environ['APPDATA'], 'zombieEnv')
os.environ["MAYA_APP_DIR"] = zombieEnv

shelfvs = ['Rigging', 'Animation', 'Rendering', 'FX', 'FXCaching', 'Custom', 'Bifrost', 'MASH', 'MotionGraphics', "Turtle"]
plugins = ["Substance", "bifmeshio", "bifrostshellnode", "bifrostvisplugin", "bifrostGraph", "Boss", "MASH", "ATFPlugin", "invertShape", "poseInterpolator", "mayaVnnPlugin", "Turtle"]

version = cmds.about(v=True)
zombieEnv = os.path.join(os.environ['APPDATA'], 'zombieEnv', version, 'prefs', 'shelves')

print('MAYA VERSION: {0}'.format(cmds.about(v=True)))

for p in plugins:
    if cmds.pluginInfo(p, query=True, loaded=True):
        cmds.unloadPlugin(p, force=True)
        cmds.pluginInfo(p, edit=True, autoload=False)

for shelf in shelfvs:
    deleteFile = os.path.join(zombieEnv, 'shelf_{0}.mel'.format(shelf))
    createFile = os.path.join(zombieEnv, 'shelf_{0}.mel.deleted'.format(shelf))
    try:
        name = mel.eval('string $main = ($gShelfTopLevel + "|" + "{0}");'.format(shelf))
        cmds.deleteUI(name, layout=True)

    except Exception, e:
        print(e)

    if os.path.exists(deleteFile):
        os.remove(deleteFile)
    with open(createFile, "w") as file:
        file.write('//DELETED shelf_{0}'.format(shelf))

gshelf = mel.eval("$temp = $gShelfTopLevel")
listShelfs = cmds.tabLayout(gshelf, q=1, childArray=1)
total = len(listShelfs)
pref = 'abc'
shelf = sorted([s for s in listShelfs if s.startswith(pref)]) + sorted([s for s in listShelfs if not s.startswith(pref)])
for i, object in enumerate(shelf):
    i += 1
    sIndex = cmds.tabLayout(gshelf, q=1, childArray=1).index(object) + 1
    cmds.tabLayout(gshelf, e=1, moveTab=(sIndex, i))

for s in cmds.optionVar(list=True):
    if 'shelf' in s:
        for sf in shelfvs:
            if cmds.optionVar(q=s) == 'shelf_{0}'.format(sf):
                cmds.optionVar(remove=s)
            if cmds.optionVar(q=s) == format(sf):
                cmds.optionVar(remove=s)

cmds.optionVar(stringValue=("colorManagementPolicyFileName", "R:/Zombie Dropbox/Zombie Studio (freelance)/INHOUSE/OCIO/maya/ACES.xml"))
cmds.optionVar(stringValue=("zombieEnviroment", True))
cmds.optionVar(intValue=("showHighlightNewFeaturesWindowOnStartup", 0))
cmds.optionVar(stringValue=("showStartupDialog", False))
mel.eval('whatsNewHighlight -highlightOn false;')
mel.eval('whatsNewHighlight -showStartupDialog false;')

unknownNodes = cmds.ls(type="unknown")
for item in unknownNodes:
    if cmds.objExists(item):
        print item
        cmds.delete(item)

cmds.SavePreferences()
cmds.savePrefs()
cmds.saveToolSettings()
cmds.saveViewportSettings()
#cmds.quit(force=True)
