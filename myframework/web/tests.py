from django.test import TestCase

# Create your tests here.

import plotly.express as px

# Sample data for the bar chart
data = {
    'X': ['Round 1', 'Round 2'],
    'Y1': [30, 40],
    'Y2': [10, 20]
}

# Create a bar chart using Plotly Express
fig = px.bar(data, x='X', y=['Y1', 'Y2'], title='Bar Chart with Two Values')

# Show the chart
fig.show()