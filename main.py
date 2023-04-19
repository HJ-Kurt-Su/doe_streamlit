import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import pyDOE2
import numpy as np
import io
# from plotly.subplots import make_subplots

# from IPython.display import display,HTML


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

# @st.cache_data
# def convert_df(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv().encode('utf-8')


def lv_doe_table(df, df_fac):
  # Target: change doe code table to factor real upper & lower level 
  # Input: doe code table with dataframe type
  # 
  df.columns = df_fac.columns
  df_resp = df.copy()
  # df_resp.columns = df_raw.columns

  for i in df.columns:

    resp_sfac_max = df[i].max()
    resp_sfac_min = df[i].min()

    low_lv = df_fac[i][0]
    hi_lv = df_fac[i][1]

    doe_code = [resp_sfac_min, resp_sfac_max]
    true_range = df_fac[i]

    x_range = df[i].sort_values(ascending=True)
    x_range = x_range.unique()[1:-1]
    for j in x_range:

      tmp_lv = np.interp(j, doe_code, true_range)
      df_resp[i].replace({j:tmp_lv}, inplace=True)
      
    df_resp[i].replace({resp_sfac_min:low_lv, resp_sfac_max:hi_lv}, inplace=True)
  
  return df_resp




st.title('DoE (Design of Experiment) Tool')



factor_ex_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRt_gecFPJZUw3MmI16zI042Z_RaeWj7w-Fs07wLaj-qKymK_K_XwRx-G09IcrqHmHhUQqP8-Qe0cQQ/pub?gid=0&single=true&output=csv"
# st.write("Factor Format Example File [link](%s)" % factor_ex_url)
st.markdown("#### Factor Format Example File [link](%s)" % factor_ex_url)

uploaded_csv = st.file_uploader('#### 選擇您要上傳的CSV檔')

if uploaded_csv is not None:
    df_fac = pd.read_csv(uploaded_csv, encoding="utf-8")
    st.header('您所上傳的CSV檔內容：')
    st.dataframe(df_fac)
    fac_n = df_fac.shape[1]

    doe_type = st.selectbox(
    'Choose DoE Type:',
    ("2 lv full", "response surface", "taguchi", "gsd", "latin-hypercube"))

    st.write('You selected:', doe_type)

    if doe_type == "response surface":

        doe_rs_array = pyDOE2.ccdesign(fac_n)
        df_code = pd.DataFrame(doe_rs_array)


    df_resp = lv_doe_table(df_code, df_fac)
    df_resp
        
    # df = pd.read_csv("idc_nb_tidy.csv", encoding="utf-8")  
    fig_pair = px.scatter_matrix(df_resp, dimensions=df_resp.columns,  
                             width=640, height=480)
    
    fig_pair.update_traces(diagonal_visible=False, showupperhalf=False,)
    st.plotly_chart(fig_pair, use_container_width=True)

    mybuff = io.StringIO()
    fig_file_name = doe_type + "_pair-plot-test.html"
    fig_html = fig_pair.write_html(fig_file_name)
    fig_pair.write_html(mybuff, include_plotlyjs='cdn')
    html_bytes = mybuff.getvalue().encode()
    

    csv = convert_df(df_resp)
    doe_table = doe_type + "_doe-table.csv"
    st.download_button(label='Download data as CSV', 
                       data=csv, 
                       file_name=doe_table,
                       mime='text/csv')

    st.download_button(label="download figure",
                               data=html_bytes,
                               file_name=fig_file_name,
                               mime='text/html'
                               )