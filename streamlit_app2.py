import streamlit as st
import pandas as pd

# https://gist.github.com/asehmi/160109597bca79f7498d0f24d1adaae6

st.set_page_config(page_title="Excel v2", page_icon="🗃")
st.title("Excel v2")
uploaded_file = st.file_uploader("Choose a file", type = 'xlsx')
#file = pd.ExcelFile("myfile.xlsx")

if uploaded_file is not None:
  df1 = pd.read_excel(uploaded_file, sheet_name='Tableaux', decimal =',')
  st.dataframe(df1)

if uploaded_file is not None:
  file = pd.ExcelFile(uploaded_file)
  chosen_id = st.tabs(file.sheet_names, width="stretch", default=None)
  file.sheet_names
  if "tabs" not in st.session_state:
    st.session_state["tabs"] = file.sheet_names
  if "chosen_id" not in st.session_state:
    st.session_state["chosen_id"] = chosen_id

if st.session_state["chosen_id"] is not None:
  st.session_state["chosen_id"] 

# st.experimental_rerun()
