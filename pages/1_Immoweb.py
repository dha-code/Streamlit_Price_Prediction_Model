import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessing.cleaning_data import DataCleaner

st.title("Real Estate - Belgium")
preprocess = DataCleaner()

with st.form("my_form"):
    preprocess.zipcode = int(st.number_input("Zipcode", 1000, 9992, value=3390))
    submitted = st.form_submit_button("Submit")

if submitted:
    st.subheader("All properties in your locality")
    data = preprocess.read_property_data()
    data = data[data["Locality"] == preprocess.zipcode]

    col_list = [
        "Subtype",
        "Price",
        "Living area",
        "Bedrooms",
        "Bathrooms",
        "Construction year",
        "EPC score",
        "Building state",
        "Facades",
    ]
    data = data[col_list]

    st.dataframe(
        data,
        column_config={"Construction year": st.column_config.NumberColumn(format="%f")},
        hide_index=True,
    )

immo_all = pd.read_csv("./data/KNNInput.txt")
immo_all["Property type"] = immo_all["Property type"].map({1: "HOUSE", 0: "APARTMENT"})
immo_all["Region"] = immo_all["Region"].map(
    {1: "Brussels", 2: "Flanders", 3: "Wallonia"}
)
st.header("Price vs Living area for properties in Belgium")

g = sns.FacetGrid(
    immo_all, col="Region", row="Property type", hue="Region"
)  # , margin_titles=True)
g.map_dataframe(sns.scatterplot, x="Price", y="Living area")
g.set_titles("{row_name} : {col_name}")
st.pyplot(plt.gcf())