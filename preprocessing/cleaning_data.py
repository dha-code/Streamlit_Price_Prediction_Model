import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self):
        self.property_type = None
        self.subtype = None
        self.land_surface = None
        self.living_area = None
        self.building_state = None
        self.year = None
        self.age = None
        self.bedrooms = None
        self.bathrooms = None
        self.epc = None
        self.terrace_area = None
        self.facades = None
        self.zipcode = None
        self.latitude = None
        self.longitude = None
        self.income = None
        self.popdensity = None
        self.tax = None
        self.region = None

    def preprocess(self):
        self.property_type = self.categorise_property()
        self.subtype = self.categorise_subproperty(self.subtype)
        self.building_state = self.replace_build_state(self.building_state)
        self.epc = self.replace_epc(self.epc)
        self.age = self.set_age()        
        self.region = self.get_region(self.zipcode)
        self.read_zip_info()
        #self.quality_check()
        npdata = self.to_numpy()
        column_header = ["Property type","Subtype","Age","Living area","Bedrooms","Bathrooms",
                     "Terrace Area","EPC score","Land surface","Taxes", "Population Density",
                     "Facades","Building state","Region","Latitude","Longitude","Income"]
        data = pd.DataFrame([npdata], columns=column_header)
        #print(data)
        return data 
    
    def to_numpy(self):
        return np.array((self.property_type,self.subtype,self.age,self.living_area,
                         self.bedrooms,self.bathrooms,self.terrace_area,
                         self.epc,self.land_surface,self.tax,self.popdensity,
                         self.facades,self.building_state,self.region,
                         self.latitude,self.longitude,self.income))

    def set_age(self):
        if self.year <= 2024:
            return 2024-int(self.year)
        return 0
    
    def categorise_property(self):
        if self.property_type == 'House':
            return 1
        return 0

    def quality_check(self):
        print(self)
        
    def replace_epc(self, x):
        """
        Function to replace EPC score (string) to numerical value
        """
        if x == 'A++/A+/A':
            return 1
        elif x == 'B/C':
            return 2
        elif x == 'D/E':
            return 3
        elif x == 'F/G':
            return 5
        else:
            return 2.5
    
    def replace_build_state(self, x):
        """
        Function to replace Building state (string) to numerical value
        """
        if x == 'Good':
            return 1
        elif x == 'As new/Just renovated':
            return 2
        elif x == 'To renovate/To restore':
            return 0
        else:
            return 0.75

    def categorise_subproperty(self, property_type):
        """
        Function to replace Property type (string) to numerical value
        """
        house = ["House/Town house","Bungalow/Loft/Chalet"]
        apartment = ["Apartment/Penthouse","Ground floor/Duplex/Triplex"]
        small = ["Flat studio/Service flat/Kot"]
        
        if property_type in house:
            return 2
        elif property_type in apartment:
            return 1
        elif property_type in small:
            return 0
        else:
            return 4
        
    def get_region(self, x):
        """
        Function to add a column Region based on zip code
        """
        x = int(x)
        if x >=1000 and x <=1200:
            return 1
        elif (x >=1500 and x<=3999) or (x >= 8000 and x <= 9999):
            return 2
        else:
            return 3
    
    def add_external_data(self, extracted_data):
        self.popdensity = int(extracted_data.iloc[0,1])
        self.tax = float(extracted_data.iloc[0,2])
        self.income = float(extracted_data.iloc[0,3])
        self.longitude = float(extracted_data.iloc[0,4])
        self.latitude = float(extracted_data.iloc[0,5])

    def read_zip_info(self):
        zipinfo =  pd.read_csv('./data/Zipcode_info.txt', sep="\t")
        extracted_data = zipinfo[zipinfo["Locality"] == self.zipcode]
        if int(extracted_data.shape[0]) == 1:
            self.add_external_data(extracted_data)
        else:
            extracted_data = zipinfo[zipinfo["Locality"] == '3390']
            self.add_external_data(extracted_data)        