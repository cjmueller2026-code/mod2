"""
Diabetes Prediction Model
Dataset: Pima Indians Diabetes Database (OpenML ID 43483 / UCI)
Author: [Student Name]
Course: [Course Name]

Steps implemented (per assignment requirements):
    1. Load Data
    2. Define the Model
    3. Compile the Model
    4. Fit the Model
    5. Evaluate the Model
    6. Make Predictions
"""

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # suppress verbose TensorFlow/CUDA logging

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input

# Reproducibility
np.random.seed(7)
tf.random.set_seed(7)

# ----------------------------------------------------------------------
# STEP 1: LOAD DATA
# ----------------------------------------------------------------------
column_names = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"
]

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "pima-indians-diabetes.csv")
dataframe = pd.read_csv(csv_path, names=column_names)

print("=" * 70)
print("STEP 1: LOAD DATA")
print("=" * 70)
print(f"Dataset shape: {dataframe.shape}")
print("\nFirst 5 rows:")
print(dataframe.head())
print("\nSummary statistics:")
print(dataframe.describe())
print(f"\nClass balance (Outcome):\n{dataframe['Outcome'].value_counts()}")

# Split into input (X) and output (y) variables
X = dataframe.drop("Outcome", axis=1).values
y = dataframe["Outcome"].values

# Train/test split (80/20) so the model is evaluated on unseen data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=7, stratify=y
)

# Feature scaling improves convergence for neural networks
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print(f"\nTraining samples: {X_train.shape[0]}, Test samples: {X_test.shape[0]}")

# ----------------------------------------------------------------------
# STEP 2: DEFINE THE MODEL
# ----------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 2: DEFINE THE MODEL")
print("=" * 70)

model = Sequential()
model.add(Input(shape=(8,)))
model.add(Dense(12, activation="relu"))
model.add(Dense(8, activation="relu"))
model.add(Dense(1, activation="sigmoid"))

model.summary()

# ----------------------------------------------------------------------
# STEP 3: COMPILE THE MODEL
# ----------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 3: COMPILE THE MODEL")
print("=" * 70)

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
print("Model compiled with binary_crossentropy loss, adam optimizer, accuracy metric.")

# ----------------------------------------------------------------------
# STEP 4: FIT THE MODEL
# ----------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 4: FIT THE MODEL")
print("=" * 70)

history = model.fit(
    X_train, y_train,
    epochs=150,
    batch_size=10,
    validation_split=0.1,
    verbose=0
)

print("Training complete.")
print(f"Final training accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")

# ----------------------------------------------------------------------
# STEP 5: EVALUATE THE MODEL
# ----------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 5: EVALUATE THE MODEL")
print("=" * 70)

loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Loss: {loss:.4f}")
print(f"Test Accuracy: {accuracy * 100:.2f}%")

# ----------------------------------------------------------------------
# STEP 6: MAKE PREDICTIONS
# ----------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 6: MAKE PREDICTIONS")
print("=" * 70)

predictions_prob = model.predict(X_test, verbose=0)
predictions = (predictions_prob > 0.5).astype(int).flatten()

print("Sample predictions (first 15 test records):")
print(f"{'Predicted':<12}{'Actual':<10}{'Probability'}")
for i in range(15):
    print(f"{predictions[i]:<12}{y_test[i]:<10}{predictions_prob[i][0]:.4f}")

correct = np.sum(predictions == y_test)
print(f"\nCorrect predictions on test set: {correct}/{len(y_test)}")

# Save model for reproducibility / portfolio evidence
model.save("diabetes_model.keras")
print("\nModel saved as diabetes_model.keras")
