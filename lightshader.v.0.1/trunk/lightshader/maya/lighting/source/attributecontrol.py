import lightshader.maya.lighting.gui.attributecontrol as acgui
import lightshader.maya.lighting.gui.subclass as subclass
from lightshader.maya.qt.helper import mayaMainWindow, wrapinstance, getQObject
from lightshader.maya.api.api import API
from lightshader.qt.interface import QtCore, QtWidgets
import pymel.core as pmc
from lightshader.maya.core import Scene, Renderer, Attribute
import random


class AttributeControl(acgui.AttributeControl):
    def __init__(self):
        self.Renderer = Renderer()

        super(AttributeControl, self).__init__(mayaMainWindow())
        self._populateObjectList()

    def _populateObjectList(self, append=False, recursive=False):

        if not append:
            self.objectList.clear()
        activeSelection = pmc.selected()
        if not activeSelection:
            return pmc.displayWarning('Please make a valid selection')

        items = list()

        if not recursive:
            for obj in API.getHierarchyOfSelection():
                if obj not in [item.text() for item in self.objectList.allItems()]:
                    items.append(obj)
        else:
            for obj in activeSelection:
                items.append(obj.fullPath())

        self.objectList.addItems(items)
        self.objectList.sortItems()
        self.objectList.selectAll()

    def objectControlEvent(self, button, *args, **kwargs):
        super(AttributeControl, self).objectControlEvent(button, args, kwargs)
        mode = button.property('mode')
        if mode == 'refresh':
            self._populateObjectList()
        elif mode == 'add':
            self._populateObjectList(append=True)
        elif mode == 'clear':
            self.objectList.clear()
        elif mode == 'recursive':
            self._populateObjectList(append=False, recursive=True)

    def controlSignalEvent(self, button, *args, **kwargs):
        super(AttributeControl, self).controlSignalEvent(button, args, kwargs)
        text = button.text()
        attribute = button.property('attribute')
        value = button.property('value')
        widget = button.property('control')
        force = self.forceAttributesCheckbox.isChecked()
        pmc.undoInfo(openChunk=True)

        if text == 'Set':
            for item in self.objectList.selectedItems():

                if self.__typeValidation(item):
                    pass
                else:
                    continue
                if value is not None:
                    Attribute.set(item.text(), attribute, value, unlock=force)
                elif widget:
                    if attribute == 'aiSssSetname' or attribute == 'aiAov':
                        value = widget.text()
                    elif attribute == 'color' or attribute == 'lightColor':
                        value = (widget.property('red'), widget.property('green'), widget.property('blue'))

                    else:
                        value = widget.value()

                    if attribute == 'sxyz':
                        for attr in ['sx', 'sy', 'sz']:
                            Attribute.set(item.text(), attr, value, unlock=force)
                    else:
                        Attribute.set(item.text(), attribute, value, unlock=force)
                value = None
        elif text == 'Increment':
            for item in self.objectList.selectedItems():

                if self.__typeValidation(item):
                    pass
                else:
                    continue


                if attribute == 'sxyz':
                    for attr in ['sx', 'sy', 'sz']:
                        currentValue = Attribute.get(item.text(), attr)
                        incrementValue = currentValue + widget.value()
                        Attribute.set(item.text(), attr, incrementValue, unlock=force)
                    continue

                currentValue = Attribute.get(item.text(), attribute)
                if widget and currentValue is not None:
                    incrementValue = currentValue + widget.value()
                    Attribute.set(item.text(), attribute, incrementValue, unlock=force)

        elif text == 'Random':
            randomDialog = subclass.RandomDialog(self)
            randomDialog.exec_()
            if randomDialog.value:
                for item in self.objectList.selectedItems():
                    if self.__typeValidation(item):
                        pass
                    else:
                        continue
                    if attribute == 'sxyz':
                        value = randomDialog.randomize()
                        for attr in ['sx', 'sy', 'sz']:
                            print attr
                            Attribute.set(item.text(), attr, value, unlock=force)
                    else:
                        Attribute.set(item.text(), attribute, randomDialog.randomize(), unlock=force)
        else:
            for item in self.objectList.selectedItems():
                if self.__typeValidation(item):
                    pass
                else:
                    continue

                if attribute == 'sxyz':
                        for attr in ['sx', 'sy', 'sz']:
                            Attribute.set(item.text(), attr, value, unlock=force)
                else:
                    Attribute.set(item.text(), attribute, value, unlock=force)

        pmc.undoInfo(closeChunk=True)

    def __typeValidation(self, item):
        if isinstance(pmc.PyNode(item.text()), pmc.nodetypes.Transform) and self.tab.currentIndex() == 0:  # making sure only on transforms on transform tab
            return True
        elif isinstance(pmc.PyNode(item.text()), pmc.nodetypes.Transform) is False and self.tab.currentIndex() == 0:
            return False
        elif isinstance(pmc.PyNode(item.text()), pmc.nodetypes.Transform) and self.tab.currentIndex() != 0:  # making sure transforms are skipped on other tabs
            return False
        else:
            return True

    def _setupMeshTabWidgets(self):
        super(AttributeControl, self)._setupMeshTabWidgets()

        if self.Renderer.isArnold:

            self.meshLayout.addWidget(
                self._groupWidgets([self.addControl('Opaque', {'Off': 0, 'On': 1}, 'aiOpaque'),
                                    self.addControl('Matte', {'Off': 0, 'On': 1}, 'aiMatte'),
                                    self.addControl('Primary Visibility', {'Off': 0, 'On': 1}, 'primaryVisibility'),
                                    self.addControl('Cast Shadows', {'Off': 0, 'On': 1}, 'castsShadows'),
                                    self.addControl('Diffuse Reflection', {'Off': 0, 'On': 1}, 'aiVisibleInDiffuseReflection'),
                                    self.addControl('Specular Reflection', {'Off': 0, 'On': 1}, 'aiVisibleInSpecularReflection'),
                                    self.addControl('Diffuse Transmission', {'Off': 0, 'On': 1}, 'aiVisibleInDiffuseTransmission'),
                                    self.addControl('Specular Transmission', {'Off': 0, 'On': 1}, 'aiVisibleInSpecularTransmission'),
                                    self.addControl('Visible in Volume', {'Off': 0, 'On': 1}, 'aiVisibleInVolume'),
                                    self.addControl('Self Shadows', {'Off': 0, 'On': 1}, 'aiSelfShadows'),
                                    self.addControl('SSS Set Name', 'custom', 'aiSssSetname'),

                                    ], 'Arnold Visibility'))

            self.meshLayout.addWidget(
                self._groupWidgets([self.addControl('Type', {'None': 0, 'Catclark': 1, 'Linear': 2}, 'aiSubdivType'),
                                    self.addControl('Iterations', 'intSlider', 'aiSubdivIterations'),
                                    self.addControl('Adaptive Metric', {'Auto': 0, 'Edge Length': 1, 'Flatness': 2}, 'aiSubdivAdaptiveMetric'),
                                    self.addControl('Adaptive Error', 'floatSlider', 'aiSubdivPixelError'),
                                    self.addControl('Adaptive Space', {'Raster': 0, 'Object': 1}, 'aiSubdivAdaptiveSpace'),
                                    self.addControl('UV Smoothing', {'Pin Corners': 0, 'Pin Borders': 1, 'Linear': 2, 'Smooth': 3}, 'aiSubdivUvSmoothing'),
                                    self.addControl('Smooth Tangents', {'Off': 0, 'On': 1}, 'aiSubdivSmoothDerivs'),
                                    ], 'Arnold Subdivision'))

            self.meshLayout.addWidget(
                self._groupWidgets([self.addControl('Height', 'floatSlider', 'aiDispHeight'),
                                    self.addControl('Bounds Padding', 'floatSlider', 'aiDispPadding'),
                                    self.addControl('Zero Value', 'floatSlider', 'aiDispZeroValue'),
                                    self.addControl('Auto Bump', {'Off': 0, 'On': 1}, 'aiDispAutobump'),
                                    ], 'Arnold Displacement'))


        elif self.Renderer.isPrman:
            self.meshLayout.addWidget(
                self._groupWidgets([
                                    self.addControl('Ptex Face Offset', 'intSlider', 'rman__torattr___ptexFaceOffset'),
                                    self.addControl('Output Tangents', {'Off': 0, 'On': 1}, 'rman__torattr___outputTangents'),
                                    self.addControl('Camera Visibility', {'Off': 0, 'On': 1}, 'rman__riattr__visibility_camera'),
                                    self.addControl('Indirect Visibility', {'Off': 0, 'On': 1}, 'rman__riattr__visibility_indirect'),
                                    self.addControl('Transmission Visibility', {'Off': 0, 'On': 1}, 'rman__riattr__visibility_transmission'),
                                    self.addControl('Output Color Sets', {'Off': 0, 'On': 1}, 'rman__torattr___outputColorSets'),
                                    ], 'Prman Attributes'))

            self.meshLayout.addWidget(
                self._groupWidgets([
                                    self.addControl('Type', {'None': 2, 'Catclark': 0, 'Loop': 1}, 'rman__torattr___subdivScheme'),
                                    self.addControl('Face Varying', {'0': 0, '1': 1, '2': 2, '3': 3}, 'rman__torattr___subdivFacevaryingInterp'),

                                    ], 'Prman Subdivision'))

        elif self.Renderer.isVray:
            print 'vray mesh tab'

    def _setupLightTabWidgets(self):
        super(AttributeControl, self)._setupLightTabWidgets()

        if self.Renderer.isArnold:

            self.lightLayout.addWidget(
                self._groupWidgets([self.addControl('Exposure', 'floatSlider', 'exposure'),
                                    self.addControl('Kelvin', {'Off': 0, 'On': 1}, 'aiUseColorTemperature'),
                                    self.addControl('Kelvin', 'intSlider', 'aiColorTemperature'),
                                    self.addControl('Primary Visibility', {'Off': 0, 'On': 1}, 'primaryVisibility'),
                                    self.addControl('Light Type', {'Cylinder': 'cylinder', 'Quad': 'quad', 'Disk': 'disk'}, 'aiTranslator'),
                                    self.addControl('Spread', 'floatSlider', 'aiSpread'),
                                    self.addControl('Roundness', 'floatSlider', 'aiRoundness'),
                                    self.addControl('Soft Edge', 'floatSlider', 'aiSoftEdge'),
                                    self.addControl('Samples', 'intSlider', 'aiSamples'),
                                    self.addControl('Volume Samples', 'intSlider', 'aiVolumeSamples'),
                                    self.addControl('Normalize', {'Off': 0, 'On': 1}, 'aiNormalize'),
                                    self.addControl('Cast Shadows', {'Off': 0, 'On': 1}, 'aiCastShadows'),
                                    self.addControl('Volumetric Shadows', {'Off': 0, 'On': 1}, 'aiCastVolumetricShadows'),
                                    ], 'Arnold Light Attributes'))

            self.lightLayout.addWidget(
                self._groupWidgets([self.addControl('Diffuse', 'floatSlider', 'aiDiffuse'),
                                    self.addControl('Specular', 'floatSlider', 'aiSpecular'),
                                    self.addControl('SSS', 'floatSlider', 'aiSss'),
                                    self.addControl('Indirect', 'floatSlider', 'aiIndirect'),
                                    self.addControl('Volume', 'floatSlider', 'aiVolume'),
                                    self.addControl('AOV Light Group', 'custom', 'aiAov'),
                                    ], 'Arnold Light Visibility'))



        elif self.Renderer.isPrman:
            self.lightColorWidget.setHidden(True)
            self.lightLayout.addWidget(
                self._groupWidgets([
                                    self.addControl('Color', 'colorSlider', 'lightColor'),
                                    self.addControl('Kelvin', {'Off': 0, 'On': 1}, 'enableTemperature'),
                                    self.addControl('Kelvin', 'intSlider', 'temperature'),
                                    self.addControl('Focus', 'floatSlider', 'emissionFocus'),
                                    self.addControl('Angle Extent', 'floatSlider', 'angleExtent', default=0.530),
                                    self.addControl('Fixed Samples', 'intSlider', 'fixedSampleCount'),
                                    self.addControl('Importance', 'floatSlider', 'importanceMultiplier', default=1),
                                    self.addControl('Normalize', {'Off': 0, 'On': 1}, 'areaNormalize'),
                                    self.addControl('Cast Shadows', {'Off': 0, 'On': 1}, 'enableShadows'),
                                    self.addControl('Thin Shadow', {'Off': 0, 'On': 1}, 'thinShadow'),
                                    ], 'Prman Light Attributes'))

            self.lightLayout.addWidget(
                self._groupWidgets([self.addControl('Diffuse', 'floatSlider', 'diffuse'),
                                    self.addControl('Specular', 'floatSlider', 'specular'),
                                    self.addControl('Camera Visibility', {'Off': 0, 'On': 1}, 'rman__riattr__visibility_camera'),
                                    ], 'Prman Light Visibility'))
        elif self.Renderer.isVray:
            print 'vray light tab'