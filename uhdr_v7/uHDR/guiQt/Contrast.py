# uHDR: HDR image editing software
#   Copyright (C) 2022  remi cozot 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
# hdrCore project 2020-2022
# author: remi.cozot@univ-littoral.fr

# import
# ------------------------------------------------------------------------------------------
# Contrast.py
import numpy as np, copy
from typing_extensions import Self
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QLineEdit, QCheckBox, QWidget
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIntValidator

from guiQt.AdvanceSliderLine import AdvanceSliderLine
from guiQt.ChannelSelector import ChannelSelector

from core import colourData, colourSpace

class Contrast(QFrame):
    # Declaration of signals
    scalingChanged = pyqtSignal(float)
    offsetChanged = pyqtSignal(float)
    lightnessRangeChanged = pyqtSignal(tuple)
    activeContrastChanged = pyqtSignal(bool)

    loadJsonChanged: pyqtSignal = pyqtSignal(list)

    def __init__(self: Self) -> None:
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        # attributes
        self.active: bool = True

        ## lightness range
        self.LightnessRange: tuple[int, int] = (0, 200)

        ## contrast scaling
        self.scaling: float = 1.0

        ## contrast offset
        self.offset: float = 0.0

        ## layout
        self.topLayout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.topLayout)

        ### container constrast active
        self.containerContrastActive: QWidget = QWidget()
        self.containerContrastActiveLayout: QHBoxLayout = QHBoxLayout()
        self.containerContrastActive.setLayout(self.containerContrastActiveLayout)

        self.contrastLabel: QLabel = QLabel('contrast')

        self.checkBoxActive: QCheckBox = QCheckBox("active")
        self.checkBoxActive.setChecked(True)

        self.containerContrastActiveLayout.addWidget(self.contrastLabel)
        self.containerContrastActiveLayout.addStretch()
        self.containerContrastActiveLayout.addWidget(self.checkBoxActive)

        ## container scaling, offset
        self.containerScalingOffset: QFrame = QFrame()
        self.containerScalingOffset.setFrameShape(QFrame.Shape.StyledPanel)
        self.containerScalingOffsetLayout: QVBoxLayout = QVBoxLayout()
        self.containerScalingOffset.setLayout(self.containerScalingOffsetLayout)

        ### contrast scaling, offset
        self.scalingSlider: AdvanceSliderLine = AdvanceSliderLine('scaling', 0.0, (-100, 100), (-100.0, 100.0), 8, 100)
        self.offsetlider: AdvanceSliderLine = AdvanceSliderLine('offset', 0.0, (-100, 100), (-100.0, 100.0), 8, 100)

        self.containerScalingOffsetLayout.addWidget(self.scalingSlider)
        self.containerScalingOffsetLayout.addWidget(self.offsetlider)

        ### lightness
        lightnessBarLch: np.ndarray = colourData.buildLchcolourData((0, 200), (0, 0), (180, 180), (20, 720), width='L', height='c')
        lightnessBarRGB: np.ndarray = colourSpace.Lch_to_sRGB(lightnessBarLch, apply_cctf_encoding=True, clip=True)
        self.lightnessSelector: ChannelSelector = ChannelSelector('lightness', lightnessBarRGB, (0, 200), (0, 150))

        ### show selection
        self.showSelection: QCheckBox = QCheckBox("show selection")

        ### add widget to layout
        self.topLayout.addWidget(self.containerContrastActive)
        self.topLayout.addWidget(self.containerScalingOffset)
        self.topLayout.addWidget(self.lightnessSelector)

        ## calbacks
        self.scalingSlider.valueChanged.connect(self.onScalingChanged)
        self.offsetlider.valueChanged.connect(self.onOffsetChanged)
        self.lightnessSelector.valuesChanged.connect(self.CBlightnessselectionChanged)
        self.checkBoxActive.stateChanged.connect(self.onActiveContrastChanged)

        # self.loadJsonChanged.connect(self.changeValue)

    def changeValue(self, value: list):
        """
        Manage the activation/desactivation system of the element contrast 
        
        Args :
            value (list, Required)
        """
        self.scalingSlider.setValue(value[1]['contrast']['contrast'])

    def onScalingChanged(self, str: str, value: float):
        value = float(value)
        self.scaling = value
        self.scalingChanged.emit(value)

    def onOffsetChanged(self, str: str, value: float):
        value = float(value)
        self.offset = value
        self.offsetChanged.emit(value)

    def CBlightnessselectionChanged(self: Self) -> None:
        self.LightnessRange = self.lightnessSelector.getValues()
        self.lightnessRangeChanged.emit(self.LightnessRange)
        self.updateView()
    
    def onActiveContrastChanged(self: Self) -> None:
        """
        Manage the activation/desactivation system of the element contrast 
        """
        if self.active == True:
            self.active = False
        else:
            self.active = True
        
        self.scalingSlider.slider.setEnabled(self.active)
        self.activeContrastChanged.emit(self.active)

    def updateView(self: Self) -> None:
        pass
