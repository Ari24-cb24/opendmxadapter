from ..adapter import OpenDMXAdapter


class _AbstractFixture:
    adapter: OpenDMXAdapter

    def initialize(self, channelIndex: int):
        ...

    def setValue(self, index: int, value: int):
        ...


class BaseFixture(_AbstractFixture):
    def __init__(self,
                 channelCount: int,
                 rawChannel: int | None = None):
        self.rawChannel = rawChannel
        self.channelCount = channelCount
        self.autoCalculateChannel = self.rawChannel is None

    def initialize(self, channelIndex: int):
        if self.autoCalculateChannel:
            self.rawChannel = channelIndex

        # Black out everything
        for i in range(self.channelCount):
            self.setValue(i, 0)

        return self.channelCount

    def setValue(self, index: int, value: int):
        if not isinstance(index, int):
            raise TypeError('index must be an integer')

        if not isinstance(value, int):
            raise TypeError('value must be an int')

        if index < 0 or index >= self.channelCount:
            raise IndexError

        value = min(255, max(0, int(value)))
        self.adapter.setChannel(self.rawChannel + index, value)


class ColorFixture(_AbstractFixture):
    _redChannel: int | None = None
    _greenChannel: int | None = None
    _blueChannel: int | None = None
    _intensityChannel: int | None = None

    def _initializeColorChannels(self, redChannel: int, greenChannel: int, blueChannel: int, intensityChannel: int | None):
        self._redChannel = redChannel
        self._greenChannel = greenChannel
        self._blueChannel = blueChannel
        self._intensityChannel = intensityChannel

    def setRgb(self, r: int, g: int, b: int):
        self.setValue(self._redChannel, r)
        self.setValue(self._greenChannel, g)
        self.setValue(self._blueChannel, b)

    def setIntensity(self, intensity: int):
        self.setValue(self._intensityChannel, intensity)


class StroboFixture(_AbstractFixture):
    _stroboChannel: int | None = None

    def _initializeStroboChannels(self, stroboChannel):
        self._stroboChannel = stroboChannel

    def setStrobo(self, value: int):
        self.setValue(self._stroboChannel, value)


class MovingHeadFixture(_AbstractFixture):
    _panChannel: int | None = None
    _panFineChannel: int | None = None
    _tiltChannel: int | None = None
    _tiltFineChannel: int | None = None
    _movingSpeedChannel: int | None = None

    def _initializeMovingHeadChannels(self, panChannel: int, panFineChannel: int | None, tiltChannel: int, tiltFineChannel: int | None, movingSpeedChannel: int | None):
        self._panChannel = panChannel
        self._panFineChannel = panFineChannel
        self._tiltChannel = tiltChannel
        self._tiltFineChannel = tiltFineChannel
        self._movingSpeedChannel = movingSpeedChannel

    def setPan(self, value: int):
        self.setValue(self._panChannel, value)

    def setPanFine(self, value: int):
        self.setValue(self._panFineChannel, value)

    def setTilt(self, value: int):
        self.setValue(self._tiltChannel, value)

    def setTiltFine(self, value: int):
        self.setValue(self._tiltFineChannel, value)

    def setMovingSpeed(self, speed: int):
        self.setValue(self._movingSpeedChannel, speed)
