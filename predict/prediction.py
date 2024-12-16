import pickle
import sklearn

class KNNPredict:
    def __init__(self, model_path="./model/knnreg.pkl"):
        self.model_path = model_path
        self.model = None
        self.scaler = None

    def load_model_and_scaler(self):
        with open(self.model_path, "rb") as file:
            data = pickle.load(file)
            self.model = data["model"]
            self.scaler = data["scaler"]
# Load model from pickle file
# Evaluate model 
    def predict(self, data):
        #data = data.reshape(1, -1)
        scaled_data = self.scaler.transform(data)
        return float(self.model.predict(scaled_data))
        