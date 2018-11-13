import pandas as pd
import numpy as np
import time
import scipy.stats
import hashlib
from os.path import dirname, join
from scipy.stats import norm

df2 = pd.read_csv('11-5 Plotting.csv')
trial = df2

min_pop_val = min(trial.log_times_rated)
max_pop_val = max(trial.log_times_rated)

min_good_val = min(trial.mu)-2.326*max(trial['stdev'])
max_good_val = max(trial.mu)+2.326*max(trial['stdev'])

from bokeh.layouts import layout, WidgetBox
from bokeh.models import ColumnDataSource, Div
from bokeh.models.widgets import Slider, Select, TextInput, RangeSlider
from bokeh.io import curdoc
from bokeh.colors import RGB
from bokeh.layouts import row

from bokeh.plotting import figure, show, output_file, reset_output, output_notebook
from bokeh.tile_providers import CARTODBPOSITRON
from bokeh.models import ColumnDataSource, ColorBar, HoverTool, LinearColorMapper, NumeralTickFormatter
from bokeh.io import export_png
import bokeh
from bokeh.models import Panel
from bokeh.models.widgets import Tabs

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

def book_tab(doc):
    
    pal = bokeh.palettes.RdBu[11][::-1]
    mapper = LinearColorMapper(palette=pal, 
                               low = np.mean(df2.mu)-2*np.std(df2.mu), 
                               high =np.mean(df2.mu)+2*np.std(df2.mu))
    
    min_pop_val = min(trial.log_times_rated)
    max_pop_val = max(trial.log_times_rated)

    min_good_val = min(trial.mu)-2.326*max(trial['stdev'])
    max_good_val = max(trial.mu)+2.326*max(trial['stdev'])
    

    def make_dataset(trial, range_start=0, range_end=max_pop_val, z_score=50, 
                     book_quality=50,
                    axis_1='factor1', axis_2='factor2'):
        trial = trial[trial.log_times_rated>range_start]
        trial =  trial[trial.log_times_rated<range_end]
        
        desired_area = z_score/100
        
        bar = (max_good_val)*(book_quality-50)/50
        
        def norm_dist_over(x):
            norm(loc=x.mu, scale=x.stdev)
            return 1-norm.cdf(bar)
        
        trial['area'] = (1-norm(loc=trial.mu, scale=trial.stdev).cdf(bar))
                
        trial = trial[trial.area>desired_area]
        
        trial['X'] = trial[axis_1]
        trial['Y'] = trial[axis_2]
        
        if len(trial) > 1000:
            trial = trial.sample(1000)
        return ColumnDataSource(trial)

    def make_plot(src):
        hover_tool = HoverTool(tooltips =[
            ("Title", "@title"),
            ("Author", "@author"),
            ("Average Rating", "@avg_rating"),
            ("Times Rated", "@times_rated")
            ])

        p = figure()
        p.circle(source=src, x='X', y='Y', size=10,
                 fill_color={'field':'mu', 'transform': mapper}, alpha=0.8, line_color="black",
                legend=False)

        p.add_tools(hover_tool)
        return(p)

    def update(attr, old, new):
        range_start = range_select.value[0]
        range_end = range_select.value[1]
        z_score = z_slider.value
        min_good = goodness_select.value
        axis_1 = axis1.value
        axis_2 = axis2.value
        new_src = make_dataset(trial, range_start, range_end, z_score, min_good, axis_1, axis_2)
        src.data.update(new_src.data)
        
   
    src = make_dataset(trial)
    p = make_plot(src)
    
    range_select = RangeSlider(start = min_pop_val, end = max_pop_val, value = (min_pop_val,min_pop_val+5),
                               step = .1, title = 'Times Rated (log10-range)')
    range_select.on_change('value', update)
    
    z_slider = Slider(start = 0, end = 100, value = 20, title = 'Readership Appeal %', step =1)
    z_slider.on_change('value', update)
    
    goodness_select = Slider(start = 0, end = 100, value = 50,
                            step = 1, title = 'Book Quality Percentile')
    goodness_select.on_change('value', update)
    
    axis1 = Select(title="Axis 1:", value="factor1", options=['factor1', 'factor2','factor3','factor4','factor5'])
    axis1.on_change('value', update)
    
    axis2 = Select(title="Axis 1:", value="factor2", options=['factor1', 'factor2','factor3','factor4','factor5'])
    axis2.on_change('value', update)

    # Create a row layout
    # Put controls in a single element
    controls = WidgetBox(range_select, z_slider, goodness_select, axis1, axis2)
    layout = row(controls, p)

    tab =  Panel(child=layout, title='Book Explorer')
    return(tab)

