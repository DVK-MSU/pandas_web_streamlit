import pandas as pd
import streamlit as st
import numpy as np
import streamlit.web.cli as stcli
import time
import re
from re import search
import sys
st.title(':panda_face: _Interactive Web Pandas_ 	')

from io import StringIO

col1, col2 = st.columns(2)

options=[]

with col1:
    
    st.header('Uploading file', divider='violet')
    uploaded_file = st.file_uploader("Choose a file on disc")
    
    try:
        uploaded_file_name = uploaded_file.name
    except AttributeError:
        uploaded_file_name = ''
    
    if search('.csv', uploaded_file_name):
        st.write('<font color="#00FF00">Uploaded file has format .csv</font>', unsafe_allow_html=True)
        sep_csv = st.text_input(label='Input a csv-separator: ', value=',')
    elif search('.xlsx', uploaded_file_name):
        st.write('<font color="#00FF00">Uploaded file has format .xlsx</font>', unsafe_allow_html=True)
        sep_csv=';'
    elif search('.xls', uploaded_file_name):
        st.write('<font color="#00FF00">Uploaded file has format .xls</font>', unsafe_allow_html=True)
        sep_csv=';'
    
    elif uploaded_file_name == '':
        sys.exit()
    else:
        st.write('<font color = "#FA8072">Not found format</font>', unsafe_allow_html=True)
        sep_csv=';'

    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file, sep=sep_csv)
        except UnicodeDecodeError:
            try:
                df_upload = pd.read_excel(uploaded_file)
            except NameError:
                sys.exit()
            except ValueError:
                sys.exit()
            except ImportError:
                sys.exit()               
    else:
        pass  
        

with col2:
    
    if uploaded_file is not None:
        st.header('Select columns', divider='violet')
        options = st.multiselect('Select columns:', df_upload.columns, placeholder='Click me to select columns')

if uploaded_file is not None:
    progress_text = "Selecting in process"
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.005)
        my_bar.progress(percent_complete + 1, text=progress_text)



if uploaded_file is not None:
    if options != []:       
        df_selected_cols = df_upload[options]
        st.write(df_selected_cols)
        
    elif options == []:
        options=df_upload.columns 
        df_selected_cols = df_upload[options]
        df_len = len(df_selected_cols)
        slider_value = st.slider(min_value=0, max_value=df_len, label='Len of DataFrame', value=10)
        st.write(df_selected_cols.head(slider_value))
    col3, col4 = st.columns(2)
    

    with col3:
        types_data_toogle = st.toggle('Show types of data')
        if types_data_toogle:
            st.write('<font color = "#00FF00">Types of data in columns:</font>', unsafe_allow_html=True)
            # st.header('', divider='violet')
            st.text(f'{df_selected_cols.dtypes}')

    with col4:
        subcol_1, subcol_2 = st.columns(2)
        
        unique_values_toogle = st.toggle('Show unique values')
        hists_on = st.toggle('Switch on histograms')
        if (hists_on and unique_values_toogle):
            color_hist = st.color_picker('Select color for histograms', value='#00FF00')
        if unique_values_toogle:
            st.write('<font color = "#00FF00">Unique values in column:</font>', unsafe_allow_html=True)
        
            for i in df_selected_cols.columns: 
                
                hist_dev = pd.DataFrame(df_selected_cols[i].value_counts())
                
                st.write(hist_dev)
                if hists_on:
                    
                    st.bar_chart(hist_dev, color=color_hist)






