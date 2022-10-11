# import streamlit as st
# import pandas as pd
# import altair as alt
# import json
# #from vega_datasets import data
# import geopandas as gpd

# st.title("Let's analyze some Food Data in Philadaphia.")

# ##################################################################################
# ##################################################################################

# st.header("1. Load Data")

# def check_json_fmt(line):
#     # This function check if the row has a valid json formate
#     # param: str: the row of record read from text file
#     # return: JSON object if parsed successfully, or None
#     data = None
#     try:
#         data = json.loads(line)
#     except:
#         data = None
#         print ("Fail: %s" % (line))
#     return data

# @st.experimental_memo
# def load_data(file):
#     raw_data = open(file).readlines()
#     print ('Number of rows in the file: %d' % (len(raw_data)))
#     filter_data = []
#     for line in raw_data:
#         data = check_json_fmt(line)
#         if data != None:
#             filter_data.append(data)        
#     df = pd.json_normalize(filter_data)
#     #df.info(verbose=True)
#     return df

# fin = 'yelp_academic_dataset_business.json'
# df= load_data(fin)

# st.text("Let's look at raw data in the Pandas Data Frame.")

# st.dataframe(df)

# ##################################################################################
# ##################################################################################

# st.header("2. Data ETL")

# st.text("Filter by City: Philadelphia \n Filter by Category: contains the key word: [Restaurants, Food] \n Filter by Column \n Drop Duplicate \n Handle Missing Data")

# def convert_categorary_column(row):
#     '''
#     This function convert the string of categories to a list
#     '''
#     row = row.split(',')
#     row = [s.strip() for s in row]
#     return row

# def create_is_restaurant_column(row):
#     '''   
#     This function filter the rows with key word: 'Restaurants' or 'Food' 
#     '''
#     if ('Restaurants' in row) or ('Food' in row):
#         return True
#     else:
#         return False

# def handle_missing(df, handle):
#     """
#     This function handle the missing data
#     """
#     for colName in handle:
#         print ("==== column: %s ====" % (colName))
#         if handle[colName] == 'del':
#             df.dropna(subset=[colName], inplace=True)
#             print ("  -- The missing row is deleted")
#         else:
#             df[colName].fillna(handle[colName], inplace=True)
#             print ("  -- The missing row is filled with %s" % ("Unknown"))
#     return df

# @st.experimental_memo
# def data_clean(df):
#     # Keep the Philidaphia data
#     newDf = df[df['city']=='Philadelphia']

#     # Filter by Category
#     newDf.dropna(subset = ['categories'], inplace=True)
#     newDf['category_list'] = newDf['categories'].apply(convert_categorary_column)
#     newDf['is_restaurant'] = newDf['category_list'].apply(create_is_restaurant_column)
#     newDf = newDf[newDf['is_restaurant']==True]

#     # Filter by Column
#     COLUMNS = ['business_id', 'name', 'address', 'city', 'state',  
#              'latitude', 'longitude', 'stars', 'review_count', 'category_list', 
#              'attributes.RestaurantsPriceRange2', 'attributes.RestaurantsTakeOut', 
#              'attributes.RestaurantsDelivery', 'attributes.WheelchairAccessible']
#     newDf = newDf[COLUMNS]

#     # Drop Duplicate
#     newDf.drop_duplicates(subset=['business_id'], keep='first', inplace=False)

#     NEW_COL_NAME = ['id', 'name', 'address', 'city', 'state', 'latitude', 'longitude',
#                     'stars', 'review_count', 'categories', 'price_range', 'takeout',
#                     'delivery', 'wheelchair_access']
#     newDf.columns = NEW_COL_NAME
#     newDf = newDf.drop(['id'], axis=1)

#     # Handle Missing Data
#     MISS_HANDLE = {
#         'name': 'del', 
#         'address': 'del', 
#         'city': 'del', 
#         'state': 'del', 
#         'latitude': 'del', 
#         'longitude': 'del', 
#         'stars': 'del', 
#         'review_count': 'del', 
#         'categories': 'del',
#         'price_range': -1, 
#         'takeout': 'Unknown', 
#         'delivery': 'Unknown', 
#         'wheelchair_access': 'Unknown'
#     }
#     newDf = handle_missing(newDf, MISS_HANDLE)
#     return newDf

# newDf = data_clean(df)

# st.dataframe(newDf)

# # st.map(newDf)


# ################################
# #Version one: Background map + interactive points


# ##US states background
# #counties = alt.topo_feature(data.us_10m.url, feature='counties')
# #background = alt.Chart(counties).mark_geoshape(
# #    fill='lightgray',
# #    stroke='white'
# #).properties(
# #    width=500,
# #    height=300
# #).project('albersUsa')

# gdf = gpd.read_file('./PhillyPlanning_Neighborhoods/PhillyPlanning_Neighborhoods.shp')
# #Creating an altair map layer
# choro = alt.Chart(gdf).mark_geoshape(
#     stroke='black'
# ).properties(
#     width=500,
#     height=300
# )

# # .encode(
# #     color=color
# #    tooltip=['state','count']

# # click = alt.selection_multi(encodings=['color'])

# # # restaurant positions on background
# # points = alt.Chart(newDf).mark_circle().encode(
# #     longitude='longitude:Q',
# #     latitude='latitude:Q',
# #     color=alt.value('steelblue'),
# #     tooltip=['name:N']
# # ).properties(
# #     title='Restaurants in Phili'
# # ).transform_filter(
# #     click
# # )

# # hist = alt.Chart(newDf).mark_bar().encode(
# #     x='count()',
# #     y='stars',
# #     color=alt.condition(click, 'stars', alt.value('lightgray'))
# # ).add_selection(
# #     click
# # )

# st.altair_chart(choro)


# st.markdown("This project was created by Hazel Zhang and Qianru Zhang for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")


import pandas as pd
from pandas.io.json import json_normalize
import json
import streamlit as st
import altair as alt

###############################################################################
#       1. Load Data
###############################################################################
def check_json_fmt(line):
    '''
    This function check if the row has a valid json formate
    param: str: the row of record read from text file
    return: JSON object if parsed successfully, or None
    '''
    data = None
    try:
        data = json.loads(line)
    except:
        data = None
        print ("Fail: %s" % (line))
    return data


@st.experimental_memo
def load_data(file):
    raw_data = open(file, encoding="utf-8").readlines()
    #print ('Number of rows in the file: %d' % (len(raw_data)))
    filter_data = []
    for line in raw_data:
        data = check_json_fmt(line)
        if data != None:
            filter_data.append(data)        
    df = json_normalize(filter_data)
    #df = pd.json_normalize(filter_data)
    #df.info(verbose=True)
    return df

###############################################################################
#       2. Data ETL
#           - Filter by City: Philadelphia
#           - Filter by Category: contains the key word: [Restaurants, Food]
#           - Filter by Column
#           - Drop Duplicate
#           - Handle Missing Data
###############################################################################

def convert_categorary_column(df):
    '''
    This function convert the string of categories to a list
    '''
    newDf = df.copy()
    newDf['categories'] = df['categories'].apply(lambda row: [s.strip() for s in row.split(',')])
    return newDf

def filter_by_categoary(df, categoryList):
    '''
    This function filter the restaurant by the given categoary
    '''
    mask = df['categories'].apply(lambda row: any(x in categoryList for x in row))
    df = df[mask]

    return df

def filter_restaurant(df):
    '''
    This function filter the rows with key word: 'Restaurants'
    '''
    categoryList = ['Restaurants']
    newDf = filter_by_categoary(df, categoryList)
    return newDf

def handle_missing(df, handle):
    """
    This function handle the missing data
    """
    for colName in handle:
        #print ("==== column: %s ====" % (colName))
        if handle[colName] == 'del':
            df.dropna(subset=[colName], inplace=True)
            #print ("  -- The missing row is deleted")
        else:
            df[colName].fillna(handle[colName], inplace=True)
            #print ("  -- The missing row is filled with %s" % ("Unknown"))
    return df

def filter_categoary(df, categoaryList):
    """
    This function only keep the selected category
    """
    newDf = df.copy()
    newDf['categories'] = df['categories'].apply(lambda row: [x for x in row if x in categoaryList])
    return newDf


@st.experimental_memo
def data_clean(df, selectCategList):
    # Keep the Philidaphia data
    newDf = df[df['city']=='Philadelphia']

    # Filter by Category
    newDf.dropna(subset=['categories'], inplace=True)
    newDf = convert_categorary_column(newDf)
    newDf = filter_restaurant(newDf)

    # Filter by Column
    COLUMNS = ['business_id', 'name', 'address', 'city', 'state',  
             'latitude', 'longitude', 'stars', 'review_count', 'categories', 
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
    newDf = newDf.replace({'price_range': 'None'}, -1)

    # Format column
    COLUMN_FORMAT = {
        'name': str,
        'address': str,
        'city': str,
        'state': str,
        'latitude': float, 
        'longitude': float, 
        'stars': float, 
        'review_count': int, 
        'price_range': int, 
        'takeout': str, 
        'delivery': str, 
        'wheelchair_access': str
    }
    newDf = newDf.astype(COLUMN_FORMAT)

    # Keep only the selected categories (the rows contains at least one in the list)
    # Keep only the selected catgories (the list only contains the selected key word)
    newDf = filter_by_categoary(newDf, selectCategList)
    newDf = filter_categoary(newDf, selectCategList)

    return newDf

###############################################################################
#       3. Data Interactive Filter
###############################################################################

def select_data_by_filter(df, categorySelected):
    """
    This function help to filter the data by user selected filters
    """
    newDf = df.copy()

    # if isDelivery:
    #     newDf = newDf[newDf['delivery']=='True']
    # if isTakeout:
    #     newDf = newDf[newDf['takeout']=='True']
    # if isAccess:
    #     newDf = newDf[newDf['wheelchair_access']=='True']
    
    # if priceRange != 'ALL':
    #     newDf = newDf[(newDf['price_range']<=int(priceRange)) & (newDf['price_range']>0)]
    
    newDf = filter_by_categoary(newDf, categorySelected)
    return newDf


def select_data_by_map(df, mapBounds):
    """
    This function help to filter the data by user selected map
    """
    newDf = df.copy()
    minLat, maxLat = float(mapBounds['_southWest']['lat']), float(mapBounds['_northEast']['lat'])
    minLng, maxLng = float(mapBounds['_southWest']['lng']), float(mapBounds['_northEast']['lng'])
    newDf = newDf[(newDf['latitude']>=minLat) & (newDf['latitude']<=maxLat) & 
                  (newDf['longitude']>=minLng) & (newDf['longitude']<=maxLng)]
    return newDf 

def get_name_address(df):
    newDf = df[['name', 'address']].sort_values('name')
    newDf.reset_index(drop=True, inplace=True)
    return newDf

###############################################################################
#       4. Altair Plots
###############################################################################

# def plot_scatter(df):
#     """
#     This function plot the review count and star scatter for the selected restaurants
#     """
#     #df = df.explode('categories').reset_index(drop=True)
#     scatter = alt.Chart(df).mark_point().encode(
#         alt.X("review_count", scale=alt.Scale(zero=False), title="Review Count"),
#         alt.Y("stars", scale=alt.Scale(zero=False), title="Star")
#     )
#     return scatter


# def plot_histogram(df):
#     """
#     This function plot the star histogram for the selected restaurants
#     """
#     #df = df.explode('categories').reset_index(drop=True)
#     hist = alt.Chart(df).mark_bar().encode(
#         alt.X("stars", bin=alt.Bin(maxbins=5), title="Star"),
#         alt.Y("count()", title="The number of stars")
#     )
#     return hist


# def plot_rule(df):
#     """
#     This function plot the average restartaurant star
#     """
#     #df = df.explode('categories').reset_index(drop=True)
#     rule = alt.Chart(df).mark_rule().encode(
#         alt.Y("stars", title="Star"),
#         alt.Color("categories")
#     )
#     return rule

def plot_binnedscatter(df):
	binned_scatter = alt.Chart(df).mark_circle().encode(
    	alt.X('stars', bin=True, title="Star"),
    	alt.Y('price_range', bin=True, title="Price Range"),
    	size='count()'
	)

	return binned_scatter

def plot_hist(df):
	hist = alt.Chart(df).mark_bar().encode(
    	alt.Y('categories'),
    	alt.X('count()')
	)

	return hist

def plot_altair(df, categorySelected):
    """
    This function plot the interactive scatter and histogram
    """
    df = df.explode('categories').reset_index(drop=True)
    df = df[df['categories'].isin(categorySelected)]
    # scatter = plot_scatter(df)
    # hist = plot_histogram(df)
    # rule = plot_rule(df)

    # selection = alt.selection_interval()
    # fig = scatter.add_selection(selection).encode(
    #     color=alt.condition(selection, "categories", alt.value("grey"))
    # ) + rule | hist.encode(
    #     alt.Color("categories")
    # ).transform_filter(selection)

    single = alt.selection_interval()

    binned_scatter = plot_binnedscatter(df)
    hist = plot_hist(df)

    binned_scatter = binned_scatter.add_selection(single).encode(
        color=alt.condition(single, "stars", alt.value("grey"))
    ) 

    hist = hist.encode(
        alt.Color("categories")
    ).transform_filter(single)

    return alt.vconcat(binned_scatter, hist)

##################################################################################
##################################################################################


import streamlit as st
import folium
from streamlit_folium import st_folium


# Load Data
fin = 'yelp_academic_dataset_business.json'
df = load_data(fin)

# Data ETL
# Keep the following 30 categoaries only
SELECTED_CATEGOARIES = ['Mexican', 'Chinese', 'Italian', 'Thai', 'Japanese', 'Korean',
    'Vietnamese',  'American (New)',  'American (Traditional)', 'Mediterranean', 'French',
    'Latin American', 'Indian', 'Breakfast & Brunch', 'Cafes', 'Bars', 'Desserts', 'Vegetarian', 
    'Sandwiches', 'Barbeque', 'Pizza', 'Seafood', 'Burgers', 'Steakhouses', 'Tacos', 'Sushi Bars',
    'Fast Food', 'Delis', 'Chicken Wings', 'Diners']
SELECTED_CATEGOARIES.sort()
newDf = data_clean(df, SELECTED_CATEGOARIES)

##################################################################################
##################################################################################

def create_map_figure(df):
    '''
    This function plot the map of Philidaphia and the restaurant on top of it
    PARAM:
        df:: [dataframe] the list of the restaurant that pass the filter
    '''
    # create the base map
    map = folium.Map(location=[39.99, -75.13], zoom_start=11)
    
    # add restaurant to map
    feature_group = folium.FeatureGroup("Locations")
    latList, lngList, nameList, addressList, starList, priceList= df['latitude'].to_list(), df['longitude'].to_list(), df['name'].to_list(), df['address'].to_list(), df['stars'].to_list(), df['price_range'].to_list()
    for lat, lng, name, address, star, price in zip(latList, lngList, nameList, addressList, starList, priceList):
        feature_group.add_child(folium.Marker(location=[lat,lng],
                                              tooltip=""" 
                                              <i>Name: </i> <br> <b>{}</b> <br> 
                                                <i>Address: </i><b><br>{}</b><br>
                                                <i>Stars: </i><b><br>{}</b><br>
                                                <i>Price Range: </i><b><br>{}</b><br>
                                              """.format(name,address,star,price)))
    map.add_child(feature_group)

    return map

##################################################################################
##################################################################################

st.title("Let's analyze some Food Data in Philadaphia.")
with st.sidebar:
    sideChoice = st.radio(
        "Choose a page", 
        ("Load Data", "Data ETL", "Food Map")
    )

##################################################################################
##################################################################################
if sideChoice == "Load Data":
    st.header("Load Data")
    st.text("Let's look at raw data in the Pandas Data Frame.")
    st.dataframe(df, use_container_width=True)

##################################################################################
##################################################################################
elif sideChoice == "Data ETL":
    st.header("Data ETL")
    st.text(" Filter by City: Philadelphia \n Filter by Category: contains the key word \n Filter by Column \n Drop Duplicate \n Handle Missing Data")
    st.dataframe(newDf, use_container_width=True)

##################################################################################
##################################################################################
elif sideChoice == "Food Map":
    st.header("Food Map")
    # st.subheader("Restaurant filters")
    # isDelivery = st.checkbox('Delivery', key='delivery')
    # isTakeout = st.checkbox('Takeout', key='takeout')
    # isAccess = st.checkbox('Wheelchair Access', key='accessibility')
    # priceRange = st.select_slider('Pick a price range', ['1', '2', '3', '4', 'ALL'])

    st.subheader("Restaurant categoaries")
    categorySelected = st.multiselect('Categories', SELECTED_CATEGOARIES)

    # Filter the data by selection
    filterDf = select_data_by_filter(newDf, categorySelected)

    # Plot the map and the selected restaurants
    st.subheader("Restaurant locations")
    map = create_map_figure(filterDf)
    st_data = st_folium(map, width=700, height=700)
    mapBounds = st_data['bounds']
    
    # Filter the data by map size
    selectDf = select_data_by_map(filterDf, mapBounds)

    # Plot the histogram etc. by altair
    st.subheader("Restaurant reviews and stars")
    alt_fig = plot_altair(selectDf, categorySelected)
    st.altair_chart(alt_fig)

    # # Show the address and name of the restaurants
    # st.subheader("Restaurant names and addresses")
    # dfNameAddress = get_name_address(selectDf)
    # st.dataframe(dfNameAddress, use_container_width=True)

##################################################################################
##################################################################################

