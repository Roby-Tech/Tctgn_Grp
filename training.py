import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import tesorflow as tf

# Configura l'ambiente per utilizzare la GPU se disponibile
if tf.config.list_physical_devices('GPU'):
    for gpu in tf.config.list_physical_devices('GPU'):
        tf.config.experimental.set_memory_growth(gpu, True)
    print("GPU configurata correttamente per la crescita dinamica della memoria.")
else:
    print("GPU non disponibile. Si utilizzerà la CPU.")

# Caricamento dati
data = pd.read_csv('DATI_With_Out_Rotation_Label.csv')

# Preprocessing dei dati sensoriali
scaler = StandardScaler()
data[['accX', 'accY', 'accZ', 'gyroX', 'gyroY', 'gyroZ']] = scaler.fit_transform(
    data[['accX', 'accY', 'accZ', 'gyroX', 'gyroY', 'gyroZ']]
)

# Preprocessing delle etichette
labels = data['Label'].apply(eval)  # Converti stringhe in liste
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(labels)

# Creazione delle sequenze
sequence_length = 50
X, y_sequences = [], []

for i in range(len(data) - sequence_length + 1):
    X.append(data[['accX', 'accY', 'accZ', 'gyroX', 'gyroY', 'gyroZ']].iloc[i:i + sequence_length].values)
    y_sequences.append(y[i + sequence_length - 1])  # L'output corrisponde all'ultima riga della sequenza

X = np.array(X)
y_sequences = np.array(y_sequences)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y_sequences, test_size=0.2, random_state=42)

# Definizione del modello
model = Sequential([
    LSTM(128, input_shape=(sequence_length, 6), return_sequences=True),
    Dropout(0.2),
    LSTM(64),
    Dropout(0.2),
    Dense(y_sequences.shape[1], activation='sigmoid')  # Sigmoid per multi-label
])

# Compilazione del modello
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Allenamento
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.2)

# Valutazione
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Loss: {loss}, Accuracy: {accuracy}")

model.save('model_tskin.keras')