"""
SCRIPT ClearColorManagement
AUTHOR: Thiago Silva/thiago.silva@zombiestudio.com.br
DATE: Wednesday 17 March 2021 07:54

SCRIPT FOR ZOMBIE STUDIO
"""

import sgtk
from maya import cmds

try:
    app = sgtk.platform.current_engine()
    pipe = app.context.tank.pipeline_configuration.get_name()

    if pipe == 'zombieProd' or pipe == 'zombieDev':
        if not cmds.colorManagementPrefs(q=True, cmEnabled=True):
            cmds.colorManagementPrefs(e=True, cmEnabled=True)
            cmds.colorManagementPrefs(e=True, configFilePath="R:/Zombie Dropbox/INHOUSE/OCIO/aces_1.0.3/config.ocio")
            cmds.colorManagementPrefs(e=True, policyFileName="R:/Zombie Dropbox/INHOUSE/OCIO/maya/ACES.xml")
            cmds.colorManagementPrefs(e=True, ocioRulesEnabled=True)
            cmds.colorManagementPrefs(e=True, cmConfigFileEnabled=True)
            cmds.colorManagementPrefs(e=True, refresh=True)
    else:
        if cmds.colorManagementPrefs(q=True, cmEnabled=True):
            cmds.colorManagementPrefs(e=True, ocioRulesEnabled=False)
            cmds.colorManagementPrefs(e=True, cmConfigFileEnabled=False)
            cmds.colorManagementPrefs(e=True, cmEnabled=False)
            cmds.colorManagementPrefs(e=True, configFilePath="")
            cmds.colorManagementPrefs(e=True, policyFileName="")
            cmds.colorManagementPrefs(e=True, refresh=False)

    cmds.SavePreferences()
    cmds.savePrefs()
    cmds.saveToolSettings()
    cmds.saveViewportSettings()
except Exception as error:
    print(error)