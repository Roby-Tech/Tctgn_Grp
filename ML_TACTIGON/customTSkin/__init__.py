from numpy import add
from typing import Optional
from multiprocessing import Pipe
from tactigon_gear import Ble, Hand, OneFingerGesture
from .middleware import TSkinFlow, TSkinAudio

class CustomTSkin(Ble):
    tskinflow: TSkinFlow
    tskinaudio: TSkinAudio

    def __init__(self, address: str, hand: Hand):
        Ble.__init__(self, address, hand)
        sensor_rx, self._sensor_tx = Pipe(duplex=False)
        audio_rx, self._audio_tx = Pipe(duplex=False)

        self.tskinflow = TSkinFlow(sensor_rx)
        self.tskinaudio = TSkinAudio(audio_rx)

    def start(self):
        self.tskinflow.start()
        self.tskinaudio.start()
        Ble.start(self)

    def join(self, timeout: Optional[float] = None):
        Ble.join(self, timeout)
        self.tskinflow.terminate()
        self.tskinaudio.terminate()
        
    