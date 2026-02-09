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
import locale

# ======================================================================================================
# Définitions DataFrame et Excel
cols_data = ['Name','Type','Skill','Level','Upgradable','Step','Stars','Stock','Star 1','Star 2','Star 3','Star 4','Star 5','Unused1','Comp 1','Comp 2','Comp 3','Comp 4','Comp 5','Achievement','Needs','Unused2','Cost to max','Unused3','Unused4','RankPower','Rank','Team','Unused5','URL','URL Mutation','Unused6','Unused7','Mutation 1','Mutation 2','Unused8']
cols_exp = ['Level from', 'Level to', 'Cost']
cols_comp = ['Level from', 'Cost']
cols_mut = ['Level', 'Step', 'Substep', 'Cost level']
cols_mut_full = ['Cost type', 'Cost']

df_pal_data=None
df_costs_exp=None
df_costs_comp=None
df_costs_mut=None
df_costs_mut_full=None

idx_palmon=0
idx_costs=1
idx_comp=2
idx_mut=3
idx_val=4

data = { #                    0                  1                  2                3                4
        "Worksheet":      ["Palmon_data",    "Tableaux",        "Tableaux",     "Tableaux",         "Valeurs"            ],
        "DisplayName":    ["Palmons",        "Upgrade costs",   "Competencies", "Mutation costs",   "Upgrade full costs"       ],
        "Range":          ["A:AJ",           "A:C",             "H:I",          "N:Q",              "A:B"                ],
        "SkipRows":       [1,                1,                 1,              1,                  0                    ],
        "UpToRow":        [41,               302,               31,             224,                5                    ],
        "DisplayColumns": [cols_data,        cols_exp,          cols_comp,      cols_mut,           cols_mut_full        ],
        "DataFrame":      [df_pal_data,      df_costs_exp,      df_costs_comp,  df_costs_mut,       df_costs_mut_full    ],
       }
df_xls = pd.DataFrame(data)
#df_xls
option_skill=["⚔ Attack","🛡 Defend"]
#option_type=["💧Water","🔥Fire","⚡Electricity","🪵Wood"]
data_type={
    "Type":["Water","Fire","Electricity","Wood"],
    "Icon":["💧","🔥","⚡","🪵"]
}
option_type=data_type['Icon']
df_data_type = pd.DataFrame(data_type)
# ======================================================================================================
#format="%d ⭐",
col_pct=st.column_config.NumberColumn(
        min_value=0,
        max_value=100,
        format="percent",
    )
column_config={
    "Name": st.column_config.TextColumn( "Name", pinned = True ),
    "Type": st.column_config.SelectboxColumn( "Type", pinned = True,options=option_type ),
    #"Type": st.column_config.TextColumn( "Type", pinned = True ),
    "Skill": st.column_config.SelectboxColumn( "Skill", pinned = True,options=option_skill ),
    #"Skill": st.column_config.TextColumn( "Skill", pinned = True ),
    "Level": st.column_config.ProgressColumn(
        "Level",
        help="Palmon level",
        format="%f",
        min_value=100,
        max_value=250,
        color="#006699"
    ),
    "Step": st.column_config.NumberColumn(
        "Step",
        min_value=0,
        max_value=5,
        format="%d ⭐",
    ),
    "Achievement": col_pct,
    "Cost to max": st.column_config.NumberColumn(
        "Cost to max",
        #format="localized",
        format="compact",
    ),
    "RankPower": st.column_config.NumberColumn(
        "RankPower",
        format="localized",
    ),
    "URL": st.column_config.ImageColumn(
        "Base preview",
        width="small"
    ),
    "URL Mutation": st.column_config.ImageColumn(
        "Mutation preview",
        width="small"
    ),
    "Comp 1": col_pct,
    "Comp 2": col_pct,
    "Comp 3": col_pct,
    "Comp 4": col_pct,
    "Comp 5": col_pct,
    "Unused1": None,
    "Unused2": None,
    "Unused3": None,
    "Unused4": None,
    "Unused5": None,
    "Unused6": None,
    "Unused7": None,
    "Unused8": None
}
# ======================================================================================================

def test_df_xls():
    columns = list(df_xls)
    for i in columns:
        cell1,cell2=st.columns(2)
        with cell1:
            st.write(i)
        with cell2:
            st.write(df_xls[i][2])

def write_js_script():
    js_script="""
        <script language=javascript>alert('Hello world');</script>
    """
    st.markdown(js_script, unsafe_allow_html=True)

def write_js_menu(): 
    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)    

def file_err():
   st.markdown(":orange-badge[⚠️ No file loaded]")
    
def get_data_from_excel(xls_file,xls_sheet,skip,rng_cols,rng_rows,rencols=None,show_table=False):
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
        if show_table == True:
            with st.expander(xls_sheet, expanded=False, icon=':material/table_view:', width='stretch'):
                st.dataframe(df)
    except:
        df = None
    return df

def get_data(file,idx,show_table=False):
    df_xls["DataFrame"][idx]=get_data_from_excel(
                                                xls_file=file,
                                                xls_sheet=df_xls["Worksheet"][idx],
                                                skip=df_xls["SkipRows"][idx],
                                                rng_cols=df_xls["Range"][idx],
                                                rng_rows=df_xls["UpToRow"][idx],
                                                rencols=df_xls["DisplayColumns"][idx],
                                                show_table=show_table
                                                )  

def large_num_format(value):
    locale.setlocale(locale.LC_ALL, "fr_FR")
    try:
        return locale.format_string("%.0f", int(value), grouping=True)
    except:
        return None

def build_chart_bar(df_chart,xField,yField,sLabel,selMin=1,selMax=30):
    if df_chart is not None:
        st.bar_chart(df_chart, x=xField, y=yField)
        sel_min=selMin
        sel_max=selMax
        range_level_min, range_level_max= st.slider(
            label=sLabel,
            min_value=sel_min,
            max_value=sel_max,
            value=(sel_min,sel_max),
            step=1
        )
        df = df_chart.loc[(df_chart[xField] >= int(range_level_min)) & (df_chart[xField] <= int(range_level_max))]
        total_col = f"Total cost from {range_level_min} to {range_level_max}"
        try:
            st.markdown(f":orange-badge[{total_col} : {large_num_format(int(df[yField].sum()))}]")
        except:
            st.markdown(f":orange-badge[{total_col} : {int(df[yField].sum())}]")
        excel_loaded=True

def build_table_any(df):
        st.dataframe(
            df,
            column_config={
               "Cost": st.column_config.NumberColumn(
                     "Costs",
                     min_value=0,
                     max_value=10000000,
                     step=1,
                     format="compact",
               )
            },
            hide_index=True,
         )    

def human_format(num, round_to=1):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num = round(num / 1000.0, round_to)
    return '{:.{}f}{}'.format(num, round_to, ['', 'K', 'M', 'B', 'G'][magnitude])
#df.style.format({"stars": human_format})

def build_table_full_costs(df_src):
    sel_options=[
        "📊 Data Exploration",
        f"📈 :material/thumb_up:",
        "🤖 LLM",
    ]
    st.markdown(':material/thumb_up:')
    df=df_src.copy()
    df['NewCol']=f":material/thumb_up:" #df['Cost type']
    df['NewCol']=df['Cost type'].apply(lambda b: sel_options[1] if b=='Level300' else sel_options[2])
    df['Cost type'] = df['Cost type'].replace('Level300', f':material/thumb_up: Dummy')
    st.dataframe(
            df,
            column_config={
                "Cost type": st.column_config.TextColumn(
                    "Cost type",
                ),                
                "Cost": st.column_config.NumberColumn(
                    "Costs",
                    min_value=0,
                    max_value=10000000,
                    step=1,
                    format="compact",
                ),
                "NewCol": st.column_config.SelectboxColumn(
                    "New column",
                    disabled=True,
                    options=sel_options
                ),
            },
            hide_index=True,
         )  

def format_stars(x): #⭐
    try:
        return f":star: * round(int(x),0)"
    except:
        return x

def calcul_upgrade_costs(from_lvl=1,to_lvl=300):
    if df_xls["DataFrame"][idx_palmon] is not None:
        df = df_xls["DataFrame"][idx_costs]
        val_cost=df.loc[(df["Level from"] >= from_lvl) & (df["Level from"] <= to_lvl)]["Cost"].sum()
        return val_cost
    else:
        return None

# ======================================================================================================
with st.expander("Excel file", expanded=True, width="stretch"):
    uploaded_file  = st.file_uploader("Choose a file", type = 'xlsx')
    excel_loaded=False
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
                    if option == "Palmon_data":
                        df1.columns = cols_data
                st.dataframe(df1)
                excel_loaded=True
        else:
            uploaded_file=None


if df_xls["DataFrame"][idx_costs] is not None:
    excel_loaded=True
else:
    excel_loaded=False

row, col = df_xls.shape
for i in range(row):
    get_data(uploaded_file,i,False)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
                            df_xls["DisplayName"][idx_costs],
                            df_xls["DisplayName"][idx_comp],
                            df_xls["DisplayName"][idx_mut],
                            df_xls["DisplayName"][idx_val],
                            df_xls["DisplayName"][idx_palmon]
                            ])
with tab1:
    if df_xls["DataFrame"][idx_palmon] is not None:
        df = df_xls["DataFrame"][idx_costs]
        df_pal=df_xls["DataFrame"][idx_palmon]
        st.header(df_xls["DisplayName"][idx_costs])
        
        st.markdown(f":orange-badge[Total : {int(calcul_upgrade_costs(240,259))}]")
        
        min_upg=df_pal.loc[(df_pal["Level"] >= 1)]["Level"].min()
        max_upg=df.loc[(df["Cost"] >= 1)]["Level from"].max()
        build_chart_bar(df_xls["DataFrame"][idx_costs],'Level from','Cost','Upgrade costs from level:',int(min_upg),int(max_upg))
        with st.expander("Data graph", expanded=False, width="stretch"):
            build_table_any(df_xls["DataFrame"][idx_costs])
    else:
        file_err()
with tab2:
    if df_xls["DataFrame"][idx_palmon] is not None:   
        st.header(df_xls["DisplayName"][idx_comp])
        build_chart_bar(df_xls["DataFrame"][idx_comp],'Level from','Cost','Competencies costs from level:',int(1),int(30))
        with st.expander("Data graph", expanded=False, width="stretch"):
            build_table_any(df_xls["DataFrame"][idx_comp])
    else:
        file_err()
with tab3:
    if df_xls["DataFrame"][idx_palmon] is not None:  
        st.header(df_xls["DisplayName"][idx_mut]) 
        build_chart_bar(df_xls["DataFrame"][idx_mut],'Level','Cost level','Mutation costs from level:',int(1),int(30))
        with st.expander("Data graph", expanded=False, width="stretch"):
            build_table_any(df_xls["DataFrame"][idx_mut])
    else:
        file_err()
with tab4:
    if df_xls["DataFrame"][idx_palmon] is not None:  
        st.header(df_xls["DisplayName"][idx_val]) 
        build_table_full_costs(df_xls["DataFrame"][idx_val])
    else:
        file_err()
with tab5:
    if df_xls["DataFrame"][idx_palmon] is not None:  
        st.header(df_xls["DisplayName"][idx_palmon])

        st.write(
            df_data_type.loc[(df_data_type['Type'] == 'Fire')]['Icon']
        )
        st.write(
            df_data_type.loc[(df_data_type['Type'] == 'Fire')]['Icon']
        )
        
        #df_xls["DataFrame"][idx_palmon].columns = cols_data
        
        #df_xls["DataFrame"][idx_palmon]['Type']=df_xls["DataFrame"][idx_palmon]['Type'].apply(lambda b: option_type[0] if b=='Fire' else option_type[1])
        #df_xls["DataFrame"][idx_palmon]['Type']=df_xls["DataFrame"][idx_palmon]['Type'].apply(lambda b: df_data_type.loc[(df_data_type['Type'] == b)]['Icon'])
        df_xls["DataFrame"][idx_palmon]['Type']=df_xls["DataFrame"][idx_palmon]['Type'].apply(lambda b: option_type[data_type['Type'].index(b)])
        
        df_xls["DataFrame"][idx_palmon]['Skill']=df_xls["DataFrame"][idx_palmon]['Skill'].apply(lambda b: option_skill[0] if b=='Attack' else option_skill[1])
        event = st.dataframe(
            df_xls["DataFrame"][idx_palmon],
            column_config=column_config,
            on_select="rerun",
            selection_mode="single-row",
            hide_index=True,
        )
        palmon = event.selection.rows
        filtered_df = df_xls["DataFrame"][idx_palmon].iloc[palmon]
        st.dataframe(
            filtered_df,
            column_config=column_config,
            hide_index=True,
        )
    else:
        file_err()





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

