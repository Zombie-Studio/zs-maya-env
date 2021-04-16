"""
SCRIPT ReloadAllReferences
AUTHOR: Thiago Silva/thiago.silva@zombiestudio.com.br
DATE: Tuesday 12 January 2021 14:48

SCRIPT FOR ZOMBIE STUDIO
"""

try:
    from maya import cmds

    references = cmds.ls(type='reference')
    for ref in references:
        if 'sharedReferenceNode' not in ref:
            refFilepath = cmds.referenceQuery(ref, f=True)
        cmds.file(refFilepath, loadReference=ref, options='v=0;')
except Exception as error:
    print(error)
