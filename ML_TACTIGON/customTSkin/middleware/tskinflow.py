from multiprocessing import Process, Event
from multiprocessing.connection import _ConnectionBase
import csv
import time

class TSkinFlow(Process):
    def __init__(self, sensor_rx: _ConnectionBase, csv_file='sensor_data.csv'):
        Process.__init__(self)
        self.sensor_rx = sensor_rx
        self.csv_file = csv_file

        # Crea e inizializza il file CSV con intestazioni
        with open(self.csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'accX', 'accY', 'accZ', 'gyroX', 'gyroY', 'gyroZ'])

    def run(self):
        while True:
            if self.sensor_rx.poll(1):  # Attendi fino a 1 secondo per ricevere dati
                data = self.sensor_rx.recv()
                print(data)  # Diagnostica: stampa i dati ricevuti

                # Verifica che `data` sia una lista della lunghezza corretta
                if isinstance(data, list) and len(data) >= 6:
                    # Estrai i valori di accelerazione e giroscopio dalla lista
                    accX, accY, accZ = data[0], data[1], data[2]
                    gyroX, gyroY, gyroZ = data[3], data[4], data[5]
                    
                    # Aggiungi una riga al CSV con i dati e un timestamp
                    with open(self.csv_file, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([time.time(), accX, accY, accZ, gyroX, gyroY, gyroZ])
                else:
                    print("Errore: dati ricevuti in un formato non previsto:", data)


