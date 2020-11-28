import maya.cmds as cmds
import maya.mel as mel

gshelf = mel.eval("$temp = $gShelfTopLevel")
shelfvs = cmds.tabLayout(gshelf, q=1, childArray=1)
total = len(shelfvs)
pref = 'abc'
shelf = sorted([s for s in shelfvs if s.startswith(pref)]) + sorted([s for s in shelfvs if not s.startswith(pref)])
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
