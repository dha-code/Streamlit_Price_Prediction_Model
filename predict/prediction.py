import pickle
import pandas as pd

class KNNPredict:
    def __init__(self, model_path="./model/knnreg.pkl"):
        self.model_path = model_path
        self.model = None
        self.scaler = None

    def load_model_and_scaler(self):
        """"
        Function to load the model and scaler form pickle file
        """
        with open(self.model_path, "rb") as file:
            data = pickle.load(file)
            self.model = data["model"]
            self.scaler = data["scaler"]

    def predict(self, data):
        """
        Function to predict the price of a new property
        """
        #data = data.reshape(1, -1)
        scaled_data = self.scaler.transform(data)
        return float(self.model.predict(scaled_data))
    
    def get_neighbours(self, data):
        """
        Function to get the neighbours from the zipcode of the new property 
        """
        distances, indices = self.model.kneighbors(data)
        training_data = pd.read_csv("./model/training_data.csv")
        neighbors = training_data.iloc[indices[0]]
        neighbor_coords = neighbors[["Latitude", "Longitude"]].values.tolist()
        neighbor_prices = neighbors["Region"].tolist()
        return neighbor_coords, neighbor_prices
        