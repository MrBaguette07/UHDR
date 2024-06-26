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

# LightBlock.py
from typing_extensions import Self
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtGui import QDoubleValidator, QIntValidator 
from PyQt6.QtCore import Qt, pyqtSignal, QLocale

from guiQt.AdvanceSlider import AdvanceSlider
from guiQt.Contrast import Contrast
from guiQt.CurveWidget import CurveWidget
from guiQt.MemoGroup import MemoGroup

# ------------------------------------------------------------------------------------------
# --- class LightBlock (QFrame) ------------------------------------------------------
# ------------------------------------------------------------------------------------------
class LightBlock(QFrame):
    # class attributes
    ## signal
    exposureChanged = pyqtSignal(float)
    contrastChanged = pyqtSignal(float)
    highlightsChanged = pyqtSignal(float)
    shadowsChanged = pyqtSignal(float)
    whitesChanged = pyqtSignal(float)
    blacksChanged = pyqtSignal(float)
    mediumsChanged = pyqtSignal(float)
    activeContrastChanged = pyqtSignal(bool)
    activeExposureChanged = pyqtSignal(bool)
    activeLightnessChanged = pyqtSignal(bool)
    # autoClickedExposure: pyqtSignal = pyqtSignal(bool)

    # constructor
    def __init__(self : Self) -> None:
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)

        # attributes
        self.active : bool = True

        # layout and widgets
        self.topLayout : QVBoxLayout = QVBoxLayout()
        self.setLayout(self.topLayout)

        self.exposure : AdvanceSlider = AdvanceSlider('exposure', 0.0, (-30, +30), (-3.0, +3.0), 10)
        self.contrast : Contrast = Contrast()
        self.curve : CurveWidget = CurveWidget()

        ## add to layout
        self.topLayout.addWidget(self.exposure)
        self.topLayout.addWidget(self.contrast)
        self.topLayout.addWidget(self.curve)

        # Connect signals
        self.curve.highlightsChanged.connect(self.onHighlightsChanged)
        self.curve.shadowsChanged.connect(self.onShadowsChanged)
        self.curve.whitesChanged.connect(self.onWhitesChanged)
        self.curve.blacksChanged.connect(self.onBlacksChanged)
        self.curve.mediumsChanged.connect(self.onMediumsChanged)

        self.curve.activeLightnessChanged.connect(self.onActiveLightnessChanged)

        # self.contrast.activeContrastChanged.connect(self.onActiveContrastChanged)
        self.exposure.activeToggled.connect(self.onActiveExposureChanged)
        # self.exposure.autoClicked.connect(self.autoClickedExposure)
        # self.loadJsonChanged.connect(self.changeValue)

    def onActiveExposureChanged(self: Self, value) -> None:
        """
        Returns the Exposure signal when a button/slider is activated/deactivated
        """
        self.exposure.active = value
        
        self.exposure.auto.setEnabled(self.exposure.active)
        self.exposure.reset.setEnabled(self.exposure.active)
        self.exposure.editValue.setEnabled(self.exposure.active)
        self.exposure.slider.setEnabled(self.exposure.active)
        self.activeExposureChanged.emit(self.exposure.active)
        

    def onExposureChanged(self, value: float):
        """
        Return the signal received from Exposure

        Args
            value (float, Required)
        """
        self.exposureChanged.emit(value)

    def onContrastChanged(self, value: float):
        """
        Return the signal received from Contrast
        """
        self.contrastChanged.emit(value)

    # def onActiveContrastChanged(self, value: bool):
    #     self.contrastChanged.emit(value)

    def onActiveLightnessChanged(self, value: bool):
        """
        Return the signal received from curve

        Args :
            value (bool, Required)
        """
        self.activeLightnessChanged.emit(value)

    def onHighlightsChanged(self, value: float):
        """
        Return the signal received from curve

        Args :
            value (float, Required)
        """
        self.highlightsChanged.emit(value)

    def onShadowsChanged(self, value: float):
        """
        Return the signal received from curve

        Args :
            value (float, Required)
        """
        self.shadowsChanged.emit(value)

    def onWhitesChanged(self, value: float):
        """
        Return the signal received from curve

        Args :
            value (float, Required)
        """
        self.whitesChanged.emit(value)

    def onBlacksChanged(self, value: float):
        """
        Return the signal received from curve

        Args :
            value (float, Required)
        """
        self.blacksChanged.emit(value)

    def onMediumsChanged(self, value: float):
        """
        Return the signal received from curve

        Args
            value (float, Required)
        """
        self.mediumsChanged.emit(value)
        

# ------------------------------------------------------------------------------------------


