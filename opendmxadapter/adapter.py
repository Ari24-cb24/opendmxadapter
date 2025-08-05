import sys
import time
import threading

import pyftdi.serialext
from serial import serialutil

from . import fixtures


class OpenDMXAdapter:
    def __init__(self, serialPort: str):
        self.isConnected = False

        try:
            self.serial = pyftdi.serialext.serial_for_url(serialPort, baudrate=250000, stopbits=2)
        except ValueError as e:
            print("Malformed serialPort url: " + serialPort)
            print(e)
            sys.exit(0)
        except serialutil.SerialException as e:
            print("Error: could not open Serial Port")
            print(e)
            sys.exit(0)

        self.isConnected = True
        self.dmxData = [bytes([0])] * 513
        self.dmxData[0] = bytes([0])
        self.displayThread = threading.Thread(target=self._displayUniverse)
        self.fixtures = []
        self.channelIndex = 0

    def addFixture(self, fixture: 'fixtures.basefixture.BaseFixture'):
        fixture.adapter = self
        self.channelIndex += fixture.initialize(self.channelIndex)

        if self.channelIndex > len(self.dmxData) - 1:
            raise RuntimeError("Channel index out of range")

        self.fixtures.append(fixture)

    def addFixtures(self, *fixtureList: 'fixtures.basefixture.BaseFixture'):
        for fixture in fixtureList:
            self.addFixture(fixture)

    def setChannel(self, channel, intensity):
        channel = max(0, min(512, channel))
        intensity = max(0, min(255, intensity))
        self.dmxData[channel+1] = bytes([intensity])

    def blackout(self):
        for i in range(1, 512, 1):
            self.dmxData[i] = bytes([0])

    def start(self):
        self.displayThread.start()

    def close(self):
        self.isConnected = False
        self.serial.close()
        self.displayThread.join()

    def _displayUniverse(self):
        while self.isConnected:
            self._render()
            time.sleep(8 / 1000.0)  # 40 Hz for Enttec Open DMX USB

    def _render(self):
        if not self.isConnected:
            return

        sdata = b''.join(self.dmxData)
        self.serial.send_break(duration=0.001)
        self.serial.write(sdata)


# Guide to install driver: https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/windows
if __name__ == '__main__':
    url = "ftdi://ftdi:232:BG00DND8/1"

    dmx = OpenDMXAdapter(url)
    dmx.start()

    dmx.setChannel(1, 200)
    dmx.setChannel(3, 100)

    print("Start fading...")

    for i in range(0, 255):
        print(f"\r{int((i / 255) * 100)}% done", end='')
        dmx.setChannel(4, i)
        time.sleep(0.01)

    print("\nFading done.")
    time.sleep(5)

    print("Blackout")
    dmx.blackout()

    time.sleep(1)
    dmx.close()

