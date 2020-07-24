from lightshader.qt.interface import QtWidgets, QtCore, addBorder, Signal
from lightshader.maya.qt.base import BaseWindow
from lightshader.maya.lighting.gui.subclass import ListWidget
import random
import sys


class AttributeControl(BaseWindow):
    def __init__(self, mainWindow):
        super(AttributeControl, self).__init__(mainWindow)
        self.title = 'Attribute Control'
        self.documentationUrl = self.documentationUrl + 'documentation/attributecontrol/'
        self.resize(550, 800)
        self.objectBoxHeight = 150
        self.controlButtonWidth = 250
        self.setFixedWidth(550)
        self._setupWindow()
        self._addWidgets()
        self._setupWidgets()
        self._setupTransformTabWidgets()
        self._setupMeshTabWidgets()
        self._setupLightTabWidgets()
        self._extendMenu()

    def _setupWindow(self):
        super(AttributeControl, self)._setupWindow()

        self.baseLayout = QtWidgets.QVBoxLayout()
        self.objectList = ListWidget()
        self.objectBox = QtWidgets.QGroupBox('Objects')
        self.objectBoxLayout = QtWidgets.QHBoxLayout()
        self.objectBoxControlLayout = QtWidgets.QVBoxLayout()
        self.controlBox = QtWidgets.QGroupBox('Control')
        self.controlBoxLayout = QtWidgets.QVBoxLayout()
        self.closeButton = QtWidgets.QPushButton('Close')
        self.tab = QtWidgets.QTabWidget()
        self.addObjectButton = QtWidgets.QPushButton(u'\u271A')
        self.removeObjectButton = QtWidgets.QPushButton(u'\u2716')
        self.refreshObjectButton = QtWidgets.QPushButton(u'\u267B')
        self.recursiveObjectButton = QtWidgets.QPushButton(u'\u272A')

    def _addWidgets(self):
        self.parentWidget.setLayout(self.baseLayout)
        self.objectBox.setLayout(self.objectBoxLayout)
        self.controlBox.setLayout(self.controlBoxLayout)
        self.baseLayout.addWidget(self.objectBox)
        self.baseLayout.addWidget(self.controlBox)
        self.baseLayout.addWidget(self.closeButton)
        self.objectBoxLayout.addWidget(self.objectList)
        self.objectBoxLayout.addLayout(self.objectBoxControlLayout)
        self.objectBoxControlLayout.addWidget(self.addObjectButton)
        self.objectBoxControlLayout.addWidget(self.removeObjectButton)
        self.objectBoxControlLayout.addWidget(self.refreshObjectButton)
        self.objectBoxControlLayout.addWidget(self.recursiveObjectButton)
        self.controlBoxLayout.addWidget(self.tab)
        self.transformLayout = QtWidgets.QVBoxLayout()
        self.meshLayout = QtWidgets.QVBoxLayout()
        self.lightLayout = QtWidgets.QVBoxLayout()
        self.otherLayout = QtWidgets.QVBoxLayout()

    def _setupWidgets(self):
        self.objectBox.setFixedHeight(self.objectBoxHeight)
        addBorder(self.objectBox)
        addBorder(self.controlBox)
        self.__setupTab('Transform', self.transformLayout)
        self.__setupTab('Mesh', self.meshLayout)
        self.__setupTab('Light', self.lightLayout)
        #self.__setupTab('Other', self.otherLayout)
        self.addObjectButton.setProperty('mode', 'add')
        self.removeObjectButton.setProperty('mode', 'clear')
        self.refreshObjectButton.setProperty('mode', 'refresh')
        self.recursiveObjectButton.setProperty('mode', 'recursive')
        self.Signal.addSignal(self.addObjectButton, 'clicked', self.objectControlEvent)
        self.Signal.addSignal(self.removeObjectButton, 'clicked', self.objectControlEvent)
        self.Signal.addSignal(self.refreshObjectButton, 'clicked', self.objectControlEvent)
        self.Signal.addSignal(self.recursiveObjectButton, 'clicked', self.objectControlEvent)
        self.Signal.addSignal(self.closeButton, 'clicked', self.closeButtonEvent)
        self.objectBoxLayout.setSpacing(6)

    def _extendMenu(self):
        self.menuBar.viewMenu.deleteLater()
        self.forceAttributesCheckbox = QtWidgets.QAction('Force Attributes', self.menuBar.editMenu)
        self.forceAttributesCheckbox.setCheckable(True)
        self.menuBar.editMenu.addAction(self.forceAttributesCheckbox)

    def __setupTab(self, name, layout):
        main_widget = QtWidgets.QWidget()
        w = QtWidgets.QWidget()
        w.setLayout(layout)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(w)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(scroll_area)

        main_widget.setLayout(layout)
        self.tab.addTab(main_widget, name)

    def _setupTransformTabWidgets(self):

        self.transformLayout.addWidget(self._groupWidgets([self.addControl('X', QtWidgets.QDoubleSpinBox(), 'tx'),
                                                           self.addControl('Y', QtWidgets.QDoubleSpinBox(), 'ty'),
                                                           self.addControl('Z', QtWidgets.QDoubleSpinBox(), 'tz')
                                                           ], 'Translate'))
        self.transformLayout.addWidget(self._groupWidgets([self.addControl('X', QtWidgets.QDoubleSpinBox(), 'rx'),
                                                           self.addControl('Y', QtWidgets.QDoubleSpinBox(), 'ry'),
                                                           self.addControl('Z', QtWidgets.QDoubleSpinBox(), 'rz')
                                                           ], 'Rotate'))
        self.transformLayout.addWidget(
            self._groupWidgets([self.addControl('X', QtWidgets.QDoubleSpinBox(), 'sx', default=1),
                                self.addControl('Y', QtWidgets.QDoubleSpinBox(), 'sy', default=1),
                                self.addControl('Z', QtWidgets.QDoubleSpinBox(), 'sz', default=1),
                                self.addControl('XYZ', QtWidgets.QDoubleSpinBox(), 'sxyz', default=1)
                                ], 'Scale'))

        self.transformLayout.addWidget(
            self._groupWidgets([self.addControl('Visibility', {'Off': 0, 'On': 1}, 'visibility'),
                                self.addControl('LOD Visibility', {'Off': 0, 'On': 1}, 'lodVisibility'),
                                self.addControl('Template', {'Off': 0, 'On': 1}, 'template'),
                                self.addControl('Display', {'Normal': 0, 'Template': 1, 'Reference': 2},
                                                'overrideDisplayType'),
                                self.addControl('Overrides', {'Off': 0, 'On': 1}, 'overrideEnabled'),
                                self.addControl('LOD', {'Full': 0, 'BBox': 1}, 'overrideLevelOfDetail'),
                                ], 'Display'))

        self.transformLayout.addItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

    def _setupMeshTabWidgets(self):

        self.meshLayout.addWidget(
            self._groupWidgets([self.addControl('Smooth Mesh Preview', {'Off': 0, 'On': 2}, 'displaySmoothMesh'),
                                self.addControl('Use Smooth for Rendering', {'Off': 0, 'On': 1},
                                                'useSmoothPreviewForRender'),
                                self.addControl('Render Level', QtWidgets.QDoubleSpinBox(), 'renderSmoothLevel'),
                                self.addControl('Visibilty', {'Off': 0, 'On': 1}, 'visibility')

                                ], 'Mesh Preview'))

        self.meshLayout.addWidget(
            self._groupWidgets([self.addControl('Casts Shadows', {'Off': 0, 'On': 1}, 'castsShadows'),
                                self.addControl('Receive Shadows', {'Off': 0, 'On': 1}, 'receiveShadows'),
                                self.addControl('Primary Visibility', {'Off': 0, 'On': 1}, 'primaryVisibility'),
                                self.addControl('Visible Reflections', {'Off': 0, 'On': 1}, 'visibleInReflections'),
                                self.addControl('Visible Refractions', {'Off': 0, 'On': 1}, 'visibleInRefractions'),
                                self.addControl('Double Sided', {'Off': 0, 'On': 1}, 'doubleSided'),

                                ], 'Render Stats'))

        self.meshLayout.addItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

    def _setupLightTabWidgets(self):
        self.lightColorWidget = self.addControl('Color', 'colorSlider', 'color')
        self.lightLayout.addWidget(
            self._groupWidgets([self.lightColorWidget,
                                self.addControl('Intensity', QtWidgets.QDoubleSpinBox(), 'intensity'),
                                self.addControl('Decay', {'No': 0, 'Linear': 1, 'Quadratic': 2, 'Cubic': 3}, 'decayRate'),
                                self.addControl('Visibility', {'Off': 0, 'On': 1}, 'visibility')

                                ], 'Light Attributes'))



        self.lightLayout.addItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))



    def _groupWidgets(self, widgets, title):
        box = QtWidgets.QGroupBox(title)
        layout = QtWidgets.QVBoxLayout()
        box.setLayout(layout)
        addBorder(box)
        for widget in widgets:
            layout.addWidget(widget)
        return box

    def addControl(self, name, control, attribute, default=None):
        buttonHeight = 18
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        widget.setLayout(layout)
        label = QtWidgets.QLabel(name)
        incrementButton = QtWidgets.QPushButton('Increment')
        randomButton = QtWidgets.QPushButton('Random')
        setButton = QtWidgets.QPushButton('Set')
        incrementButton.setFixedSize(self.controlButtonWidth / 3, buttonHeight)
        randomButton.setFixedSize(self.controlButtonWidth / 3, buttonHeight)
        setButton.setFixedSize(self.controlButtonWidth / 3, buttonHeight)
        # Adding Widgets
        layout.addWidget(label)

        if control == 'intSlider':
            control = QtWidgets.QDoubleSpinBox()
        elif control == 'floatSlider':
            control = QtWidgets.QDoubleSpinBox()
        elif control == 'colorSlider':
            control = QtWidgets.QPushButton()


        if control and isinstance(control, dict):
            incrementButton.setVisible(False)
            randomButton.setVisible(False)
            setButton.setVisible(False)
            count = len(control)
            for key, value in control.iteritems():
                button = QtWidgets.QPushButton(key)
                button.setFixedSize(self.controlButtonWidth / count, buttonHeight)
                button.setProperty('attribute', attribute)
                button.setProperty('value', value)

                self.Signal.addSignal(button, 'clicked', self.controlSignalEvent)
                layout.addWidget(button)
        elif control == 'custom':
            if attribute == 'aiSssSetname' or attribute == 'aiAov':
                incrementButton.setVisible(False)
                randomButton.setVisible(False)
                control = QtWidgets.QLineEdit()
                control.setFixedSize(self.controlButtonWidth/2, buttonHeight)
                setButton.setFixedSize(self.controlButtonWidth / 2, buttonHeight)
                setButton.setProperty('control', control)
                setButton.setProperty('attribute', attribute)
                self.Signal.addSignal(setButton, 'clicked', self.controlSignalEvent)
                layout.addWidget(control)
        elif attribute == 'color' or attribute == 'lightColor':
            incrementButton.setVisible(False)
            randomButton.setVisible(False)
            control.setFixedWidth(70)
            layout.addItem(QtWidgets.QSpacerItem(73, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum))
            layout.addWidget(control)
            layout.addItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
            control.setStyleSheet('QPushButton {background-color: white}')
            control.setProperty('red', 1)
            control.setProperty('green', 1)
            control.setProperty('blue', 1)
            self.Signal.addSignal(control, 'clicked', self.colorPickerEvent)
            self.Signal.addSignal(setButton, 'clicked', self.controlSignalEvent)
            setButton.setProperty('control', control)
            setButton.setProperty('attribute', attribute)

        elif control:
            if attribute == 'renderSmoothLevel':
                self._setupControlWidgetDefaults(control, default, precision=0, minV=0, maxV=7)
            elif attribute in ['aiSubdivIterations', 'aiSamples', 'aiColorTemperature', 'aiVolumeSamples', 'temperature', 'fixedSampleCount']:
                defaultValue = 1
                if attribute == 'aiColorTemperature' or attribute == 'temperature':
                    defaultValue = 6500
                self._setupControlWidgetDefaults(control, defaultValue, precision=0, minV=0)
            elif attribute in ['aiDispHeight', 'intensity', 'aiDiffuse', 'aiSpecular', 'aiSss', 'aiIndirect', 'aiVolume', 'aiSpread', 'diffuse', 'specular']:
                self._setupControlWidgetDefaults(control, 1)
            else:
                self._setupControlWidgetDefaults(control, default)

            self.Signal.addSignal(incrementButton, 'clicked', self.controlSignalEvent)
            self.Signal.addSignal(randomButton, 'clicked', self.controlSignalEvent)
            self.Signal.addSignal(setButton, 'clicked', self.controlSignalEvent)
            incrementButton.setProperty('attribute', attribute)
            randomButton.setProperty('attribute', attribute)
            setButton.setProperty('attribute', attribute)
            incrementButton.setProperty('control', control)
            setButton.setProperty('control', control)
            layout.addWidget(control)

        layout.addWidget(incrementButton)
        layout.addWidget(randomButton)
        layout.addWidget(setButton)
        return widget

    def _setupControlWidgetDefaults(self, control, default, precision=3, minV=-999999, maxV=999999):


        control.setFixedSize(70, 25)
        control.setMaximum(maxV)
        control.setMinimum(minV)
        if default is not None:
            control.setValue(default)
        if precision == 0:
            control.setSingleStep(1)
            control.setDecimals(precision)
        else:
            control.setSingleStep(0.01)
            control.setDecimals(precision)

    def controlSignalEvent(self, button, *args, **kwargs):
        # print button.text(), button.property('attribute'), button.property('value'), button.property('control')
        pass

    def objectControlEvent(self, button, *args, **kwargs):
        # print button.property('mode')
        pass

    def closeButtonEvent(self, *args, **kwargs):
        self.close()

    def colorPickerEvent(self, control, *args, **kwargs):
        color = QtWidgets.QColorDialog().getColor()
        control.setStyleSheet('QPushButton {background-color: rgb(%s, %s, %s)}' % (color.red(), color.green(), color.blue()))
        control.setProperty('red', color.redF())
        control.setProperty('green', color.greenF())
        control.setProperty('blue', color.blueF())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    win = AttributeControl(mainWindow)
    win.show()
    sys.exit(app.exec_())
