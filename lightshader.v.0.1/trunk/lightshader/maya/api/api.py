import maya.api.OpenMaya as om
import warnings


class API(object):
    @classmethod
    def getDagNode(cls, dagPath):
        """

        @param dagPath Path or Object
        @param dagPath om.MDagPath or string
        @return om.MFnDagNode
        """
        return om.MFnDagNode(dagPath)

    @classmethod
    def getSelectionList(cls, dagPath):
        """

        @param dagPath dagPath object
        @type dagPath om.MDagPath
        @return om.MSelectionList
        """
        selList = om.MSelectionList()
        selList.add(dagPath)
        return selList

    @classmethod
    def getActiveSelectionList(cls):
        """
        @return: om.MSelectionList
        """

        return om.MGlobal.getActiveSelectionList()

    @classmethod
    def getDagPath(cls, fullPathName):
        """

        @param fullPathName FullPathName of Object
        @return om.MDagPath
        """
        return cls.getSelectionList(fullPathName).getDagPath(0)

    @classmethod
    def getHierarchy(cls, dagPath, kTypes='all', ignoreTypes=[]):
        """ Returns list of all dependents of current selection

        @param kTypes List of type of objects eg. kTransform or all
        @return [fullDagPaths]
        """

        if isinstance(dagPath, str):
            dagPath = cls.getDagPath(dagPath)
        if isinstance(kTypes, str):
            kTypes = [kTypes]
        elif not isinstance(kTypes, list):
            return warnings.warn('Expected kTypes to be of type list')

        if isinstance(ignoreTypes, str):
            ignoreTypes = [ignoreTypes]
        elif not isinstance(ignoreTypes, list):
            return warnings.warn('Expected kTypes to be of type list')

        tmpList = list()

        # Recursive call function
        def getChildren(dagPath):
            count = dagPath.childCount()
            dagNode = cls.getDagNode(dagPath)
            fullPathName = dagPath.fullPathName()
            nodeType = dagPath.node().apiTypeStr
            if count != 0:
                for id in range(count):  # Finds all children
                    child = dagNode.child(id)
                    childDagNode = cls.getDagNode(child)
                    getChildren(cls.getDagPath(childDagNode.fullPathName()))  # Recursively checks for children
            if 'all' in kTypes and nodeType not in ignoreTypes:
                tmpList.append(fullPathName)
            elif nodeType in kTypes:
                tmpList.append(fullPathName)

        getChildren(dagPath)
        return tmpList

    @classmethod
    def getHierarchyOfSelection(cls, kTypes='all', ignoreTypes=[]):
        selection_iter = om.MItSelectionList(cls.getActiveSelectionList())
        tmpList = list()
        # Loop though iterator objects
        while not selection_iter.isDone():
            dagPath = selection_iter.getDagPath()
            tmpList += cls.getHierarchy(dagPath, kTypes=kTypes, ignoreTypes=ignoreTypes)
            selection_iter.next()
        return list(set(tmpList))

    @classmethod
    def getMObject(cls, objectName=None):
        if objectName:
            sel = om.MSelectionList()
            sel.add(objectName)
            dagPath = sel.getDagPath(0)
            return dagPath.node()
        else:
            sel = om.MGlobal.getActiveSelectionList()
            selIter = om.MItSelectionList(sel)
            tmpList = list()
            # Loop though iterator objects
            while not selIter.isDone():
                tmpList.append(selIter.getDagPath().node())
                selIter.next()
            return tmpList

