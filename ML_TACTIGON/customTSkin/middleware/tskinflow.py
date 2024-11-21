from multiprocessing import Process, Event
from multiprocessing.connection import _ConnectionBase
import csv
import time
import math 
from math import sqrt 

def create_label(x,y,z):

        # direzione destra/sinistra
        threshold_direction = 9
        if y > threshold_direction:
            dir_y = "destra" # destra
        elif y < -(threshold_direction):
            dir_y = "sinistra" # sinistra
        else:
            dir_y = "acc. nulla" # fermo

        # direzione avanti/dietro
        if x > threshold_direction:
            dir_x = "sopra" # sopra
        elif x < -(threshold_direction):
            dir_x = "sotto" # sotto
        else:
            dir_x = "acc. nulla" # fermo

        # direzione sopra/sotto
        if z > threshold_direction:
            dir_z = "avanti" # avanti
        elif z < -(threshold_direction):
            dir_z = "indietro" # indietro
        else:
            dir_z = "acc. nulla" # fermo

        return [dir_x, dir_y, dir_z]

class TSkinFlow(Process):
    def __init__(self, sensor_rx: _ConnectionBase, csv_file='prova.csv'):
        Process.__init__(self)
        self.sensor_rx = sensor_rx
        self.csv_file = csv_file

        # Crea e inizializza il file CSV con intestazioni
        with open(self.csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'accX', 'accY', 'accZ',"Label"])
            #writer.writerow(['timestamp', 'accX', 'accY', 'accZ' ,'gyroX', 'gyroY', 'gyroZ'])

    def run(self):
        while True:
            if self.sensor_rx.poll(1):  # Attendi fino a 1 secondo per ricevere dati
                data = self.sensor_rx.recv()
                # Diagnostica: stampa i dati ricevuti


                # Verifica che `data` sia una lista della lunghezza corretta
                if isinstance(data, list) and len(data) >= 6:
                    # Estrai i valori di accelerazione e giroscopio dalla lista
                    accX, accY, accZ = data[0], data[1], data[2]
                    accZ = accZ + 0.81
                    accTOT = sqrt(accX**2 + accY**2 + accZ**2)-9.81
                    gyroX, gyroY, gyroZ = data[3], data[4], data[5]
                    gyroTOT = sqrt(gyroX**2 + gyroY**2 + gyroZ**2)
                    
                    with open(self.csv_file, label, mode='a', newline='') as file:
                            label = create_label(accX,accY,accZ)
                            writer = csv.writer(file)
                            writer.writerow([time.time(), accX, accY, accZ. label])
                    
                    """#Movimento X
                    if accX <= -9:
                        # Aggiungi una riga al CSV con i dati e un timestamp
                        with open(self.csv_file, label, mode='a', newline='') as file:
                            label = create_label(accX,accY,accZ)
                            writer = csv.writer(file)
                            writer.writerow([time.time(), accX, accY, accZ. label])
                        #writer.writerow([time.time(), accX, accY, accZ, gyroX, gyroY, gyroZ])
                            print('Sinistra')
                            print(f'accX: {accX}')
                    elif accX >= 9:
                        with open(self.csv_file, mode='a', newline='') as file:
                            label = create_label(accX,accY,accZ)
                            writer = csv.writer(file)
                            writer.writerow([time.time(), accX, accY, accZ])
                            print('Destra')
                            print(f'accX: {accX}')"""
                    
                else:
                    print("Errore: dati ricevuti in un formato non previsto:", data)
                
                #print(f"Accelerazione: X={accX}, Y={accY}, Z={accZ}")

                '''if accTOT < 2:
                    print('Fermo')
                else:
                    print('Movimento rilevato')
                    #print(accTOT)
                    #print(data)
                if gyroTOT < 1:
                    print('Rotazione ferma')
                else:
                    print('Rotazione in corso')'''
                
                #Movimento X
                '''if accX <= -9:
                    if accX < (accY and accZ):
                        print('Sopra')
                        print(f'accX: {accX}')
                elif accX >= 9:
                    if accX > (accY and accZ):
                        print('Sotto')
                        print(f'accX: {accX}')
                
            """ #Movimento Y
                if accY <= -9:
                    if accY < (accX and accZ):
                        print('Sinistra')
                        print(f'accY: {accY}')
                elif accY >= 9:
                    if accY > (accX and accZ):
                        print('Destra')
                        print(f'accY: {accY}')

                #Movimento Z
                if accZ <= -5:
                    if accZ < (accX and accY):
                        print('Indietro')
                        print(f'accZ: {accZ}')
                elif accZ >= 5:
                    if accZ > (accX and accY):
                        print('Avanti')
                        print(f'accZ: {accZ}')
                '''
