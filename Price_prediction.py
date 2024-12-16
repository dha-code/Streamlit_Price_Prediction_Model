import streamlit as st
from preprocessing.cleaning_data import DataCleaner
from predict.prediction import KNNPredict

preprocess = DataCleaner()
model = KNNPredict()
predicted_price = 0

page_bg = """
<style>
[data-testid="stAppViewContainer"] {
background-color: #fff8ea;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("Real Estate Price Prediction")
st.markdown("A k-nearest neighbour regression model to predict the value of a property in Belgium")
st.header("Enter the details of your property")

#st.subheader("This is the subheader")
#st.caption("This is the caption")
with st.form("my_form"):
    col1, col2 = st.columns(2)
    preprocess.property_type = col1.selectbox('Type of the property', ['House','Apartment'], index=0)
    preprocess.subtype = col1.selectbox('Property subtype', ['House/Town house','Apartment/Penthouse','Ground floor/Duplex/Triplex',
                                    'Bungalow/Loft/Chalet','Castle/Manor house/Farmhouse',
                                    'Villa/Country cottage/Mansion','Flat studio/Service flat/Kot','Exceptional property/Other'], index=0)
    preprocess.zipcode = int(col1.number_input('Zipcode', 1000, 9999, value=3390))
    preprocess.building_state = col1.selectbox('Condition of the property', ['Good','As new/Just renovated','To renovate/To restore','Unknown'], index=0)
    preprocess.bedrooms = col1.number_input('Number of bedrooms', 0, 30, value=4)
    preprocess.bathrooms = col1.number_input('Number of bathrooms', 0, 15, value=2)

    preprocess.land_surface = col2.number_input('Surface area of the plot', 0, 20000, value=500)
    preprocess.living_area = col2.number_input('Living area', 0, 2000, value=250)
    preprocess.year = col2.number_input('Construction year', 1700, 2024, value=1991)
    preprocess.epc = col2.selectbox('EPC score', ['A++/A+/A','B/C','D/E','F/G','Unknown'], index=1)
    preprocess.terrace_area = col2.number_input('If there is a terrace, its area', 0, 150, value=20)
    preprocess.facades = col2.number_input('Number of facades', 0, 6,value=4)
    submitted = st.form_submit_button("Submit")
    #start = st.button('Predict price')

    if submitted:
        processed_data = preprocess.preprocess()
        #st.dataframe(processed_data)
        define_model = model.load_model_and_scaler()
        predicted_price = model.predict(processed_data)
        
if predicted_price:

    st.subheader("Predicted price for your property:")
    price = f"€{predicted_price:,.2f}"
    st.success(price)

st.stop()