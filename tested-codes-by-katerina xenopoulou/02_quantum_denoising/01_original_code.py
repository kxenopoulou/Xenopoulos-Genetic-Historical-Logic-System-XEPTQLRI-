import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout, Rescaling
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt

# 1. Δημιουργία Ρεαλιστικών Δεδομένων
def generate_quantum_data(num_samples, timesteps=20, noise_level=0.5):
    """Δημιουργία δεδομένων με ελέγξιμο θόρυβο"""
    # Καθαρές καταστάσεις (κανονικοποιημένες)
    clean_states = np.random.randn(num_samples, timesteps, 3) + 1j * np.random.randn(num_samples, timesteps, 3)
    clean_states = clean_states / np.linalg.norm(clean_states, axis=-1, keepdims=True)
    
    # Πρόσθεση θορύβου με φυσιολογική κλίμακα
    noise_real = np.random.normal(0, noise_level, clean_states.shape)
    noise_imag = np.random.normal(0, noise_level, clean_states.shape)
    noisy_states = clean_states + (noise_real + 1j * noise_imag)
    
    # Μετατροπή σε πραγματικές/φανταστικές συνιστώσες
    noisy_states = np.float32(np.concatenate([noisy_states.real, noisy_states.imag], axis=-1))
    clean_states = np.float32(np.concatenate([clean_states.real, clean_states.imag], axis=-1))
    
    return noisy_states, clean_states

# 2. Βελτιωμένο Μοντέλο
def build_denoising_model(timesteps=20, input_dim=6):
    input_layer = Input(shape=(timesteps, input_dim))
    
    # Προ-επεξεργασία
    x = Rescaling(1./255)(input_layer)  # Κλιμάκωση τιμών
    
    # Αρχιτεκτονική
    x = LSTM(128, return_sequences=True, activation='tanh')(x)
    x = Dropout(0.3)(x)
    x = LSTM(64, return_sequences=True)(x)
    x = Dense(32, activation='relu')(x)
    
    output = Dense(input_dim, activation='linear')(x)
    
    model = Model(inputs=input_layer, outputs=output)
    return model

# 3. Αξιολόγηση Βάσης
def calculate_baseline(noisy_data, clean_data):
    mae = np.mean(np.abs(noisy_data - clean_data))
    print(f'Baseline MAE (χωρίς μοντέλο): {mae:.4f}')

# 4. Εκπαίδευση και Αξιολόγηση
if __name__ == "__main__":
    # Παράμετροι
    num_samples = 5000
    timesteps = 20
    noise_level = 0.5  # Ρεαλιστικός θόρυβος
    
    # Δεδομένα
    X, y = generate_quantum_data(num_samples, timesteps, noise_level)
    calculate_baseline(X, y)
    
    # Split δεδομένων
    split = int(0.8 * num_samples)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    # Μοντέλο
    model = build_denoising_model()
    model.compile(optimizer=Adam(learning_rate=0.001, clipnorm=1.0),
                  loss='mse',
                  metrics=['mae'])
    
    # Εκπαίδευση
    history = model.fit(X_train, y_train,
                        epochs=100,
                        batch_size=64,
                        validation_split=0.2,
                        callbacks=[EarlyStopping(patience=5, restore_best_weights=True)],
                        verbose=1)
    
    # Αξιολόγηση
    test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
    print(f'\nTest MAE: {test_mae:.4f} (Βελτίωση {np.mean(np.abs(X_test - y_test)) - test_mae:.4f})')
    
    # Οπτικοποίηση
    plt.figure(figsize=(12,5))
    
    # Ιστορικό εκπαίδευσης
    plt.subplot(1,2,1)
    plt.plot(history.history['mae'], label='Training MAE')
    plt.plot(history.history['val_mae'], label='Validation MAE')
    plt.title('Μέση Απόλυτη Τιμή')
    plt.legend()
    
    # Δείγμα προβλέψεων
    plt.subplot(1,2,2)
    sample = X_test[0:1]
    prediction = model.predict(sample, verbose=0)
    
    plt.plot(y_test[0,:,0], label='Πραγματική Κατάσταση')
    plt.plot(sample[0,:,0], '--', label='Θορυβώδης Κατάσταση')
    plt.plot(prediction[0,:,0], label='Πρόβλεψη')
    plt.title('Σύγκριση Προβλέψεων')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
