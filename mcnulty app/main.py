# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs


# Each tab is drawn by one script
from scripts.book_tab import book_tab


# Using included state data from Bokeh for map
from bokeh.sampledata.us_states import data as states

# Read data into dataframes
df = pd.read_csv(join(dirname(__file__), 'data', '11-5 Plotting.csv'), 
	                                          index_col=0).dropna()
# Create each of the tabs
tab1 = book_tab(book_tab)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab1])

# Put the tabs in the current document for display
curdoc().add_root(tabs)
