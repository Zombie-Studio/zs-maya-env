"""
SCRIPT ZsLookdevLightAces
AUTHOR: Isaac Buzzola/isaac.buzzola@zombiestudio.com.br
DATE: Friday 11 December 2020 15:11

SCRIPT FOR ZOMBIE STUDIO
"""

from maya import cmds
cmds.file("R:/Zombie Dropbox/INHOUSE/HDRI/light_setup_aces.ma", r=True, type="mayaAscii", gr=True ,ignoreVersion=True, mergeNamespacesOnClash=True, namespace=":", options="v=0")