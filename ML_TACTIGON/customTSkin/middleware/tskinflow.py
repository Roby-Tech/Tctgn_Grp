from multiprocessing import Process, Event
from multiprocessing.connection import _ConnectionBase
import csv
import time
import joblib
from math import sqrt 
import keyboard
import time
#from keras.models import load_model


#model = load_model('model_movement.keras')



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
            
    def create_label(self,x,y,z):

        # ACCELERAZIONI
        dir_x = 'fermo'
        dir_y = 'fermo'
        dir_z = 'fermo'
        
        threshold_direction = 6
        down_threshold_direction = 6
        
        z_threshold_direction = 3
        z_down_threshold_direction = 3

        # direzione destra/sinistra
        if y > threshold_direction:
            if y > (x and z):
                dir_y = "indietro" # destra
                
        elif y < -(down_threshold_direction):
            if y < (x and z):
                dir_y = "avanti" # sinistra
                
        elif -(down_threshold_direction) < y < threshold_direction:
            dir_y = "fermo" # fermo


        # direzione avanti/dietro
        if x > threshold_direction:
            if x > (y and z):
                dir_x = "sotto" # sopra
        elif x < -(down_threshold_direction):
            if x < (y and z):
                dir_x = "sopra" # sotto
        elif -(down_threshold_direction) < x < threshold_direction:
            dir_x = "fermo" # fermo
                

        # direzione sopra/sotto
        if z > z_threshold_direction:
            if z > (x and y):
                dir_z = "sinistra" # avanti
        elif z < -(z_down_threshold_direction):
            if z < (x and y):
                dir_z = "destra" # indietro
        elif -(z_down_threshold_direction) < z < z_threshold_direction:
            dir_z = "fermo" # fermo
            

        return [dir_x, dir_y, dir_z]
    
    
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
                    
                    '''#pred real time sui dati del tactigon
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
                        pred = model.predict(lista_liste)
                        
                        soglia_corretto = 0.5
                        predicted_labels = (pred > soglia_corretto)
                        print(predicted_labels)
                        
                        lista_liste.clear()'''
                                     
                    
                    with open(self.csv_file, mode='a', newline='') as file:
                         if keyboard.is_pressed('p'):
                            while keyboard.is_pressed('p'):  # Aspetta che il pulsante venga rilasciato
                                time.sleep(0.1)
                                print('stopp')
                                
                         else:            
                            label = self.create_label(accX,accY,accZ)
                            writer = csv.writer(file)
                            writer.writerow([time.time(), accX, accY, accZ, label])
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
                
                '''#Movimento X
                if accX <= -9:
                    if accX < (accY and accZ):
                        print('Sopra')
                        print(f'accX: {accX}')
                elif accX >= 9:
                    if accX > (accY and accZ):
                        print('Sotto')
                        print(f'accX: {accX}')
                
             #Movimento Y
                if accY <= -9:
                    if accY < (accX and accZ):
                        print('avanti')
                        print(f'accY: {accY}')
                elif accY >= 9:
                    if accY > (accX and accZ):
                        print('indietro')
                        print(f'accY: {accY}')

                #Movimento Z
                if accZ <= -5:
                    if accZ < (accX and accY):
                        print('destra')
                        print(f'accZ: {accZ}')
                elif accZ >= 5:
                    if accZ > (accX and accY):
                        print('sinistra')
                        print(f'accZ: {accZ}')
                
'''