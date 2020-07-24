import pymel.core as pmc



class Scene(object):
    @classmethod
    def getLights(cls):
        mayaLights = pmc.ls(lights=True)
        additionalLights = []
        if Renderer().isArnoldLoaded:
            arnoldLights = pmc.ls(type=['aiAreaLight', 'aiSkyDomeLight', 'aiLightPortal', 'aiPhotometricLight'])
            additionalLights = mayaLights + arnoldLights
        if Renderer().isPrmanLoaded:
            prmanLights = pmc.ls(type=['PxrRectLight', 'PxrDiskLight', 'PxrDistantLight', 'PxrSphereLight', 'PxrDomeLight', 'PxrEnvDayLight', 'PxrAovLight'])
            additionalLights = additionalLights + prmanLights
        return additionalLights

    @classmethod
    def getAovs(cls):
        aovs = list()
        if Renderer().isArnoldLoaded:
            import mtoa
            aovs = [pmc.PyNode(aov) for aov in mtoa.aovs.getAOVNodes()]
        return aovs


class Renderer(object):
    def __init__(self):
        """ This base class returns render specific information and parses them.
        """
        self.defaultRenderGlobals = pmc.PyNode('defaultRenderGlobals')

    @property
    def isValid(self):
        if self.isArnold or self.isPrman or self.isVray:
            return True

    @property
    def current(self):
        """ Returns current renderer """
        return self._currentRenderer()

    @current.setter
    def current(self, name):
        self.defaultRenderGlobals.currentRenderer.set(name)

    @property
    def available(self):
        """ Returns current renderer """
        return self._availableRenderer()

    @property
    def isArnold(self):
        return self._isArnold()

    @property
    def isVray(self):
        return self._isVray()

    @property
    def isPrman(self):
        return self._isPrman()

    @property
    def isArnoldLoaded(self):
        return pmc.pluginInfo('mtoa', q=True, l=True)

    @property
    def isPrmanLoaded(self):
        return pmc.pluginInfo('RenderMan_for_Maya', q=True, l=True)

    @property
    def isVrayLoaded(self):
        return pmc.pluginInfo('vrayformaya', q=True, l=True)

    def _currentRenderer(self):
        """ Returns current active renderer

        @return current active renderer
        @rtype: str
        """
        return self.defaultRenderGlobals.currentRenderer.get()

    def _availableRenderer(self):
        """
        Returns available renderers in Maya
        @return Returns available renderers in Maya
        @rtype: list
        """

        return pmc.renderer(q=True, ava=True)

    def _isArnold(self):
        if self.current == 'arnold':
            return True
        else:
            return False

    def _isVray(self):
        if self.current == 'vray':
            return True
        else:
            return False

    def _isPrman(self):
        if self.current == 'renderManRIS' or self.current == 'renderMan':
            return True
        else:
            return False


class Attribute():

    @classmethod
    def set(cls, dagPath, attribute, value, unlock=False):
        try:
            attr = pmc.Attribute('{}.{}'.format(dagPath, attribute))

            if unlock:
                attr.unlock()

            if not attr.isLocked():
                attr.set(value)

                if unlock:
                    attr.lock()
            else:
                pmc.displayWarning('{}.{} locked. skipped.'.format(dagPath, attribute))

        except (pmc.MayaAttributeError, RuntimeError) as e:
            pass

    @classmethod
    def get(cls, dagPath, attribute):
        try:
            attr = pmc.Attribute('{}.{}'.format(dagPath, attribute))
            return attr.get()
        except pmc.MayaAttributeError as e:
            pass