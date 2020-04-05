from bokeh.plotting import figure, output_file, show, save
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral3
from bokeh.models.tools import HoverTool
import datetime
import os
import pandas as pd

base_path = 'public_html/'

# load data
df = pd.read_csv('covid-19-data/us-counties.csv')
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
march1st = datetime.datetime(2020, 3, 1, 0, 0, 0, 0)
df = df.loc[df['date'] > march1st]

states_to_render = ['California', 'Washington', 'New York']
for state in states_to_render:
    state_path = base_path + state
    if not os.path.exists(state_path):
        os.makedirs(state_path)

    state_frame = df.loc[df['state'] == state]
    for county in state_frame.county.unique():
        output_file(state_path + '/' + county + '.html', title=county + ' County Covid Cases')

        county_frame = state_frame.loc[state_frame['county'] == county]
        county_frame['new_cases'] = county_frame.sort_values(by='date').loc[:, 'cases'].diff()

        source = ColumnDataSource(county_frame)

        p = figure(x_axis_type='datetime')

        p.line(x='date', y='cases', line_width=2, source=source, legend_label='Total')
        p.vbar(x='date', top='new_cases', width=1, source=source, legend_label='New Cases', color='#FF0000')

        p.title.text = county + ' County Confirmed Covid Cases'
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Cases'

        hover = HoverTool()
        hover.tooltips=[
        #    ('Date', '@DateTime{%F}'),
            ('Total', '@cases'),
            ('New Cases', '@new_cases'),
        ]
        #hover.formatters = {'DateTime': 'date'}

        p.add_tools(hover)
        p.legend.location = 'top_left'

        save(p)
