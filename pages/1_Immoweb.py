import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Real Estate Reality - Belgium")

immo_all = pd.read_csv("./data/KNNInput.txt")

immo_all["Property type"] = immo_all["Property type"].map({1:"HOUSE",0:"APARTMENT"})
immo_all["Region"] = immo_all["Region"].map({1:"Brussels",2:"Flanders",3:"Wallonia"})

g = sns.FacetGrid(immo_all, col='Region', row='Property type', hue="Region") #, margin_titles=True)
g.map_dataframe(sns.scatterplot, x='Price', y='Living area')
g.set_titles('{row_name} : {col_name}')
st.pyplot(plt.gcf())