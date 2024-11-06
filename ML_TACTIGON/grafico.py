import pandas as pd
import matplotlib.pyplot as plt

# Leggi i dati dal file CSV
data = pd.read_csv('sensor_data.csv')

# Creazione dei grafici
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Grafico Accelerazione
axs[0].plot(data['timestamp'], data['accX'], label='Acc X', color='r')
axs[0].plot(data['timestamp'], data['accY'], label='Acc Y', color='g')
axs[0].plot(data['timestamp'], data['accZ'], label='Acc Z', color='b')
axs[0].set_title("Accelerazione")
axs[0].set_ylabel("Acc (m/s^2)")
axs[0].legend()

# Grafico Giroscopio
axs[1].plot(data['timestamp'], data['gyroX'], label='Gyro X', color='r')
axs[1].plot(data['timestamp'], data['gyroY'], label='Gyro Y', color='g')
axs[1].plot(data['timestamp'], data['gyroZ'], label='Gyro Z', color='b')
axs[1].set_title("Giroscopio")
axs[1].set_ylabel("Velocità Angolare (rad/s)")
axs[1].set_xlabel("Timestamp")
axs[1].legend()

plt.tight_layout()
plt.show()
