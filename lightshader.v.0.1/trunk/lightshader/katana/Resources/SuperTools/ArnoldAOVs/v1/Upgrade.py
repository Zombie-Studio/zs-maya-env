__all__ = ['Upgrade']


from Katana import NodegraphAPI, Utils
import logging

log = logging.getLogger("ArnoldAOVs_LS.Upgrade")


def Upgrade(node):
    Utils.UndoStack.DisableCapture()
    try:
        pass
        # This is where you would detect an out-of-date version:
        #    node.getParameter('version')
        # and upgrade the internal network.
    except Exception as exception:
        log.exception('Error upgrading ArnoldAOVs_LS node "%s": %s'
                      % (node.getName(), str(exception)))
    finally:
        Utils.UndoStack.EnableCapture()
