import io
import streamlit as st
import plotly.io as pio
import numpy as np
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout='wide')
#=========================================================================================

df = pd.read_csv('india.csv')
# ==================================fecth the state data from dataframe============================
list_of_states = list(df['State'].unique())
list_of_states.insert(0,'Overall India')

# ==============================fecth the district wise data from dataframe===========================
district_list=list(df["District"].unique())

# Page 1: Data Visualization
def page_data_viz():
    st.title('State-by-State Comparison')

    # Select primary and secondary parameters
    primary = st.selectbox('Select Primary Parameter',df.columns[6:])
    secondary = st.selectbox('Select Secondary Parameter', df.columns[6:])

    # Create a bar chart to show the primary parameter for all states
    fig1 = px.bar(df, x='State', y=primary, height=600)
    fig1.update_layout(xaxis={'categoryorder': 'total descending'})
    st.plotly_chart(fig1, use_container_width=True)


    # Create a scatter plot to show the secondary parameter vs. primary parameter for all states
    fig2 = px.scatter(df, x=primary, y=secondary, color='State', hover_name='District', height=600)
    st.plotly_chart(fig2, use_container_width=True)

    # Export data
    if st.button('Export Data'):
        # Assign value to data variable
        data = pd.DataFrame(df)
        csv = data.to_csv(index=False)
        # Create a download button to download the CSV data
        st.download_button(
            label="Download Data",
            data=csv,
            file_name='data.csv',
            mime='text/csv'
        )

    # Export chart
    if st.button('Export Chart'):
        with st.spinner('Exporting chart...'):
            # Save chart as a BytesIO object
            img_bytes = io.BytesIO()
            pio.write_image(fig1, img_bytes, format='png')

            # Download chart as a file
            st.download_button(
                label='Download Chart',
                data=img_bytes.getvalue(),
                file_name='chart.png',
                mime='image/png'
            )
            st.success('Chart exported successfully.')


#================================================================================================================

def data_visualization():

    st.sidebar.title('Data Visualization about Cencus')

    selected_state = st.sidebar.selectbox('Select a state', list_of_states)
    primary = st.sidebar.selectbox('Select Primary Parameter', sorted(df.columns[5:]))
    secondary = st.sidebar.selectbox('Select Secondary Parameter', sorted(df.columns[5:]))

    plot = st.sidebar.button('Plot Graph')

    if plot:

        st.text('Size represent primary parameter')
        st.text('Color represents secondary parameter')
        if selected_state == 'Overall India':
            # plot for india
            fig1 = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", size=primary, color=secondary, zoom=4,
                                    size_max=35,
                                    mapbox_style="carto-positron", width=1200, height=700, hover_name='District')

            st.plotly_chart(fig1, use_container_width=True)
        else:
            # plot for state
            state_df = df[df['State'] == selected_state]

            fig1 = px.scatter_mapbox(state_df, lat="Latitude", lon="Longitude", size=primary, color=secondary, zoom=6,
                                    size_max=35,
                                    mapbox_style="carto-positron", width=1200, height=700, hover_name='District')

            st.plotly_chart(fig1, use_container_width=True)


    # Export data
    if st.button('Export Data'):
        # Assign value to data variable
        data = pd.DataFrame(df)
        csv = data.to_csv(index=False)
        # Create a download button to download the CSV data
        st.download_button(
            label="Download Data",
            data=csv,
            file_name='data.csv',
            mime='text/csv'
        )

#================================================================================================================





def district_wise():
    states = sorted(df["State"].unique())
    selected_state = st.selectbox("Select a state", states)

    primary = st.sidebar.selectbox('Select Primary Parameter', df.columns[6:])
    #secondary = st.sidebar.selectbox('Select Secondary Parameter', sorted(df.columns))

    if selected_state:
        district_data = df[df["State"]==selected_state].groupby("District").agg({primary: "sum"}).reset_index()
        fig = px.bar(district_data, x="District", y=primary, height=600)
        fig.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig, use_container_width=True)


    # Export data
    if st.button('Export Data'):
        # Assign value to data variable
        data = pd.DataFrame(df)
        csv = data.to_csv(index=False)
        # Create a download button to download the CSV data
        st.download_button(
            label="Download Data",
            data=csv,
            file_name='data.csv',
            mime='text/csv'
        )

    # Export chart
    if st.button('Export Chart'):
        with st.spinner('Exporting chart...'):
            # Save chart as a BytesIO object
            img_bytes = io.BytesIO()
            pio.write_image(fig, img_bytes, format='png')

            # Download chart as a file
            st.download_button(
                label='Download Chart',
                data=img_bytes.getvalue(),
                file_name='chart.png',
                mime='image/png'
            )
            st.success('Chart exported successfully.')

    # Create a scatter plot to show the secondary parameter vs. primary parameter for all states
    #-fig2 = px.scatter(df, x=primary, y=secondary, color='State', hover_name='District', height=600)
    #-st.plotly_chart(fig2, use_container_width=True)

#================================================================================================================


def page_about():
    # Title
    st.title('About this Project')

    # Introduction paragraph
    st.write(''' This web application that displays data from the Indian Census, allowing users to visualize various demographic and socio-economic indicators across different states and districts. The app is built using Streamlit and Plotly, and uses data processing libraries like Pandas and NumPy.
The app provides various visualization options, including scatter plots and scatter_mapbox, to help users gain insights into the data. Users can compare different states based on primary and secondary parameters selected from a dropdown menu. The results are displayed in a bar chart and scatter plot for easy comparison.
The project was developed by Me of data enthusiasts with a passion for building interactive data visualizations.
               ''')

    # Subheadings
    st.header('Features')

    st.subheader('Data Visualization')
    st.write('The app provides various visualization options, including scatter plots and scatter_mapbox, to help users gain insights into the data.')

    st.subheader('State-by-State Comparison')
    st.write('Users can compare different states based on primary and secondary parameters selected from a dropdown menu. The results are displayed in a bar chart and scatter plot for easy comparison.')

    st.subheader('District Analysis')
    st.write('Users can selected paramisters from a dropdown menu. The results are displayed in a bar chart and scatter plot for easy comparison.')



#Second project

# Create multi-page app
pages = {
    'About_project':page_about,
    'Data Visualization📶': data_visualization,
    'State-by-State Comparison 🌍': page_data_viz,
    'District_wise🗺️':district_wise
}

st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', list(pages.keys()))

# Display the selected page
pages[page]()
# The aim of this project is to create a web application that allows users to visualize various
# demographic and socio-economic indicators across different states and districts in India.--------------------
#The app will provide various visualization options, including scatter plots and scatter_mapbox,
# to help users gain insights into the data. Users can compare different states based on primary and secondary parameters selected from a dropdown menu.
# The results will be displayed in a bar chart and scatter plot for easy comparison.