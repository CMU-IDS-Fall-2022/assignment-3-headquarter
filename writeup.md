# Project name

![A screenshot of your application. Could be a GIF.](Map.gif)

## Project Goals

**A clear description of the goals of your project.** 

- What is the price range & star distribution of different categories of restaurants in Philadelphia? 
- Are there any differences between different categories?
- Which category of restaurants is more common for a given price range & star?

## Design

**A rationale for your design decisions.** 

To answer the questions above, we would like to design functions including:

- Allow users to be able to filter according to restaurant categories in Philadelphia.
- Show the selected restaurants on the map of Philadelphia
- For a selected area, show the distribution of price range and stars of the restaurants
- For a selected area, show the number of restaurants in different categories
- For a selected price range and star, show the number of restaurants in different categories

And we adopted

- A stremlit multi-selection input widget
- A folium nteractive map that allows users to zoom in/out
- Tooltip on the map to show the name, address, star, and price range.
- Altair charts that shows the statistics of the selected map area
- Altair charts selection to allow users choose specific price range and stars

Alternatives we considered

- We would like to use the Altair map in the beginning as it is better to develop interactive features. However, it does not allow zooming in/out function, we turned to folium instead.
- We tried to use an altair chart to filter folim map, but it is not feasible. As a result, we turned to streamlit input to filter the map.


## Development

**An overview of your development process.** 

- At first, we worked together on the Exploratory Data Analysis and decided on the dataset we would like to work on, the data we need, and interaction techniques we want to include in our app.
- We split the work to data cleaning and interaction implementation among 2 of us. When encountering problems, we would schedule a meeting to discuss the blocks together.
- The data cleaning took about 13 hours. The interaction implementaton took about 12 hours.
- Time-consuming aspects: explore the data, find the right interaction tools, try to submit the big date file to the GIT

## Success Story

**A success story of your project.** 

- In Philadelphia, bars are significantly more than other restaurants. And the price range of bars are relatively higher. Also, bars usually have good stars.