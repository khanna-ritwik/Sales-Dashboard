import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sklearn import preprocessing

st.set_page_config(page_title="Sales Overview",
                   page_icon=":memo:", layout="wide")

# Reading csv file


def get_data_from_excel():
    df = pd.read_csv('supermarket_sales.csv', index_col=False)
    return df


df = get_data_from_excel()

# Implementing sidebar
st.sidebar.header("Please Filter Here:")

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),  # options shown in sidebar categories
    # shows the default categories for which data is to be displayed
    default=df["Gender"].unique()
)

city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

payment = st.sidebar.multiselect(
    "Select the Payment Type:",
    options=df["Payment"].unique(),
    default=df["Payment"].unique()
)

product_line = st.sidebar.multiselect(
    "Select the Product Line:",
    options=df["Product_line"].unique(),
    default=df["Product_line"].unique()
)

# Selection of data to be displayed on the dashboard
# initially calculations are shown considering all the data
df_selection = df.query(
    "Gender == @gender & City == @city & Customer_type == @customer_type & Payment == @payment & Product_line == @product_line"
)

# HomePage of the dashboard
st.title(":bar_chart: Sales Overview")
st.markdown("##")

total_sales = int(df_selection["Total"].sum())
total_quantity_sold = int(df_selection["Quantity"].sum())
average_rating = round(df_selection['Rating'].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sale:")
    st.subheader(f" ₹ {total_sales}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Total Quantity Sold:")
    st.subheader(f"{total_quantity_sold} units")

st.markdown("---")

# Pie chart to get the distribution of different product lines in the data
a = df.groupby('Product_line').sum('Quantity')
labels = a.index
values = a['Quantity']
colors = ['lightcoral', 'gold', 'yellowgreen',
          'lightskyblue', 'violet', 'grey']
pie_product_line = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                          insidetextorientation='radial'
                                          )])
pie_product_line.update_traces(hoverinfo='label+percent', textfont_size=10,
                               marker=dict(colors=colors, line=dict(color='#000000', width=0.5)))

# Pie chart to get the distribution of different payment modes in the data
b = df.groupby('Payment').count()
labels = b.index
# label_encoder = preprocessing.LabelEncoder()
# # Encode labels in column 'payment'
# df['Payment'] = label_encoder.fit_transform(df['Payment'])
# df['Payment'].unique()
values = b['Branch']
colors = ['gold', 'yellowgreen', 'lightskyblue']
pie_payment = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                     insidetextorientation='radial'
                                     )])
pie_payment.update_traces(hoverinfo='label+percent', textfont_size=10,
                          marker=dict(colors=colors, line=dict(color='#000000', width=0.5)))

# Line graph to display frequency of each quantity
c = (
    df_selection.groupby(by=["Quantity"]).count()
)
fig_line = px.line(c, x=c.index, y="Total",
                   title="Line Graph showing frequency of each quantity")
fig_line.update_layout(
    plot_bgcolor="#FFF59E",
)

# Vertical Bar Graph for Sales in each city
sale_by_city = (
    df_selection.groupby(by=["City"]).count()
)
fig_barv = px.bar(
    sale_by_city,
    x=sale_by_city.index,
    y="Branch",
    title="<b>Invoice generated in each city</b>",
    color_discrete_sequence=["#FFCC00"],
    template="plotly_white",
)
fig_barv.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

# Horizontal Bar Graph for Sales by each product
sales_by_product = (
    df_selection.groupby(by=["Product_line"]).sum()[
        ["Total"]].sort_values(by="Total")
)
fig_barh = px.bar(
    sales_by_product,
    x="Total",
    y=sales_by_product.index,
    orientation="h",
    title="<b>Sale by Product</b>",
    color_discrete_sequence=["#FC6A03"],
    template="plotly_white",
)
fig_barh.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(pie_product_line, use_container_width=True)
right_column.plotly_chart(pie_payment, use_container_width=True)

st.markdown("---")

left_column_2, right_column_2 = st.columns(2)
left_column_2.plotly_chart(fig_barv, use_container_width=True)
right_column_2.plotly_chart(fig_barh, use_container_width=True)

st.markdown("---")

left_column_3, right_column_3 = st.columns(2)
left_column_3.plotly_chart(fig_line, use_container_width=True)

# hiding the footer and other non useful components provided by default by streamlit
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
