import lightshader.maya.lighting.gui.lightcontrol as lcgui
from lightshader.maya.qt.helper import mayaMainWindow, wrapinstance, getQObject
from lightshader.qt.interface import QtCore, QtWidgets
import pymel.core as pmc
import maya.OpenMayaUI as openMayaUI
import shiboken2
from lightshader.maya.core import Scene
from lightshader.maya.core import Renderer


class LightControl(lcgui.LightControl):
    def __init__(self):
        super(LightControl, self).__init__(mayaMainWindow())
        self.Renderer = Renderer()

        self.supportedTypes = [pmc.nodetypes.SpotLight, pmc.nodetypes.DirectionalLight, pmc.nodetypes.PointLight, pmc.nodetypes.AreaLight]
        self._setupController()


        self.activeLight = None
        # Function calls
        self._dockCleanUp()
        self._appendRendererLightTypes()
        self._populateLightList()
        self._addMayaUI()
        self._addControls()

    def _setupController(self):
        self.controller = None
        if self.Renderer.isArnold:
            self.controller = {'color': ['lcColorSlider', 'Color'], 'aiColorTemperature': ['lcTemperatureSlider', 'Kelvin'],
                               'intensity': ['lcIntensitySlider', 'Intensity'],
                               'aiExposure': ['lcExposureSlider', 'Exposure'],
                               'aiSpread': ['lcSpreadSlider', 'Spread'], 'aiRoundness': ['lcRoundnessSlider', 'Roundness'],
                               'aiSamples': ['lcSampleSlider', 'Samples'], 'aiSoftEdge': ['lcSoftEdgeSlider', 'Soft Edge'],
                               'aiDiffuse': ['lcDiffuseSlider', 'Diffuse'], 'aiSpecular': ['lsSpecularSlider', 'Specular'],
                               'aiSss': ['lcSssSlider', 'SSS'], 'aiIndirect': ['lcIndirectSlider', 'Indirect'],
                               'aiVolume': ['lcVolumeSlider', 'Volume'], 'coneAngle': ['lcConeAngleSlider', 'Cone Angle'],
                               'penumbraAngle': ['lcPenumbraAngleSlider', 'Penumbra'],
                               'dropoff': ['lcDropoffSlider', 'Dropoff'], 'scale': ['lcScaleSlider', 'Uniform Scale']}
        elif self.Renderer.isPrman:

            self.controller = {'lightColor': ['lcColorSlider', 'Color'],
                            'temperature': ['lcTemperatureSlider', 'Kelvin'],
                           'intensity': ['lcIntensitySlider', 'Intensity'],
                           'exposure': ['lcExposureSlider', 'Exposure'],
                           'emissionFocus': ['lcSpreadSlider', 'Focus'], 'coneSoftness': ['lcRoundnessSlider', 'Softness'],
                           'diffuse': ['lcDiffuseSlider', 'Diffuse'], 'specular': ['lsSpecularSlider', 'Specular'],
                           'coneAngle': ['lcConeAngleSlider', 'Cone Angle']}

    def _addMayaUI(self):
        ptr = long(shiboken2.getCppPointer(self.cameraBoxLayout)[0])
        # Then get the full path to the UI in maya as a string
        mayaFullDagPath = openMayaUI.MQtUtil.fullName(ptr)
        if pmc.modelPanel('lcModelPanel', ex=True):
            pmc.deleteUI('lcModelPanel', panel=True)
        # Find a pointer to the paneLayout that we just created
        self.paneLayoutName = pmc.paneLayout('lcPaneLayout', cn='horizontal2', parent=mayaFullDagPath)
        ptr = openMayaUI.MQtUtil.findControl(self.paneLayoutName)
        # Wrap the pointer into a python QObject
        panelObj = wrapinstance(long(ptr))
        self.lcModelPanel = pmc.modelPanel('lcModelPanel', label='Light Control', p=self.paneLayoutName)
        self.lcModelPanel.setMenuBarVisible(False)
        self.lcModelPanel.unParent()
        # add our QObject reference to the paneLayout to our layout
        self.cameraBoxLayout.addWidget(panelObj)

    def _appendRendererLightTypes(self):
        if self.Renderer.isArnoldLoaded:
            self.supportedTypes = self.supportedTypes + [pmc.nodetypes.AiAreaLight, pmc.nodetypes.AiLightPortal, pmc.nodetypes.AiPhotometricLight]
        if self.Renderer.isPrmanLoaded:
            self.supportedTypes = self.supportedTypes + [pmc.nodetypes.PxrRectLight, pmc.nodetypes.PxrDiskLight, pmc.nodetypes.PxrDistantLight, pmc.nodetypes.PxrSphereLight]

    def _populateLightList(self):

        self.lightList.clear()
        for light in Scene.getLights():
            if not type(light) in self.supportedTypes:
                continue

            name = light.getParent().name()
            listItem = QtWidgets.QListWidgetItem(name)
            listItem.setData(QtCore.Qt.UserRole, name)
            self.lightList.addItem(listItem)

    def refreshLightListEvent(self, *args, **kwargs):
        super(LightControl, self).refreshLightListEvent(args, kwargs)
        self._populateLightList()

    def lightEnableEvent(self, obj, state, *args, **kwargs):
        super(LightControl, self).lightEnableEvent(args, kwargs)
        self.activeLight.visibility.set(state)
        self._updateControls(self.activeLight, enable=state)
        self.useKelvinCheckbox.setEnabled(state)

    def kelvinEnableEvent(self, obj, state, *args, **kwargs):
        super(LightControl, self).kelvinEnableEvent(args, kwargs)
        if self.Renderer.isArnold:
            pmc.setAttr('{}.aiUseColorTemperature'.format(self.activeLight.getShape().name()), state)
            pmc.attrFieldSliderGrp('lcTemperatureSlider', e=True, en=state)
        elif self.Renderer.isPrman:
            pmc.setAttr('{}.enableTemperature'.format(self.activeLight.getShape().name()), state)
            pmc.attrFieldSliderGrp('lcTemperatureSlider', e=True, en=state)
        if not self.activeLight.visibility.get():
            pmc.attrFieldSliderGrp('lcTemperatureSlider', e=True, en=False)

    def lightActivatedEvent(self, obj, lightItem, *args, **kwargs):
        super(LightControl, self).lightActivatedEvent(args, kwargs)
        name = lightItem.data(QtCore.Qt.UserRole)
        light = pmc.PyNode(name)
        self.activeLight = light
        pmc.modelPanel('lcModelPanel', e=True, p=self.paneLayoutName)
        if self.selectLightCheckbox.isChecked():
            pmc.select(light)
        if self.lookThroughLightCheckbox.isChecked():
            self._updateCamera(light.name())

        self._updateControls(light, enable=light.visibility.get())
        self.statusBar().showMessage('Controlling {}'.format(light.name()))

    def _updateCamera(self, lightName):
        pmc.lookThru('lcModelPanel', lightName)

    def _updateControls(self, light, enable=True):
        if self.Renderer.isArnoldLoaded and self.Renderer.isArnold:
            kelvinState = pmc.getAttr('{}.aiUseColorTemperature'.format(light.getShape().name()))
            self.useKelvinCheckbox.setChecked(kelvinState)
        elif self.Renderer.isPrmanLoaded and self.Renderer.isPrman:
            kelvinState = pmc.getAttr('{}.enableTemperature'.format(light.getShape().name()))
            self.useKelvinCheckbox.setChecked(kelvinState)
        else:
            kelvinState = False
            self.useKelvinCheckbox.setHidden(True)


        lightState = light.visibility.get()
        self.lightEnableCheckbox.setChecked(lightState)
        self.useKelvinCheckbox.setEnabled(lightState)

        for key, value in self.controller.iteritems():
            slider, name = value
            if key == 'scale':
                self._updateSlider(slider, light, key, enable)
            else:
                self._updateSlider(slider, light.getShape(), key, enable)

        if light.visibility.get():
            pmc.attrFieldSliderGrp('lcTemperatureSlider', e=True, en=kelvinState)

    def _updateSlider(self, sliderName, lightShape, attribute, state):
        # Checking for hidden attributes and skipping
        try:
            if pmc.Attribute('%s.%s' % (lightShape, attribute)).isHidden():
                pmc.attrFieldSliderGrp(sliderName, edit=True, visible=False)
                return
        except pmc.MayaAttributeError:
            pass

        if sliderName == 'lcColorSlider':
            pmc.attrColorSliderGrp(sliderName, edit=True, visible=True, at='%s.%s' % (lightShape, attribute))
            pmc.attrColorSliderGrp(sliderName, edit=True, cw4=[60, 70, 10, 10])
            pmc.attrColorSliderGrp(sliderName, edit=True, en=state)
            return

        if sliderName == 'lcScaleSlider':
            pmc.attrFieldGrp(sliderName, edit=True, cw4=[60, 65, 65, 65], visible=True,
                             at='%s.%s' % (lightShape, attribute))
            pmc.attrFieldGrp(sliderName, edit=True, en=state)
            return

        pmc.attrFieldSliderGrp(sliderName, edit=True, cw=[1, 60])
        pmc.attrFieldSliderGrp(sliderName, edit=True, cw=[2, 70])

        try:
            pmc.attrFieldSliderGrp(sliderName, edit=True, visible=True, at='%s.%s' % (lightShape, attribute))
        except RuntimeError:
            pmc.attrFieldSliderGrp(sliderName, edit=True, visible=False)

        pmc.attrFieldSliderGrp(sliderName, edit=True, en=state)

    def _addControls(self):
        self._deleteExisting()

        # Converting and Adding maya slider
        self.controlBoxLayout.addWidget(LightControl._addSeparator())
        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrColorSliderGrp('lcColorSlider', label='{:>10}'.format('Color:'), cw4=[55, 60, 60, 40],
                                   visible=False)))

        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrFieldSliderGrp('lcTemperatureSlider', label='{:>10}'.format('Kelvin:'), pre=0, visible=False,
                                   min=-99999, max=99999)))
        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrFieldSliderGrp('lcIntensitySlider', label='{:>10}'.format('Intensity:'), visible=False, min=-9999,
                                   max=9999)))
        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrFieldSliderGrp('lcExposureSlider', label='{:>10}'.format('Exposure:'), visible=False, min=-9999,
                                   max=9999)))
        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrFieldSliderGrp('lcSpreadSlider', label='{:>10}'.format('Spread:'), visible=False, min=-9999,
                                   max=9999)))
        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrFieldSliderGrp('lcRoundnessSlider', label='{:>10}'.format('Roundness:'), visible=False, min=-9999,
                                   max=9999)))
        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrFieldSliderGrp('lcSoftEdgeSlider', label='{:>10}'.format('Soft Edge:'), visible=False, min=-9999,
                                   max=9999)))
        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrFieldSliderGrp('lcConeAngleSlider', label='{:>10}'.format('Cone:'), pre=2, visible=False, min=-9999,
                                   max=9999)))
        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrFieldSliderGrp('lcPenumbraAngleSlider', label='{:>10}'.format('Penumbra:'), pre=2, visible=False,
                                   min=-9999, max=9999)))
        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrFieldSliderGrp('lcDropoffSlider', label='{:>10}'.format('Dropoff:'), pre=2, visible=False,
                                   min=-9999, max=9999)))
        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrFieldSliderGrp('lcSampleSlider', label='{:>10}'.format('Samples:'), visible=False, min=-9999,
                                   max=9999)))
        self.controlBoxLayout.addWidget(LightControl._addSeparator())
        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrFieldSliderGrp('lcDiffuseSlider', label='{:>10}'.format('Diffuse:'), visible=False, min=-9999,
                                   max=9999)))
        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrFieldSliderGrp('lsSpecularSlider', label='{:>10}'.format('Specular:'), visible=False, min=-9999,
                                   max=9999)))
        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrFieldSliderGrp('lcSssSlider', label='{:>10}'.format('SSS:'), visible=False, min=-9999, max=9999)))
        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrFieldSliderGrp('lcIndirectSlider', label='{:>10}'.format('Indirect:'), visible=False, min=-9999,
                                   max=9999)))
        self.controlBoxLayout.addWidget(getQObject(
            pmc.attrFieldSliderGrp('lcVolumeSlider', label='{:>10}'.format('Volume:'), visible=False, min=-9999,
                                   max=9999)))
        self.controlBoxLayout.addWidget(LightControl._addSeparator())
        self.controlBoxLayout.addWidget(
            getQObject(pmc.attrFieldGrp('lcScaleSlider', label='{:>10}'.format('Scale:'), pre=3, visible=False)))
        self.controlBoxLayout.addWidget(LightControl._addSeparator())
        self.controlBoxLayout.addItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

    @classmethod
    def _addSeparator(cls):
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        return line

    def _deleteExisting(self):

        for key, value in self.controller.iteritems():
            slider, name = value

            if slider == 'lcColorSlider' and pmc.attrColorSliderGrp(slider, ex=True):
                pmc.deleteUI(slider)
            elif slider == 'lcScaleSlider' and pmc.attrFieldGrp(slider, ex=True):
                pmc.deleteUI(slider)
            else:
                if pmc.attrFieldSliderGrp(slider, ex=True):
                    pmc.deleteUI(slider)
