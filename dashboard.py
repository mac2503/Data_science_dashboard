"""
Plotly is a Python graphing library which is used to make interactive graphs.
In this code, I have plotted density plot, pie chart, histogram and scatter plot.
"""
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Reading the csv file using pandas
df = pd.read_csv("onlinedeliverydata.csv")
print("Dataset Size : ", df.shape)
print(df.head())

# A density plot is a representation of the distribution of a numeric variable.
# It is a smoothed version of the histogram and is used in the same concept.
x1 = df.loc[df['Buy_again'] == 'Yes', "Age"]
x2 = df.loc[df['Buy_again'] == 'No', "Age"]
data = [x1, x2]
group_labels = ['Yes', 'No']
colors = ["#58508d", "#bc5090"]
fig = ff.create_distplot(data, group_labels, colors=colors, show_hist=False, show_rug=False)
chart1 = fig.update_layout(title_text='Density Plot: Age color-encoded by Output (Buy again)')

"""
A pie chart is a type of graph in which a circle is divided into 
sectors that each represents a proportion of the whole.
"""
labels = ['Male', 'Female']
res1 = df.groupby(['Gender', 'Buy_again']).size().reset_index().pivot(columns='Gender', index='Buy_again', values=0)
one1 = res1.iloc[0, :].tolist()
two1 = res1.iloc[1, :].tolist()
print(one1)
print(two1)

# Create subplots: use 'domain' type for Pie subplot
fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

# New traces can be added to a graph object figure using the add_trace() method.
# This method accepts a graph object trace and adds it to the figure.
# This allows us to start with an empty figure, and add traces to it sequentially.
fig.add_trace(go.Pie(labels=labels, values=two1, name="Yes"), 1, 1)
fig.add_trace(go.Pie(labels=labels, values=one1, name="No"), 1, 2)

# Use `hole` to create a donut-like pie chart
fig.update_traces(hole=.4, hoverinfo="label+percent+name", marker=dict(colors=colors))

# Update the properties of the figure’s layout with a dict
chart2 = fig.update_layout(title_text="Pie Chart: Gender by Output (Buy again)",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='Yes', x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text='No', x=0.82, y=0.5, font_size=20, showarrow=False)])

"""
A histogram provides a visual representation of the distribution of a dataset
"""
chart3 = px.histogram(data_frame=df,
             x="Buy_again",
             color="Monthly_Income",
             barmode='group',
             color_discrete_sequence=['#003f5c', '#58508d', '#bc5090', '#ff6361', '#ffa600'],
             title="Histogram: Output (Buy again) color-encoded by Monthly income")

"""
A scatter plot is a chart type that is normally used to observe and visually display the 
relationship between variables. The values of the variables are represented by dots.
"""
chart4 = px.scatter(data_frame=df,
           x="Medium",
           y="Family_size",
           color="Buy_again",
           size=[1.0]*388,
           color_discrete_sequence=["#58508d", "#bc5090"],
           title="Scatter Plot: Medium vs Family size color-encoded by Output")

chart5 = px.histogram(data_frame=df,
             x="Buy_again",
             color="Occupation",
             barmode='group',
             color_discrete_sequence=['#003f5c', '#58508d', '#bc5090', '#ff6361'],
             title="Histogram: Output (Buy again) color-encoded by Occupation")

labels = ['Married', 'Prefer not to say', 'Single']
res2 = df.groupby(['Marital_Status', 'Buy_again']).size().reset_index().pivot(columns='Marital_Status', index='Buy_again', values=0)
print(res2)
one2 = res2.iloc[0, :].tolist()
two2 = res2.iloc[1, :].tolist()
colors2 = ['#003f5c', '#58508d', '#bc5090']
print(one2)
print(two2)

fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
fig.add_trace(go.Pie(labels=labels, values=two2, name="Yes"), 1, 1)
fig.add_trace(go.Pie(labels=labels, values=one2, name="No"), 1, 2)
fig.update_traces(hole=.4, hoverinfo="label+percent+name", marker=dict(colors=colors2))
chart6 = fig.update_layout(title_text="Pie Chart: Marital status by Output (Buy again)",
    annotations=[dict(text='Yes', x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text='No', x=0.82, y=0.5, font_size=20, showarrow=False)])

# External CSS file for styling the dashboard
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initializing a dash application
app = Dash(__name__, external_stylesheets=external_stylesheets)

graph1 = dcc.Graph(
        id='graph1',
        figure=chart1,
        className="six columns"
    )

graph2 = dcc.Graph(
        id='graph2',
        figure=chart2,
        className="six columns"
    )

graph3 = dcc.Graph(
        id='graph3',
        figure=chart3,
        className="six columns"
    )

graph4 = dcc.Graph(
        id='graph4',
        figure=chart4,
        className="six columns"
    )

graph5 = dcc.Graph(
        id='graph5',
        figure=chart5,
        className="six columns"
    )

graph6 = dcc.Graph(
        id='graph6',
        figure=chart6,
        className="six columns"
    )

# Heading for Dashboard
header = html.H2(children="Online Food Delivery Preferences Dataset Analysis", style={
    "width": "100%",
    "height": "45px",
    "border-style": "solid",
    "border-color": "#f4abba",
    "background-color": "#f4abba"
})
intro = html.Div(children="The dashboard analyses a survey conducted to answer the question about why there has been a rise in the demand of online food delivery in the metropolitan cities such as Bangalore. "
                          "The dataset has the following columns: Age, Gender, Marital_Status, Occupation, Monthly_Income, Educational_Qualifications, Family_size, Medium, Meal, Preference, Buy_again. ",
                 style={"textAlign": "center", "color": "#003f5c"})
br = html.Br()

# Creating rows in the dashboard
# Each row contains 2 graphs
row1 = html.Div(children=[graph1, graph3])
row2 = html.Div(children=[graph2, graph4])
row3 = html.Div(children=[graph5, graph6])

footer = html.Footer(children=["Name: Mahek Khowala || Roll Number: 101903567 || Group: 3CO22"],style={"textAlign": "center"})

layout = html.Div(children=[header, intro, br, row1, row2, row3, footer], style={"text-align": "center"})
app.layout = layout

# Running the dashboard application on the local browser
# Dash will run on http://127.0.0.1:8050/
if __name__ == "__main__":
    app.run_server(debug=True)