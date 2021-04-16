"""
SCRIPT ZsRgbaLight
AUTHOR: Isaac Buzzola/isaac.buzzola@zombiestudio.com.br
DATE: Friday 11 December 2020 15:30

SCRIPT FOR ZOMBIE STUDIO
"""

try:
    import mtoa
    import mtoa.aovs as aovs
    from maya import cmds

    nLights = cmds.ls(sl=True)
    nameGroup = []

    for i in range(len(nLights)):
        nameGroup.append(nLights[i].split("_")[0])
        nameGroup = [str(item) for item in nameGroup]

    i = 0
    for light in nLights:
        cmds.setAttr(light + ".aiAov", nameGroup[i], type="string")
        i = i + 1

    lightMixer = sorted(set(nameGroup))
    for i in lightMixer:
        aovs.AOVInterface().addAOV('RGBA_' + i, aovType='rgb')
except Exception as error:
    print(error)