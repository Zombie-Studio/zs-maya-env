"""
SCRIPT ZsCreateAovs
AUTHOR: Isaac Buzzola/isaac.buzzola@zombiestudio.com.br
DATE: Friday 11 December 2020 15:12

SCRIPT FOR ZOMBIE STUDIO
"""

import mtoa
import mtoa.aovs as aovs
from maya import cmds


aovs.AOVInterface().addAOV('N', aovType='vector')
aovs.AOVInterface().addAOV('P', aovType='vector')
aovs.AOVInterface().addAOV('Z', aovType='float')
aovs.AOVInterface().addAOV('coat', aovType='rgb')
aovs.AOVInterface().addAOV('diffuse', aovType='rgb')
aovs.AOVInterface().addAOV('direct', aovType='rgb')
aovs.AOVInterface().addAOV('indirect', aovType='rgb')
aovs.AOVInterface().addAOV('specular', aovType='rgb')
aovs.AOVInterface().addAOV('sss', aovType='rgb')
aovs.AOVInterface().addAOV('transmission', aovType='rgb')
aovs.AOVInterface().addAOV('crypto_asset', aovShader='cryptomatte', aovType='rgb')
aovs.AOVInterface().addAOV('crypto_material',  aovShader='cryptomatte', aovType='rgb')
aovs.AOVInterface().addAOV('crypto_object',  aovShader='cryptomatte', aovType='rgb')