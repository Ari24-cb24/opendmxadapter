from ..basefixture import BaseFixture, ColorFixture, StroboFixture


class RootPar6(BaseFixture, ColorFixture, StroboFixture):
    def __init__(self, rawChannel: int | None = None):
        """
        8ch mode
        0 - dimmer
        1 - strobe
        2 - red
        3 - green
        4 - blue
        5 - white
        6 - amber
        7 - uv
        """
        super().__init__(8, rawChannel)
        self._initializeColorChannels(2, 3, 4, 0)
        self._initializeStroboChannels(1)

    def setWhite(self, value: int):
        self.setValue(5, value)

    def setAmber(self, value: int):
        self.setValue(6, value)

    def setUV(self, value: int):
        self.setValue(7, value)
