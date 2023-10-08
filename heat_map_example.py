import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

# While the code for the actual implementation would retrieve data from the graph database on server,
# this example uses a downloaded database from DataSF (https://data.sfgov.org/City-Infrastructure/streetlights/6tt8-ugnj). 
# It maps some street lights in the center of SF. 
# Moreover, a shape map of San Francisco is downloaded from 
# https://earthworks.stanford.edu/?_=1475263344737&bbox=-122.73495+37.462852+-122.152675+37.893262&f%5Baccess%5D%5B%5D=public&f%5Bdc_format_s%5D%5B%5D=Shapefile&f%5Bdct_spatial_sm%5D%5B%5D=San+Francisco+Bay+Area+%28Calif.%29&page=2&per_page=50&sort=dc_title_sort+asc


# set the background
sns.set(style="whitegrid", palette="pastel", color_codes=True) 
sns.mpl.rc("figure", figsize=(10,6))

#opening the vector map
shp_path = "planning_neighborhoods.dbf"
#reading the shape file by using reader function of the shape lib
sf = shp.Reader(shp_path)

# the function takes as input the file variable and returns the corresponding pandas dataframe
def read_shapefile(sf):
    #fetching the headings from the shape file
    fields = [x[0] for x in sf.fields][1:]
    #fetching the records from the shape file
    records = [list(i) for i in sf.records()]
    shps = [s.points for s in sf.shapes()]
    #converting shapefile data into pandas dataframe
    shape_map_df = pd.DataFrame(columns=fields, data=records)
    #assigning the coordinates
    shape_map_df = shape_map_df.assign(coords=shps)
    return shape_map_df


shape_map_df = read_shapefile(sf)
## This dataset is an example of street lights in the city of san francisco. 
street_lights_df = pd.read_csv('streetlights.csv')

# returns the mean of danger levels for each neighborhood.  
neighborhood_danger_map = street_lights_df.groupby('Neighborhood')['DangerLevel'].mean().to_list()

# each neighborhood now needs to be mapped. It will be assigned a color based on the danger level. 
def plot_sf_map():
    count = 0
    for shape in sf.shapes():
        # get the x and y coordinates for the shape
        x, y = zip(*shape.points)
        # plot the shape and a number inside it
        color = ''
        # we had to use an excpetion to be account for the different number of neighborhoods 
        # considered by the shape map and the list neighborhood_danger_map. 
        # This is due to the fact that some neighborhoods do not have any street lights mapped in the sample dataset.
        try: 
            if (neighborhood_danger_map[count] <= 1):
                color = 'green'
            elif (neighborhood_danger_map[count] <= 2):
                color = 'yellow'
            elif (neighborhood_danger_map[count] <= 3):
                color = 'orange'
            else:
                color = 'red'
            count  += 1
        except:
            color = 'white'
        plt.fill(x, y, color=color, alpha=0.5)
        #plt.text(x[1], y[1], s='Yoooo', fontsize=10, color='black')
        plt.plot(x, y, color='black')
    # the patch sub module is useful for the colored rectangles in the legend. 
    green_patch = mpatches.Patch(color='green', label='Low Danger')
    yellow_patch = mpatches.Patch(color='yellow', label='Moderate Danger')
    orange_patch = mpatches.Patch(color='orange', label='High Danger')
    red_patch = mpatches.Patch(color='red', label='Very High Danger')
    # add the legend to the plot
    plt.legend(handles=[green_patch, yellow_patch, orange_patch, red_patch], loc='lower left')
    plt.show()


plot_sf_map()
