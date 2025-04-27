import os
from tensorflow.keras.models import load_model

model_path = os.path.join("models", "face-latest.hdf5")
model = load_model(model_path)
# model.summary()

def predict(img_array) -> (float, str):
    pred = model.predict(img_array)[0][0]
    label = "Live" if pred > 0.5 else "Spoof"
    return float(pred), label


