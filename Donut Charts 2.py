import plotly.graph_objects as go
import xcel_to_df
from plotly.subplots import make_subplots

# ### Donut Charts
# 
# In this part, we display the empty parking space (on average) by using donut charts
# 
# *Install plotly version 4.3.0 before proceed*

labels = ["S spot (permit)", "B spot (permit)", "A spot (permit)", "V spot"]

# Create subplots: use 'domain' type for Pie subplot
colors = ['rgb(255, 255, 100)', 'rgb(60,179,113)', 'rgb(220,20,60)',
          'rgb(220,220,220)']

fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
fig.add_trace(go.Pie(labels=labels, values=[1449.95, 502.5, 1002.9, 448.75], name="", marker_colors=colors),
              1, 1)
fig.add_trace(go.Pie(labels=labels, values=[79.4375, 179.5625, 148.23684210526315, 78.04347826086956], name="", marker_colors=colors),
              1, 2)

# Use `hole` to create a donut-like pie chart
fig.update_traces(hole=.4, hoverinfo="label+percent+name")

fig.update_layout(
    title_text="What are the percentages of average parking spaces (by permits) in year 2014 and 2019?",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='2014', x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text='2019', x=0.82, y=0.5, font_size=20, showarrow=False)])
fig.show()
