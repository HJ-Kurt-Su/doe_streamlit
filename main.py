import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import pyDOE2

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


st.title('DoE (Design of Experiment) Tool')



factor_ex_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRt_gecFPJZUw3MmI16zI042Z_RaeWj7w-Fs07wLaj-qKymK_K_XwRx-G09IcrqHmHhUQqP8-Qe0cQQ/pub?gid=0&single=true&output=csv"
# st.write("Factor Format Example File [link](%s)" % factor_ex_url)
st.markdown("#### Factor Format Example File [link](%s)" % factor_ex_url)

uploaded_csv = st.file_uploader('#### 選擇您要上傳的CSV檔')

if uploaded_csv is not None:
    df = pd.read_csv(uploaded_csv, encoding="utf-8")
    st.header('您所上傳的CSV檔內容：')
    st.dataframe(df)
    fac_n = df.shape[1]

    doe_type = st.selectbox(
    'Choose DoE Type:',
    ("2 lv full", "response surface", "taguchi", "gsd", "latin-hypercube"))

    st.write('You selected:', doe_type)

    if doe_type == "response surface":

        doe_rs_array = pyDOE2.ccdesign(fac_n)
        df_code = pd.DataFrame(doe_rs_array)
        df_code
    # df = pd.read_csv("idc_nb_tidy.csv", encoding="utf-8")

    csv = convert_df(df)
    st.download_button('Download data as CSV', data=csv, file_name='large_df.csv',
    mime='text/csv')