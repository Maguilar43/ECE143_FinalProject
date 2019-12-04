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
fig.add_trace(go.Pie(labels=labels, values=[2740.3, 579.45, 895.975, 232.525], name="", marker_colors=colors),
              1, 1)
fig.add_trace(go.Pie(labels=labels, values=[2300.15, 499.925, 1002.9, 411.1], name="", marker_colors=colors),
              1, 2)

# Use `hole` to create a donut-like pie chart
fig.update_traces(hole=.4, hoverinfo="label+percent+name")

fig.update_layout(
    title_text="What are the percentages of average empty parking spaces (by permits) in year 2000 and 2010?",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='2000', x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text='2010', x=0.82, y=0.5, font_size=20, showarrow=False)])
fig.show()

