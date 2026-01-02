import pickle
import numpy as np

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

def predict(features):
    x = np.array([features])
    return model.predict(x)[0]
