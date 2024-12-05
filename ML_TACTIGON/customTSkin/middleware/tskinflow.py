from multiprocessing import Process, Event
from multiprocessing.connection import _ConnectionBase
import csv
import time
import joblib
from math import sqrt 
from tensorflow.keras.models import load_model


model = load_model('model_movement.keras')



class TSkinFlow(Process):
    def __init__(self, sensor_rx: _ConnectionBase, csv_file='DATI.csv'):
        Process.__init__(self)
        self.sensor_rx = sensor_rx
        self.csv_file = csv_file

        # Crea e inizializza il file CSV con intestazioni
        with open(self.csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            #writer.writerow(['timestamp', 'accX', 'accY', 'accZ',"Label"])
            writer.writerow(['timestamp', 'accX', 'accY', 'accZ' ,'gyroX', 'gyroY', 'gyroZ','Label'])
            
    def create_label(self,x,y,z,gx,gy,gz):

        # ACCELERAZIONI

        threshold_direction = 5

        # direzione destra/sinistra
        if y > threshold_direction:
            dir_y = "avanti" # destra
        elif y < -(threshold_direction):
            dir_y = "indietro" # sinistra
        else:
            dir_y = "fermo" # fermo

        # direzione avanti/dietro
        if x > threshold_direction:
            dir_x = "sopra" # sopra
        elif x < -(threshold_direction):
            dir_x = "sotto" # sotto
        else:
            dir_x = "fermo" # fermo

        # direzione sopra/sotto
        if z > threshold_direction:
            dir_z = "destra" # avanti
        elif z < -(threshold_direction):
            dir_z = "sinistra" # indietro
        else:
            dir_z = "fermo" # fermo

        # ACCELERAZIONI ANGOLARI

        threshold_rotation = 1

        # accelerazione angolare destra/sinistra
        if gy > threshold_rotation:
            rot_y = "destra polso" # destra
        elif gy < -(threshold_rotation):
            rot_y = "sinistra polso" # sinistra
        else:
            rot_y = "fermo" # fermo

        # accelerazione angolare avanti/dietro
        if gx > threshold_rotation:
            rot_x = "sinistra braccio" # sopra
        elif gx < -(threshold_rotation):
            rot_x = "destra braccio" # sotto
        else:
            rot_x = "fermo" # fermo

        # accelerazione angolare sopra/sotto
        if gz > threshold_rotation:
            rot_z = "impenna" # avanti
        elif gz < -(threshold_rotation):
            rot_z = "picchiata" # indietro
        else:
            rot_z = "fermo" # fermo

        return [dir_x, dir_y, dir_z, rot_x, rot_y, rot_z]
    
    
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
                    label = []
                    
                    #pred real time sui dati del tactigon
                    lista_pred = []                    
                    data2 = data[:3]
                    
                    for acc in data2:
                        lista_pred.append(acc)
                        
                    lista_liste = []
                    lista_liste.append(lista_pred)
                    lista_pred.clear()
                    
                    if len(lista_liste) == 10:
                        scaler = joblib.load('scaler.soblib')
                        lista_liste = scaler.transform(lista_liste)
                        model.predict(lista_liste)
                        
                        lista_liste.clear()
                                     
                    
                    with open(self.csv_file, mode='a', newline='') as file:
                            label = self.create_label(accX,accY,accZ,gyroX,gyroY,gyroZ)
                            writer = csv.writer(file)
                            writer.writerow([time.time(), accX, accY, accZ, gyroX, gyroY, gyroZ, label])
                            print(label)
                    
                else:
                    print("Errore: dati ricevuti in un formato non previsto:", data)
                
                
                
                #sogliole
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
