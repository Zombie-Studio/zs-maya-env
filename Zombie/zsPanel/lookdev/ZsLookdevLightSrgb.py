"""
SCRIPT ZsLookdevLightSrgb
AUTHOR: Isaac Buzzola/isaac.buzzola@zombiestudio.com.br
DATE: Friday 11 December 2020 15:46

SCRIPT FOR ZOMBIE STUDIO
"""
try:
    import os
    from maya import cmds
    file = "R:/Zombie Dropbox/INHOUSE/HDRI/light_setup.ma"
    if os.path.exists(file):
        cmds.file(fiile, r=True, type="mayaAscii", gr=True ,ignoreVersion=True, mergeNamespacesOnClash=True, namespace=":", options="v=0")
    else:
        raise GeneratorExit('Arquivo light_setup.ma nao encontrado')

except Exception as error:
    print(error)