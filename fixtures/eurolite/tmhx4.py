import time

from opendmxadapter.fixtures.basefixture import BaseFixture, ColorFixture, MovingHeadFixture, StroboFixture


class TMHX4(BaseFixture, ColorFixture, MovingHeadFixture, StroboFixture):
    def __init__(self, rawChannel: int | None = None):
        """
        16ch mode
        ...

        24ch mode
        0 - Pan Clockwise
        1 - Pan fine
        2 - Tilt
        3 - Tilt fine
        4 - Moving Speed (1-212: less speed, 213-255: nothing)
        5 - Lens Zoom
        6 - Intensity
        7 - Strobo (0-3: None, 4-95: normal, 96-176: random, 177-255: "thunder"-strobe)

        8 - Red     Inner
        9 - Green   Inner
        10 - Blue   Inner
        11 - White  Inner

        12 - Red    Outer (Top-Start)
        13 - Green  Outer (Top-Start)
        14 - Blue   Outer (Top-Start)
        15 - White  Outer (Top-Start)

        16 - Red    Outer (Non-Top-Start)
        17 - Green  Outer (Non-Top-Start)
        18 - Blue   Outer (Non-Top-Start)
        19 - White  Outer (Non-Top-Start)

        20 - Color Preset and Macro
        21 - Macro Speed
        22 - Pattern (0-49: Channel 1-20, 50-99: Presets/Macros, 100-149: Internal P1, 150-199: Internal P2, 200-255: Music)
        23 - Reset (251-255)
        """
        super().__init__(24, rawChannel)
        self._initializeColorChannels(8, 9, 10, 6)
        self._initializeMovingHeadChannels(0, 1, 2, 3, 4)
        self._initializeStroboChannels(7)

    def setOuterColor(self, r: int, g: int, b: int, w: int, topStart: bool = True):
        self.setValue(12 + 4 if topStart else 0, r)
        self.setValue(13 + 4 if topStart else 0, g)
        self.setValue(14 + 4 if topStart else 0, b)
        self.setValue(15 + 4 if topStart else 0, b)

    def setLensZoom(self, value: int):
        self.setValue(5, value)

    def setPattern(self, value: int):
        self.setValue(22, value)

    def setReset(self, shouldReset: bool):
        self.setValue(23, 255 if shouldReset else 0)

    def setColorMacro(self, value: int):
        self.setValue(20, value)

    def setMacroSpeed(self, value: int):
        self.setValue(21, value)
