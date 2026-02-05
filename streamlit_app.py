import streamlit as st
import pandas as pd
import datetime
import numpy as np
# import matplotlib.pyplot as plt
from io import StringIO
# import statistics Library
import statistics
from openpyxl import load_workbook
# import xlsxwriter
# from openpyxl.utils.dataframe import dataframe_to_rows

# 0:"Palmon"
# 1:"TCD"
# 2:"Details"
# 3:"Tableaux"
# 4:"Tests"
# 5:"CSV tableaux"
# ?:"Valeurs"

uploaded_file  = st.file_uploader("Choose a file", type = 'xlsx')
excel_loaded=False

# ======================================================================================================
# Définitions DataFrame et Excel
cols_data = ['Name','Type','Skill','Level','Step','Stars','Stock','Star 1','Star 2','Star 3','Star 4','Star 5','Comp 1','Comp 2','Comp 3','Comp 4','Comp 5','Achievement','Needs','Cost to max','Upgradable','RankPower','Rank','Team','URL','URL Mutation','Mutation 1','Mutation 2']
cols_exp = ['Level from', 'Level to', 'Cost']
cols_comp = ['Level from', 'Cost']
cols_mut = ['Level', 'Step', 'Substep', 'Cost level']
cols_mut_full = ['Cost type', 'Cost']

df_xls = pd.DataFrame(
    {
       #"Sample":          ["Worksheet", "DisplayName",     "Range", "SkipRows", "UpToRow", "DisplayColumns"],
        "Palmons":         ["Palmon",    "Palmons",         "B:N",    1,         40,         cols_data ],
        "EXP":             ["Tableaux",  "Update costs",    "A:C",    1,         302,        cols_exp ],
        "Competencies":    ["Tableaux",  "Competencies",    "H:I",    1,         31,         cols_comp ],
        "Mutation":        ["Tableaux",  "Mutation costs",  "N:Q",    1,         224,        cols_mut ],
        "MaxCosts":        ["Valeurs",   "Valeurs Réf.",    "A:B",    0,         5,          cols_mut_full ],
    },
    index=["Worksheet", "DisplayName", "Range", "SkipRows", "UpToRow", "DisplayColumns"]
)

df_costs_exp=None
xls_exp_cols='A:C'
xls_exp_rows=302

df_costs_comp=None
xls_comp_cols='H:I'
xls_comp_rows=31

df_costs_mut=None
xls_mut_cols='N:Q'
xls_mut_rows=224

df_pal_data=None
xls_data_cols='B:N'
xls_data_rows=40

df_costs_mut_full=None
xls_mut_full_cols='A:B'
xls_mut_full_rows=5
# ======================================================================================================

def write_js_script():
    js_script="""
        <script language=javascript>alert('Hello workd');</script>
    """
    st.markdown(js_script, unsafe_allow_html=True)

def get_data_from_excel(xls_file,xls_sheet,skip,rng_cols,rng_rows,rencols=None):
    try:
        df = pd.read_excel(
            io=xls_file,
            engine="openpyxl",
            sheet_name=xls_sheet,
            skiprows=int(skip),
            usecols=str(rng_cols),
            nrows=int(rng_rows),
        )
        if rencols is not None:
            try:
                df.columns = rencols
            except:
                df=df
        with st.expander(xls_sheet, expanded=False, icon=':material/table_view:', width='stretch'):
            st.dataframe(df)
    except:
        df = None
    #df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df_xls
for row in df_xls.itertuples(name="Workbook"):
    #"Worksheet", "DisplayName", "Range", "SkipRows", "UpToRow", "DisplayColumns"
    st.write(row.Index,row[0]) #,row.Range,row.SkipRows,row.UpToRow,row.DisplayColumns)
#df_test=get_data_from_excel(uploaded_file,"Valeurs",0,xls_mut_full_cols,xls_mut_full_rows,cols_mut_full)

if uploaded_file is not None:
    file = pd.ExcelFile(uploaded_file)
    if file is not None:
        option = st.selectbox(
            "Worksheet to open",
            file.sheet_names,
            index=None,
            placeholder="Select Worksheet...",
        )
        if option is not None:
            if option == "Tableaux":
                df1 = pd.read_excel(file, sheet_name=option, skiprows=[0], header=[0], decimal =',')
            else:
                df1 = pd.read_excel(file, sheet_name=option, skiprows=[0], header=[0], decimal =',')
            st.dataframe(df1)
            excel_loaded=True
    else:
        excel_loaded=False
    

    #                get_data_from_excel(    xls_file,    xls_sheet,    skip,    rng_cols,    rng_rows,    rencols=None)
    df_pal_data=get_data_from_excel(uploaded_file,"Palmon",1,xls_data_cols,xls_data_rows,cols_data)
    df_costs_exp=get_data_from_excel(uploaded_file,"Tableaux",1,xls_exp_cols,xls_exp_rows,cols_exp)
    df_costs_comp=get_data_from_excel(uploaded_file,"Tableaux",1,xls_comp_cols,xls_comp_rows,cols_comp)
    df_costs_mut=get_data_from_excel(uploaded_file,"Tableaux",1,xls_mut_cols,xls_mut_rows,cols_mut)
    df_costs_mut_full=get_data_from_excel(uploaded_file,"Valeurs",0,xls_mut_full_cols,xls_mut_full_rows,cols_mut_full)
    
    # st.dataframe(df_pal_data)
    # st.dataframe(df_costs_exp)
    # st.dataframe(df_costs_comp)
    # st.dataframe(df_costs_mut)
    # st.dataframe(df_costs_mut_full)

    

# ---- HIDE STREAMLIT STYLE ----
#hide_st_style = """
#            <style>
#            #MainMenu {visibility: hidden;}
#            footer {visibility: hidden;}
#            header {visibility: hidden;}
#            </style>
#            """
#st.markdown(hide_st_style, unsafe_allow_html=True)
write_js_script()
js_script = """
    </div><script language='javascript'>alert('Hello world');</script><div>
    """
st.markdown(js_script, unsafe_allow_html=True)

    #df2 = pd.read_excel(uploaded_file, sheet_name='Statistik')
    #st.dataframe(df2)

    #df3 = pd.read_excel(uploaded_file, sheet_name='Probe 1', header = [0, 1, 2], decimal =',')
    #st.dataframe(df3)
    #probe1Max = df3[df3.columns[0]].max()
    #st.write('Maximalwert Probe 1: ' + str(round(probe1Max, 2)))
    #probe1Min = df3.iloc[-1, 0]
    #st.write('Minimalwert Probe 1: ' + str(round(probe1Min, 2)))


    #df4 = pd.read_excel(uploaded_file, sheet_name='Probe 2', header = [0, 1, 2], converters={0:float})
    #st.dataframe(df4)
    #probe2Max = df4[df4.columns[0]].max()
    #st.write('Maximalwert Probe 2: ' + str(round(probe2Max, 2)))
    #probe2Min = df4.iloc[-1, 0]
    #st.write('Minimalwert Probe 2: ' + str(round(probe2Min, 2)))

    #st.write("""---""")
    #st.write('Maximalwert Probe 1: ' + str(round(probe1Max, 4)))
    #st.write('Minimalwert Probe 1: ' + str(round(probe1Min, 4)))
    #st.write('Maximalwert Probe 2: ' + str(round(probe2Max, 4)))
    #st.write('Minimalwert Probe 2: ' + str(round(probe1Min, 4)))

    #mittelwertMax = statistics.mean([probe1Max, probe2Max])
    #mittelwertMin = statistics.mean([probe1Min, probe2Min])
    #st.write('Spannung Beginn: ' + str(round(mittelwertMax, 4)))
    #st.write('Spannung Ende: ' + str(round(mittelwertMin, 4)))

    #stdevMax = statistics.stdev([probe1Max, probe2Max])
    #stdevMin = statistics.stdev([probe1Min, probe2Min])
    #st.write('STABW Beginn: ' + str(round(stdevMax, 4)))
    #st.write('STABW Ende: ' + str(round(stdevMin, 4)))

    #sigmaRelProbe1 = (probe1Min / probe1Max)
    #sigmaRelProbe2 = (probe2Min / probe2Max)
    #st.write('rel Spannung Probe 1: ' + str(round(sigmaRelProbe1, 4)))
    #st.write('rel Spannung Probe 2: ' + str(round(sigmaRelProbe2, 4)))

    #mittelwertSigmaRel = statistics.mean([sigmaRelProbe1, sigmaRelProbe2])
    #st.write('rel Spannung Versuchsende: ' + str(round(mittelwertSigmaRel * 100, 4)))

    #stdevSigmaRel = statistics.stdev([sigmaRelProbe1, sigmaRelProbe2])
    #st.write('STABW rel Spannung Versuchsende: ' + str(round(stdevSigmaRel, 4)))

    #df5 = pd.DataFrame([{'Spannung Beginn':mittelwertMax, 'STABW Beginn': stdevMax, 'Spannung Ende': mittelwertMin, 'STABW Ende': stdevMin, 'rel. Spannung Versuchsende': mittelwertSigmaRel * 100, 'rel. Spannung STABW': stdevSigmaRel}])
    #st.dataframe(df5)

