from bokeh.plotting import figure, output_file, show, save
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral3
from bokeh.models.tools import HoverTool
import datetime
import json
import os
import pandas as pd

def render_graph(output_file_path, title, data_frame):
    output_file(output_file_path, title=title)

    source = ColumnDataSource(data_frame)

    p = figure(x_axis_type='datetime')

    p.line(x='date', y='cases', line_width=2, source=source, legend_label='Total')
    p.vbar(x='date', top='new_cases', line_width=5, source=source, legend_label='New Cases', color='#FF0000')
    p.line(x='date', y='deaths', line_width=2, source=source, legend_label='Deaths', color='#000000')

    p.title.text = title
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Cases'

    hover = HoverTool()
    hover.tooltips=[
#            ('Date', '@date{%F}'),
        ('Total', '@cases'),
        ('New Cases', '@new_cases'),
        ('Deaths', '@deaths'),
    ]
#        hover.formatters = {'Date': 'datetime'}

    p.add_tools(hover)
    p.legend.location = 'top_left'

    save(p)

# actually do stuff
base_output_path = 'public_html/'
march8 = datetime.datetime(2020, 3, 8, 0, 0, 0, 0)
states_and_counties = {} # used to populate html dropdowns

# render state graphs
df = pd.read_csv('covid-19-data/us-states.csv')
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df = df.loc[df['date'] > march8]

states = df.state.unique().tolist()
states.sort()
for state in states:
    state_path = base_output_path + state
    if not os.path.exists(state_path):
        os.makedirs(state_path)

    state_frame = df.loc[df['state'] == state]
    state_frame = state_frame.assign(new_cases=state_frame.sort_values(by='date').loc[:, 'cases'].diff())

    render_graph(state_path + '.html', state + ' State Covid Cases', state_frame)

# render all states
df = df.drop(columns=['state', 'fips'])
df = df.groupby('date').sum()
df = df.assign(new_cases=df.sort_values(by='date').loc[:, 'cases'].diff())

render_graph(base_output_path + 'all_states.html', 'United States Covid Cases', df)

# render county graphs
df = pd.read_csv('covid-19-data/us-counties.csv')
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df = df.loc[df['date'] > march8]

states = df.state.unique().tolist()
states.sort()
for state in states:
    state_path = base_output_path + state

    state_frame = df.loc[df['state'] == state]

    counties = state_frame.county.unique().tolist()
    counties.sort()
    states_and_counties[state] = counties
    for county in counties:
        county_frame = state_frame.loc[state_frame['county'] == county]
        county_frame = county_frame.assign(new_cases=county_frame.sort_values(by='date').loc[:, 'cases'].diff())

        render_graph(state_path + '/' + county + '.html', county + ' County Covid Cases', county_frame)

# save states and counties
with open(base_output_path + 'states_and_counties.json', 'w') as fp:
    json.dump({
        'updated_at': datetime.datetime.now().__str__() + ' UTC',
        'states_and_counties': states_and_counties,
        }, fp)

