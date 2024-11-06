import wave
from multiprocessing import Process
from multiprocessing.connection import _ConnectionBase

class TSkinAudio(Process):
    audio_rx: _ConnectionBase
    def __init__(self, audio_rx: _ConnectionBase):
        Process.__init__(self)

        self.audio_rx = audio_rx

def run(self):
    while True:
        if self.audio_rx.poll():
            with wave.open("test.wav", "wb") as audio_file:
                audio_file.setnchannels(1)
                audio_file.setsampwidth(2)
                audio_file.setframerate(16000)

                while self.audio_rx.poll(0.5):
                     audio_bytes = self.audio_rx.recv_bytes()
                     audio_file.writeframes(audio_bytes)
                     
            audio = self.audio_rx.recv_bytes()
            print(audio)