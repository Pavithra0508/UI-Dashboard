import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='Customer review dashboard')
st.title('Customer review dashboard')
st.subheader('Use slider to see the review result based on the age')


### Load dataframe
excel_file = 'project.xlsx'
sheet_name = 'DATA'


df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='B:D',
                   header=3)

df_users = pd.read_excel(excel_file,
                         sheet_name = sheet_name,
                         usecols="G:H",
                         header=3)


#streamlit selection
devices = df["Devices"]. unique().tolist()
ages = df['Age'].unique().tolist()

age_selection = st.slider('Age:',
                          min_value=min(ages),
                          max_value=max(ages),
                          value=(min(ages),max(ages)))

devices_selection = st.multiselect('Devices:',
                                   devices,
                                   default=devices)

#filter dataframe based on selection
mask = (df['Age'].between(*age_selection)) & (df['Devices'].isin(devices_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available results:{number_of_result}*')


#group dataframe after selection
df_grouped = df[mask].groupby(by=['Users Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age':'Votes'})
df_grouped = df_grouped.reset_index()

#plot bar chart
bar_chart = px.bar(df_grouped,
                   x='Users Rating',
                   y='Votes',
                   text='Votes',
                   color_discrete_sequence=['#45B39D']*len(df_grouped),
                   template='plotly_white')
st.plotly_chart(bar_chart)

#display image & dataframe
col1, col2 = st.columns(2)
image = Image.open('images/firmbee-com-jrh5lAq-mIs-unsplash.jpg')
col1.image(image,
           use_container_width=True)
col2.dataframe(df[mask])

#plot pie chart

pie_chart = px.pie(df_users,
                   title='Total no. of Users',
                   values='Users',
                   names='Device')

st.plotly_chart(pie_chart)  

image = Image.open('images/firmbee-com-jrh5lAq-mIs-unsplash.jpg')
st.image(image,
         use_container_width=True)
