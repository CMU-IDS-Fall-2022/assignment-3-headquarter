import streamlit as st
import pandas as pd
import altair as alt
import json
from vega_datasets import data

st.title("Let's analyze some Food Data in Philadaphia.")

##################################################################################
##################################################################################

st.header("1. Load Data")

def check_json_fmt(line):
    # This function check if the row has a valid json formate
    # param: str: the row of record read from text file
    # return: JSON object if parsed successfully, or None
    data = None
    try:
        data = json.loads(line)
    except:
        data = None
        print ("Fail: %s" % (line))
    return data

@st.experimental_memo
def load_data(file):
    raw_data = open(file).readlines()
    print ('Number of rows in the file: %d' % (len(raw_data)))
    filter_data = []
    for line in raw_data:
        data = check_json_fmt(line)
        if data != None:
            filter_data.append(data)        
    df = pd.json_normalize(filter_data)
    #df.info(verbose=True)
    return df

fin = 'yelp_academic_dataset_business.json'
df= load_data(fin)

st.text("Let's look at raw data in the Pandas Data Frame.")

st.dataframe(df)

##################################################################################
##################################################################################

st.header("2. Data ETL")

st.text("Filter by City: Philadelphia \n Filter by Category: contains the key word: [Restaurants, Food] \n Filter by Column \n Drop Duplicate \n Handle Missing Data")

def convert_categorary_column(row):
    '''
    This function convert the string of categories to a list
    '''
    row = row.split(',')
    row = [s.strip() for s in row]
    return row

def create_is_restaurant_column(row):
    '''   
    This function filter the rows with key word: 'Restaurants' or 'Food' 
    '''
    if ('Restaurants' in row) or ('Food' in row):
        return True
    else:
        return False

def handle_missing(df, handle):
    """
    This function handle the missing data
    """
    for colName in handle:
        print ("==== column: %s ====" % (colName))
        if handle[colName] == 'del':
            df.dropna(subset=[colName], inplace=True)
            print ("  -- The missing row is deleted")
        else:
            df[colName].fillna(handle[colName], inplace=True)
            print ("  -- The missing row is filled with %s" % ("Unknown"))
    return df

@st.experimental_memo
def data_clean(df):
    # Keep the Philidaphia data
    newDf = df[df['city']=='Philadelphia']

    # Filter by Category
    newDf.dropna(subset = ['categories'], inplace=True)
    newDf['category_list'] = newDf['categories'].apply(convert_categorary_column)
    newDf['is_restaurant'] = newDf['category_list'].apply(create_is_restaurant_column)
    newDf = newDf[newDf['is_restaurant']==True]

    # Filter by Column
    COLUMNS = ['business_id', 'name', 'address', 'city', 'state',  
             'latitude', 'longitude', 'stars', 'review_count', 'category_list', 
             'attributes.RestaurantsPriceRange2', 'attributes.RestaurantsTakeOut', 
             'attributes.RestaurantsDelivery', 'attributes.WheelchairAccessible']
    newDf = newDf[COLUMNS]

    # Drop Duplicate
    newDf.drop_duplicates(subset=['business_id'], keep='first', inplace=False)

    NEW_COL_NAME = ['id', 'name', 'address', 'city', 'state', 'latitude', 'longitude',
                    'stars', 'review_count', 'categories', 'price_range', 'takeout',
                    'delivery', 'wheelchair_access']
    newDf.columns = NEW_COL_NAME
    newDf = newDf.drop(['id'], axis=1)

    # Handle Missing Data
    MISS_HANDLE = {
        'name': 'del', 
        'address': 'del', 
        'city': 'del', 
        'state': 'del', 
        'latitude': 'del', 
        'longitude': 'del', 
        'stars': 'del', 
        'review_count': 'del', 
        'categories': 'del',
        'price_range': -1, 
        'takeout': 'Unknown', 
        'delivery': 'Unknown', 
        'wheelchair_access': 'Unknown'
    }
    newDf = handle_missing(newDf, MISS_HANDLE)
    return newDf

newDf = data_clean(df)

st.dataframe(newDf)

# st.map(newDf)


################################
#Version one: Background map + interactive points

counties = alt.topo_feature(data.us_10m.url, feature='counties')

#US states background
background = alt.Chart(counties).mark_geoshape(
    fill='lightgray',
    stroke='white'
).properties(
    width=500,
    height=300
).project('albersUsa').interactive()

click = alt.selection_multi(encodings=['color'])

# restaurant positions on background
points = alt.Chart(newDf).mark_circle().encode(
    longitude='longitude:Q',
    latitude='latitude:Q',
    color=alt.value('steelblue'),
    tooltip=['name:N']
).properties(
    title='Restaurants in Phili'
).transform_filter(
    click
)

hist = alt.Chart(newDf).mark_bar().encode(
    x='count()',
    y='stars',
    color=alt.condition(click, 'stars', alt.value('lightgray'))
).add_selection(
    click
)

st.altair_chart(background + points & hist)


st.markdown("This project was created by Hazel Zhang and Qianru Zhang for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
