"""
SCRIPT ClearReferences
AUTHOR: Thiago Silva/thiago.silva@zombiestudio.com.br
DATE: Wednesday 24 March 2021 13:39

SCRIPT FOR ZOMBIE STUDIO
"""

try:
    import pymel.core as pm
    refs_to_delete = []
    for ref in pm.ls(type='reference'):
        try:
            fileRef = pm.FileReference(ref).path
        except RuntimeError:
            ref.unlock()
            refs_to_delete.append(ref)
            continue
    pm.delete(refs_to_delete)
except Exception as error:
    print(error)