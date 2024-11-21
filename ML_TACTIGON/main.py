from customTSkin import CustomTSkin, Hand, OneFingerGesture
import time
import pandas as pd
import matplotlib.pyplot as plt

#C0:83:41:39:21:57: TSKIN50
if __name__ ==  '__main__':
    with CustomTSkin("C0:83:41:39:21:57", Hand.RIGHT) as tskin:
        while True:
            if not tskin.connected:
                print("Connecting...")
                time.sleep(0.1)
                continue
            
            touch = tskin.touch

            '''if touch and touch.one_finger == OneFingerGesture.SINGLE_TAP:
                print("Inizio Ascolto")
                tskin.select_audio()
                time.sleep(3)
                tskin.select_sensors()
                print("Fine Ascolto")'''

            time.sleep(tskin.TICK)



