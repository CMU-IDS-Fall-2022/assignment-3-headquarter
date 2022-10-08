import streamlit as st
import pandas as pd
import altair as alt
import json
# from vega_datasets import data

st.title("Let's analyze some Food Data in Philadaphia.")

@st.cache  # add caching so we load the data only once

def load_data():
    # Load the business data
    fin = 'yelp_academic_dataset_business.json'
    raw_data = open (fin).readlines()

df = load_data()

# print ('Number of rows in the file: %d' % (len(raw_data)))
# print (raw_data[1])



st.write("Let's look at raw data in the Pandas Data Frame.")

st.write(df)

st.write("Hmm 🤔, is there some correlation between body mass and flipper length? Let's make a scatterplot with [Altair](https://altair-viz.github.io/) to find.")




# chart = alt.Chart(df).mark_point().encode(
#     x=alt.X("body_mass_g", scale=alt.Scale(zero=False)),
#     y=alt.Y("flipper_length_mm", scale=alt.Scale(zero=False)),
#     color=alt.Y("species")
# ).properties(
#     width=600, height=400
# ).interactive()

# st.write(chart)

st.markdown("This project was created by Hazel Zhang and Qianru Zhang for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
