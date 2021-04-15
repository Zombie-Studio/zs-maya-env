"""
SCRIPT DpAutorig
AUTHOR: Wesley Oliveira/wesley.oliveira@zombiestudio.com.br
DATE: Wednesday 03 February 2021 14:40

SCRIPT FOR ZOMBIE STUDIO
"""

import maya.cmds as cmds
import dpAutoRigSystem
import dpAutoRigSystem.dpAutoRig as autoRig
reload(autoRig)
autoRigUI = autoRig.DP_AutoRig_UI()