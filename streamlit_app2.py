import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
#from streamlit.components.v1 import html
from streamlit_javascript import st_javascript
#import extra_streamlit_components as stx
# https://gist.github.com/asehmi/160109597bca79f7498d0f24d1adaae6

st.set_page_config(page_title="Excel v2", page_icon="🗃")
st.title("Excel v2")
uploaded_file = st.file_uploader("Choose a file", type = 'xlsx')
#file = pd.ExcelFile("myfile.xlsx")

i=0
st.session_state.selectedtab=0
st.session_state.tabs=None

my_js = """
function getCurrentTab(){
	var tabid = -1;
    try {
    	var tabobjs=document.getElementsByTagName('button');
        for (let i = 0; i < getLength(tabobjs); i++) {
        	if(tabobjs[i].ariaSelected=='true'){
                tabid=tabobjs[i].id.split('-')[3];
			}
        }
		alert(tabid);
	} catch (e) {tabid=-1;}
	window.parent.postMessage(tabid, '*');
	return tabid;
}
function getLength(o){try {return o.length;}catch(e){return 0;}}
"""

my_js2 = """
<script type='text/javascript'>
function getCurrentTab(){
	var tabid = -1;
    try {
    	var tabobjs=document.getElementsByTagName('button');
        for (let i = 0; i < getLength(tabobjs); i++) {
        	if(tabobjs[i].ariaSelected=='true'){
                tabid=tabobjs[i].id.split('-')[3];
			}
        }
		alert(tabid);
	} catch (e) {tabid=-1;}
	window.parent.postMessage(tabid, '*');
	return tabid;
}
function getLength(o){try {return o.length;}catch(e){return 0;}}
</script>
"""
def func_empty():
  return st.empty()

my_html = f"<script type='text/javascript'>{my_js}</script>"
components.html(my_html)
components.html("<div>Hello world</div>")
components.html(f"<table><tr><td><pre>{my_js}</pre></td></tr></table>")

if uploaded_file is not None:
  df1 = pd.read_excel(uploaded_file, sheet_name='Tableaux', decimal =',')
  st.dataframe(df1)

if uploaded_file is not None:
  file = pd.ExcelFile(uploaded_file)
  tabs = st.tabs(file.sheet_names, width="stretch", default=None)
  st.session_state["tabs"] = file.sheet_names
  file.sheet_names
  if "tabs" not in st.session_state:
    st.session_state["tabs"] = file.sheet_names
    #tabs = st.tabs(st.session_state["tabs"])

if st.session_state["tabs"] is not None: 
  #st.session_state["chosen_id"]
  return_value = st_javascript("(function(){ getCurrentTab(); })()")
  st.session_state.selectedtab=return_value
  #st.session_state.selectedtab=st_javascript("""getCurrentTab();""")
	
  #nbtabs = len(st.session_state["tabs"])
  nbtabs = len(tabs)
  i=0
  
  st.write(st.session_state.selectedtab)
	
  for tabx in tabs:
    if i != st.session_state.selectedtab:
      with tabs[i]:
        func_empty
    else:
      with tabs[i]:
        st.write(tabs[i])
        #df_xls = pd.read_excel(uploaded_file, sheet_name='Tableaux', decimal =',')
        #st.dataframe(df_xls)
    i=i+1

# st.experimental_rerun()
