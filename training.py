import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Funzione per caricare e preprocessare i dati
def load_and_preprocess_data(files, labels):
    sequences, targets = [], []
    for file, label in zip(files, labels):
        data = pd.read_csv(file)
        scaler = StandardScaler()
        data[['accX', 'accY', 'accZ', 'gyroX', 'gyroY', 'gyroZ']] = scaler.fit_transform(data[['accX', 'accY', 'accZ', 'gyroX', 'gyroY', 'gyroZ']])
        for i in range(len(data) - sequence_length + 1):
            sequences.append(data[['accX', 'accY', 'accZ', 'gyroX', 'gyroY', 'gyroZ']].iloc[i: i + sequence_length].values)
            targets.append(label)
    return np.array(sequences), np.array(targets)

# Parametri
sequence_length = 50
files = ['ML_TACTIGON/customTSkin/data/fermo.csv',
         'ML_TACTIGON/customTSkin/data/destra.csv',
         'ML_TACTIGON/customTSkin/data/sinistra.csv',
         'ML_TACTIGON/customTSkin/data/sopra.csv',
         'ML_TACTIGON/customTSkin/data/sotto.csv',
         'ML_TACTIGON/customTSkin/data/avanti.csv',
         'ML_TACTIGON/customTSkin/data/indietro.csv']

labels = ['fermo', 'destra', 'sinistra', 'sopra', 'sotto', 'avanti', 'indietro']  # Etichette per ciascun file

# Caricamento e suddivisione dei dati
X, y = load_and_preprocess_data(files, labels)
y = to_categorical(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creazione del modello LSTM
model = Sequential()
model.add(LSTM(64, input_shape=(sequence_length, 6), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(32))
model.add(Dropout(0.2))
model.add(Dense(7, activation='softmax'))

# Compilazione del modello
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Allenamento
model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split=0.2)

# Valutazione
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Loss: {loss}, Accuracy: {accuracy}")

