import streamlit as st
import pandas as pd
import datetime
import numpy as np
from io import StringIO
import statistics
from openpyxl import load_workbook
import locale
import logging
import os
import platform
from flask import Flask
import requests
from user_agents import parse
import extra_streamlit_components as stx    #https://github.com/Mohamed-512/Extra-Streamlit-Components

# import matplotlib.pyplot as plt
# import statistics Library
# import xlsxwriter
# from openpyxl.utils.dataframe import dataframe_to_rows

st_logger = logging.getLogger('streamlit')
st_logger.setLevel(logging.WARNING)


# ======================================================================================================
# URL: https://testexcel-xwu5zapqqz8ukerpqqvxhu.streamlit.app/
# ======================================================================================================

# Définitions variables
df_xls = None
uploaded_file = None
excel_loaded=False
tabs_data=[]
tabs = None

#def init_session():
if 'df_data' not in st.session_state:
    st.session_state.df_data = df_xls
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = uploaded_file
if "excel_loaded" not in st.session_state:
    st.session_state.excel_loaded = False
if "tabs_data" not in st.session_state:
    st.session_state.tabs_data = tabs_data

# Définitions variables de sélection de dataframes
event = None
event_a = None
event_d = None

# Définitions DataFrame et Excel
#cols_data = ['Name','Type','Skill','Level','Upgradable','Step','Stars','Stock','Star 1','Star 2','Star 3','Star 4','Star 5','Unused1','Comp 1','Comp 2','Comp 3','Comp 4','Comp 5','Achievement','Needs','Unused2','Cost to max','Unused3','Unused4','RankPower','Rank','Team','Unused5','URL','URL Mutation','Unused6','Unused7','Mutation 1','Mutation 2','Unused8']
cols_data = ['Name','Type','Skill','Level','Upgradable','Step','Stars','Stock','Comp 1','Comp 2','Comp 3','Comp 4','Comp 5','Unused1','Star 1','Star 2','Star 3','Star 4','Star 5','Achievement','Needs','Unused2','Cost to max','Unused3','Unused4','RankPower','Rank','Team','Unused5','URL','URL Mutation','Unused6','Unused7','Mutation 1','Mutation 2','Unused8']
cols_exp = ['Level from', 'Level to', 'Cost']
cols_comp = ['Level from', 'Cost']
cols_mut = ['Level', 'Step', 'Substep', 'Cost level']
cols_mut_full = ['Cost type', 'Cost']
cols_stars = ['Stars level', 'Unit Cost', 'Total']

df_pal_data=None
df_costs_exp=None
df_costs_comp=None
df_costs_mut=None
df_costs_mut_full=None
df_costs_stars=None

idx_palmon=0
idx_costs=1
idx_comp=2
idx_mut=3
idx_val=4
idx_stars=5

data = { #                    0                  1                  2                    3                4                        5
        "Worksheet":      ["Palmon_data",    "Tableaux",        "Tableaux",         "Tableaux",         "Valeurs",                "Stars"        ],
        "DisplayName":    ["Palmons",        "Upgrade costs",   "Competencies",     "Mutation costs",   "Upgrade full costs",     "Stars"        ],
        "Range":          ["A:AJ",           "A:C",             "H:I",              "N:Q",              "A:B",                    "A:C"          ],
        "SkipRows":       [0,                1,                 1,                  1,                  0,                        0              ],
        "UpToRow":        [41,               302,               31,                 224,                5,                        7              ],
        "DisplayColumns": [cols_data,        cols_exp,          cols_comp,          cols_mut,           cols_mut_full,            cols_stars     ],
        "DataFrame":      [df_pal_data,      df_costs_exp,      df_costs_comp,      df_costs_mut,       df_costs_mut_full,        df_costs_stars ],
        "Description":    ["Full list",      "EXP per level",   "Any palmon type",  "UR only",          "Defined values",         "Omni UR costs"],
       }
df_xls = pd.DataFrame(data)
option_skill=["⚔ Attack","🛡 Defend"]
data_type={
    "Type":["Water","Fire","Electricity","Wood"],
    "Icon":["💧","🔥","⚡","🪵"]
}
data_values={
    "Value":["Energy","Crystals","Pieces","Level300"],
    "Icon":["🟢","💎","🧩","🔝"],
}
map_values={"Energy":"🟢Energy",
            "Crystals":"💎Crystals",
            "Pieces":"🧩Pieces",
            "Level300":"🔝Level300" }

option_type=data_type['Icon']
df_data_type = pd.DataFrame(data_type)
option_values=data_values['Icon']
df_data_values = pd.DataFrame(data_values)
# ======================================================================================================
#format="%d ⭐",
 
cols_palmon = ['Name','Type','Skill','Level','Upgradable','Step','Stars','Achievement','Needs','Cost to max']

col_pct=st.column_config.NumberColumn(
        min_value=0,
        max_value=100,
        format="percent",
    )
col_pct_1=st.column_config.NumberColumn(
        min_value=0,
        max_value=1,
        format="percent",
    )
def col_progress(mini=0,maxi=100,label="Level",tooltip="Palmon level",numformat="%f"):
    return st.column_config.ProgressColumn(
        label,
        help=tooltip,
        format=numformat,
        min_value=mini,
        max_value=maxi,
        color="#006699"
    )
column_config={
    "Name": st.column_config.TextColumn( "Name", pinned = True ),
    "Type": st.column_config.SelectboxColumn( "Type", pinned = True,options=option_type ),
    "Skill": st.column_config.SelectboxColumn( "Skill", pinned = True,options=option_skill ),
    "Level":col_progress(100,250,"Level","Palmon level"),
    "Step": st.column_config.NumberColumn(
        "Step",
        min_value=0,
        max_value=5,
        format="%d ⭐",
    ),
    "Steps": st.column_config.TextColumn("Steps"),
    "Achievement": col_progress(0,1,"Achievement","Achievement","percent"),
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
    "Star 1": col_pct_1,
    "Star 2": col_pct_1,
    "Star 3": col_pct_1,
    "Star 4": col_pct_1,
    "Star 5": col_pct_1,
    "Comp 1": st.column_config.NumberColumn(format="compact"),
    "Comp 2": st.column_config.NumberColumn(format="compact"),
    "Comp 3": st.column_config.NumberColumn(format="compact"),
    "Comp 4": st.column_config.TextColumn("Comp 4"),
    "Comp 5": st.column_config.NumberColumn(format="compact"),
    "Unused1": None,
    "Unused2": None,
    "Unused3": None,
    "Unused4": None,
    "Unused5": None,
    "Unused6": None,
    "Unused7": None,
    "Unused8": None,
    "Cost upgrade": st.column_config.NumberColumn(
        "Cost upgrade",
        format="compact",
    )
}
column_config_lst={
    "Name": st.column_config.TextColumn( "Name", pinned = True ),
    "Type": st.column_config.SelectboxColumn( "Type", pinned = True,options=option_type ),
    "Skill": st.column_config.SelectboxColumn( "Skill", pinned = True,options=option_skill ),
    "Level":col_progress(100,250,"Level","Palmon level"),
    "Step": st.column_config.NumberColumn(
        "Step",
        min_value=0,
        max_value=5,
        format="%d ⭐",
    ),
    "Steps": st.column_config.TextColumn("Steps"),
    "Achievement": col_progress(0,1,"Achievement","Achievement","percent"),
    "Cost to max": st.column_config.NumberColumn(
        "Cost to max",
        #format="localized",
        format="compact",
    ),
    "RankPower": None,
    "URL": None,
    "URL Mutation": None,
    "Stock": None,
    "Star 1": None,
    "Star 2": None,
    "Star 3": None,
    "Star 4": None,
    "Star 5": None,    
    "Comp 1": None,
    "Comp 2": None,
    "Comp 3": None,
    "Comp 4": None,
    "Comp 5": None,
    "Unused1": None,
    "Unused2": None,
    "Unused3": None,
    "Unused4": None,
    "Unused5": None,
    "Unused6": None,
    "Unused7": None,
    "Unused8": None,
    "Rank": None,
    "Team": None,
    "Mutation 1": None,
    "Mutation 2": None,        
    "Cost upgrade": st.column_config.NumberColumn(
        "Cost upgrade",
        format="compact",
    )
}
# ======================================================================================================

def toggle_excel_loaded():
    st.session_state.excel_loaded = not st.session_state.excel_loaded

def test_df_xls():
    columns = list(df_xls)
    for i in columns:
        cell1,cell2=st.columns(2)
        with cell1:
            st.write(i)
        with cell2:
            st.write(df_xls[i][2])

def get_device_type():
    user_agent = request.headers.get('User-Agent')
    user_agent_parsed = parse(user_agent)
    device_type = ("Mobile" if user_agent_parsed.is_mobile else
                   "Tablet" if user_agent_parsed.is_tablet else
                   "Desktop")
    return f"Device Type: {device_type}, Browser: {user_agent_parsed.browser.family}"

def write_js_script():
    js_script="""
        <script language=javascript>alert('Hello world');</script>
    """
    st.markdown(js_script, unsafe_allow_html=True)

def write_js_menu(): 
    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)    
    
def do_nothing():
    return None
    
def file_err():
   st.markdown(":orange-badge[⚠️ No file loaded]")

def write_info(msg,val):
    return st.markdown(f":orange-badge[{msg} : {val}]")

def write_one_info(msg):
    return st.info(f"{msg}", icon="ℹ️", width="stretch")
    
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
    # voir pour remplacer avec: df.loc[row_indexer, "col"] = values
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
        
def percent_format(value):
    try:
        ret=value*100
        return f"{ret:.2f}%"  # "12.34%"
    except:
        return empty()

def icon_upgradable(value):
    try:
        if int(value)==1:
            return "✅"       
    except:
        return "🟥" 

def icon_full_cost(value):
    try:
        df_data_values
    except:
        return value

def build_chart_bar(df_chart,xField,yField,sLabel,selMin=1,selMax=30,with_slider=True):
    if df_chart is not None:
        try:
            switch_axis = st.toggle("Switch axis")
        except:
            switch_axis = False
        x_Field = xField
        y_Field = yField
        if switch_axis:
            x_Field = yField
            y_Field = xField            
        st.bar_chart(df_chart, x=x_Field, y=y_Field)
        if with_slider==True:
            sel_min=selMin
            sel_max=selMax
            range_level_min, range_level_max= st.slider(
                label=sLabel,
                min_value=sel_min,
                max_value=sel_max,
                value=(sel_min,sel_max),
                step=1
            )
            df = df_chart.loc[(df_chart[x_Field] >= int(range_level_min)) & (df_chart[x_Field] <= int(range_level_max))]
            total_col = f"Total Energy cost from {range_level_min} to {range_level_max}"
            try:
                st.markdown(f":orange-badge[{total_col} : {large_num_format(int(df[y_Field].sum()))}]")
            except:
                st.markdown(f":orange-badge[{total_col} : {int(df[y_Field].sum())}]")
            excel_loaded=True
            return range_level_min, range_level_max
        else:
            df = df_chart.loc[(df_chart[xField] >= int(selMin)) & (df_chart[xField] <= int(selMax))]
            total_col = f"Total Crystals cost from {selMin} to {selMax}"
            st.markdown(f":orange-badge[{total_col} : {int(df[yField].sum())}]")
            return selMin,selMax

def build_graph_select():
    st.set_page_config(
        #page_title="yFiles Graphs for Streamlit",
        layout="wide",
    )
    field_x = 'Level'
    field_y = 'Stars'
    on = st.toggle(f'Switch axis {field_x}/{field_y}')
    if on:
        field_y = 'Level'
        field_x = 'Stars'
    else:
        field_x = 'Level'
        field_y = 'Stars'
    df_srv = get_df_base().copy()
    #Graphe per type
    chart = {
        "mark": "point",
        "params": [
            {"name": "interval_selection", "select": "interval"},
            {"name": "point_selection", "select": "point"},
        ],
        "encoding": {
            "x": {
                "field": field_x,
                "type": "quantitative",
            },
            "y": {
                "field": field_y,
                "type": "quantitative",
            },
                "size": {"field": "Achievement", "type": "quantitative"},
                "color": {"field": "Skill", "type": "nominal"},
                "shape": {"field": "Type", "type": "nominal"},
        },
    }
    
    column='Type'
    options = st.multiselect(f"Filter values for {column}:", df_srv[column].unique(), default=list(df_srv[column].unique()))
    source = df_srv[df_srv[column].isin(options)]
    #st.vega_lite_chart(source, chart, theme="streamlit", width="stretch")     
    event = st.vega_lite_chart(source, chart, theme=None, on_select="rerun", width="stretch") 
    try:
        df_level = event.selection.interval_selection.Level
        df_stars = event.selection.interval_selection.Stars
        min_val_level, max_val_level = df_level[0], df_level[1]
        min_val_stars, max_val_stars = df_stars[0], df_stars[1]
        df_selection = df_srv[(df_srv['Level'] >= min_val_level) & (df_srv['Level'] <= max_val_level)]
        df_selection = df_selection[(df_selection['Stars'] >= min_val_stars) & (df_selection['Stars'] <= max_val_stars)]
    except:
        df_selection=None #=df_srv #=source[['Name', 'Type', 'Skill', 'Level', 'Stars', 'URL']]
    if df_selection is not None:
        #data_to_tiles(df_selection)
        menu_tab_palmons(df_source=df_selection,with_event=False)
        #build_table_any(df_selection)

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

def get_df_base():
    try:
        if df_xls["DataFrame"][idx_palmon] is not None:
            return df_xls["DataFrame"][idx_palmon]
        else:
            return None
    except:
        return None

def data_to_tiles(df_data=None): 
    df_srv = get_df_base().copy()
    source = df_srv #df_srv[['Name', 'Type', 'Skill', 'Level', 'Stars', 'URL','Upgradable']]
    if df_data is not None:
        source = df_srv[df_srv['Name'].isin(df_data['Name'])] 
    #source.reset_index(drop=True)
    for i, source_row in source.iterrows():
        with st.container(horizontal_alignment="center", 
                          vertical_alignment="center", 
                          border=True):
            pal_deltail(source_row['Name'],source_row,pic_width=200)
    
def human_format(num, round_to=1):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num = round(num / 1000.0, round_to)
    return '{:.{}f}{}'.format(num, round_to, ['', 'K', 'M', 'B', 'G'][magnitude])
#df.style.format({"stars": human_format})

def build_table_full_costs(df_src):
    df=df_src.copy()
    #write_info("build_table_full_costs","")
    df['Cost type']=df['Cost type'].apply(lambda b: option_values[data_values['Value'].index(b)]+' '+b)
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
            },
            hide_index=True,
         )  

def build_table_dashboard(df):
    return st.dataframe(
                df[['Name','Level','Upgradable','Steps','Achievement']],
                column_config=column_config_lst,
                on_select="rerun",
                selection_mode="single-row",                    
                hide_index=True,
            )

def format_stars(x): #⭐
    try:
        return ("⭐" * int(x))[0:int(x)]
    except:
        return x

def calcul_upgrade_costs(from_lvl=1,to_lvl=300):
    if df_xls["DataFrame"][idx_palmon] is not None:
        df = df_xls["DataFrame"][idx_costs]
        val_cost=df.loc[(df["Level from"] >= from_lvl) & (df["Level from"] <= to_lvl)]["Cost"].sum()
        return val_cost
    else:
        return None

def calcul_upgrade_comp_costs(from_lvl=1,to_lvl=30):
    if df_xls["DataFrame"][idx_palmon] is not None:
        df = df_xls["DataFrame"][idx_comp]
        val_cost=df.loc[(df["Level from"] >= from_lvl) & (df["Level from"] <= to_lvl)]["Cost"].sum()
        return large_num_format(val_cost)
    else:
        return None

def show_details(palmon,df,popup=False):
    #st.markdown(f":orange-badge[palmon : {palmon}]")
    if 1 == 1:
        df_costs = df_xls["DataFrame"][idx_costs]
        max_upg=df_costs.loc[(df_costs["Cost"] >= 1)]["Level from"].max()
        filtered_df = df.copy().iloc[palmon]
        if len(filtered_df) > 0:
            #filtered_df['Cost upgrade']=df['Level'].apply(lambda b: large_num_format(int(calcul_upgrade_costs(b,max_upg))) )
            filtered_df['Cost to max']=df['Level'].apply(lambda b: int(calcul_upgrade_costs(b,max_upg)) )
            filtered_df['Steps']=df['Step'].apply(lambda b: format_stars(b) )
            if popup==True:
                pal_deltail_dialog(palmon,filtered_df)
            else:
                st.dataframe(
                    filtered_df,
                    column_config=column_config,
                    hide_index=True,
                )                
                pal_deltail(palmon,filtered_df)
    else:
        st.empty()

def get_cell_detail(df,fld):
    try:
        return df.at[0, fld]
    except:
        return empty()

@st.dialog("Details")
def pal_deltail_dialog(palmon,df):
    open_popup=False
    if "event_a" in st.session_state:
        open_popup = True
    if "event_d" in st.session_state:
        open_popup = True        
    if open_popup == True:
        pal_deltail(palmon,df,200)
    del_session_variable("event_a")
    del_session_variable("event_d")

def del_session_variable(var_key):
    try:
        del st.session_state[var_key]
    except:
        return None

def add_session_variable(var_key,var_value):
    del_session_variable(var_key)
    st.session_state[var_key]=var_value

def get_session_variable(var_key):
    try:
        return st.session_state[var_key]
    except:
        return None

def pal_deltail(palmon,df,pic_width=300):
    col_border=True
    df_t=df.reset_index().T
    df.reset_index()
    cols_comp = ['Comp 1','Comp 2','Comp 3','Comp 4','Comp 5']
    #df
    if pic_width == 300:
        cell_pic=2
    else:
        cell_pic=1
    row0 = st.columns([cell_pic, 1], border=col_border)
    row1 = st.columns(2,border=col_border, width="stretch")
    row2 = st.columns(2,border=col_border, width="stretch")

    df_cost = df_xls["DataFrame"][idx_costs]
    level_max=df_cost.loc[(df_cost["Cost"] >= 1)]["Level to"].max()
    level_pal=df.loc[df.index[0], 'Level']
    if level_pal >= level_max:
        level_max = 0
    
    with row0[0]:
        try:
            with st.container(horizontal_alignment="center", vertical_alignment="center"):
                st.image(df.loc[df.index[0], 'URL'], caption=df.loc[df.index[0], 'Name'], width=pic_width)
        except:
            st.empty()
    with row0[1]:
        df_info=df[['Type','Skill','Steps','Achievement','Level','Cost to max']]
        df_info.loc[df.index[0], 'Achievement'] = percent_format(df_info.loc[df.index[0], 'Achievement'])
        df_info.loc[df.index[0], 'Cost to max'] = large_num_format(df_info.loc[df.index[0], 'Cost to max'])
        df_info=df_info.reset_index().T
        st.dataframe(df_info,
                    column_config={
                        "Achievement": col_progress(0,1,"Achievement","Achievement","percent"),                     
                     },
                     hide_index=False) 
    with row1[0]:
        #st.markdown(f"Level: {df.loc[df.index[0], 'Level']}")
        #df_cost = df_xls["DataFrame"][idx_costs]
        #level_max=df_cost.loc[(df_cost["Cost"] >= 1)]["Level from"].max()
        #level_pal=df.loc[df.index[0], 'Level']
        #if level_pal >= level_max:
        #    level_max = 0
        st.metric("Level", level_pal, level_max)
    with row1[1]:
        df_costs = df_xls["DataFrame"][idx_costs]
        max_upg=df_costs.loc[(df_costs["Cost"] >= 1)]["Level to"].max()
        cost_upg=calcul_upgrade_costs(df.loc[df.index[0], 'Level'],max_upg)
        #st.markdown(f"cost to {max_upg}: {large_num_format(cost_upg)}")
        st.metric("Cost", large_num_format(cost_upg), level_max)
    with row2[0]:
        st.write('Competencies')
        build_table_any(df[cols_comp])
    with row2[1]:
        st.write('Competencies upgrade costs')
        df_comp_u=df[cols_comp]
        df_comp_costs = df_xls["DataFrame"][idx_costs]
        for i in [1,2,3,5]:
            df_comp_u.loc[df.index[0], f'Comp {i}'] =  calcul_upgrade_comp_costs( df_comp_u.loc[df.index[0], f'Comp {i}'],10 if i==5 else 30 )
        
        build_table_any(df_comp_u[cols_comp])

# ======================================================================================================
#
#    Definition fonctions pages/menu
#
# ======================================================================================================
def menu_load_excel():
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
                        if option == "Stars":
                            df1.columns = cols_stars                        
                    st.dataframe(df1)
                    excel_loaded=True
            else:
                uploaded_file=None
        expanded=False
        
    if df_xls["DataFrame"][idx_costs] is not None:
        excel_loaded=True
    else:
        excel_loaded=False
    
    tabs_data=[]
    row, col = df_xls.shape
    for i in range(row):
        get_data(uploaded_file,i,False)
        if int(i)!=int(idx_stars):
            tabs_data.append(stx.TabBarItemData(id=i, 
                                                title=df_xls["DisplayName"][i], 
                                                description=df_xls["Description"][i], ) )
    add_session_variable("tabs_data",tabs_data)

def menu_build_tabs(idx_selected=0):
    
    tabs_fixed=[stx.TabBarItemData(id=100, title="Dashboard", description="List of Dashboards"),
                stx.TabBarItemData(id=150, title="Graph", description="Visual selection"),
                stx.TabBarItemData(id=200, title="Downloads", description="CSV download"),
               ]
    
    rows,cols=df_xls.shape
    
    tabs_data=get_session_variable("tabs_data")+tabs_fixed
    try:
        chosen_id = stx.tab_bar(data=tabs_data, default=idx_selected)
    except:
        chosen_id = stx.tab_bar(data=tabs_data, default=0)
    menu_tab_show(chosen_id)

def menu_tab_show(idx):
    #write_info("chosen_id=",int(idx))
    if df_xls["DataFrame"][idx_palmon] is not None:
        idx_tab = idx
    else:
        idx_tab = 999
    match int(idx_tab):
        case 0:         #int(idx_palmon)
            menu_tab_palmons()   
        case 1:         #int(idx_costs):
            menu_tab_costs()            
        case 2:        #int(idx_comp):
            menu_tab_comp()
        case 3:        #int(idx_mut):
            menu_tab_mut()
        case 4:        #int(idx_val):
            menu_tab_val()
        case 100:
            menu_tab_dashboards()
        case 150:
            build_graph_select()
        case 200:
            menu_tab_downloads()
        case _:
            return st.empty()

def menu_tab_comp():
    st.header(df_xls["DisplayName"][idx_comp])
    df = df_xls["DataFrame"][idx_comp]
    range_level_min, range_level_max = build_chart_bar(df_xls["DataFrame"][idx_comp],'Level from','Cost','Competencies costs from level:',int(1),int(30))
    with st.expander("Data graph", expanded=False, width="stretch"):
        build_table_any(df.loc[(df['Level from'] >= range_level_min) & (df['Level from'] <= range_level_max)])
    
def menu_tab_costs():
    df = df_xls["DataFrame"][idx_costs]
    df_pal=df_xls["DataFrame"][idx_palmon]
    st.header(df_xls["DisplayName"][idx_costs])
    min_upg=df_pal.loc[(df_pal["Level"] >= 1)]["Level"].min()
    max_upg=df.loc[(df["Cost"] >= 1)]["Level to"].max()
    range_level_min, range_level_max = build_chart_bar(df_xls["DataFrame"][idx_costs],'Level from','Cost','Upgrade costs from level:',int(min_upg),int(max_upg))
    with st.expander("Data graph", expanded=False, width="stretch"):
        build_table_any(df.loc[(df['Level from'] >= range_level_min) & (df['Level to'] <= range_level_max)])    

def menu_tab_mut():
    st.header(df_xls["DisplayName"][idx_mut]) 
    df = df_xls["DataFrame"][idx_mut]
    df_energy=df.loc[(df['Step'] > 0)]
    df_crystal=df.loc[(df['Step'] == 0)]        
    st.header("Energy")
    range_level_min, range_level_max = build_chart_bar(df_energy,'Level','Cost level','Mutation costs from level:',int(1),int(30))
    st.header("Crystals")
    build_chart_bar(df_crystal,'Level','Cost level','Mutation costs from level:',int(1),int(30),False)
    with st.expander("Data graph", expanded=False, width="stretch"):
        build_table_any(df_crystal.loc[(df['Level'] >= range_level_min) & (df['Level'] <= range_level_max)])
        build_table_any(df_energy.loc[(df['Level'] >= range_level_min) & (df['Level'] <= range_level_max)])

def menu_tab_val():
    #st.header(df_xls["DisplayName"][idx_val]) 
    #build_table_full_costs(df_xls["DataFrame"][idx_val])
    #st.divider()
    #st.header(df_xls["DisplayName"][idx_stars])
    #df_stars=df_xls["DataFrame"][idx_stars].copy(deep=True)
    #df_stars['Stars level']=df_stars['Stars level'].apply(lambda b: format_stars(b) )
    #build_table_any(df_stars)
    rowval = st.columns(2,border=False, width="stretch")
    with rowval[0]:
        st.header(df_xls["DisplayName"][idx_val]) 
        build_table_full_costs(df_xls["DataFrame"][idx_val])
    with rowval[1]:
        st.header(df_xls["DisplayName"][idx_stars])
        df_stars=df_xls["DataFrame"][idx_stars].copy(deep=True)
        df_stars['Stars level']=df_stars['Stars level'].apply(lambda b: format_stars(b) )
        build_table_any(df_stars)

def menu_tab_palmons(df_source=None,with_event=True):
    if df_source is None:
        st.header(df_xls["DisplayName"][idx_palmon])
        df = df_xls["DataFrame"][idx_palmon]
    else:
        df = df_source
    #df = df.sort_values(by=['Level','Achievement'],ascending=False,ignore_index=True)
    df['Type']=df['Type'].apply(lambda b: option_type[data_type['Type'].index(b)])
    df['Skill']=df['Skill'].apply(lambda b: option_skill[0] if b=='Attack' else option_skill[1]) 
    df['Upgradable']=df['Upgradable'].apply(lambda b: icon_upgradable(b)) 
    df_display=df[cols_palmon]
    event = None
    with st.expander("List", expanded=True, width="stretch"):
        event = st.dataframe(
            df, #df_xls["DataFrame"][idx_palmon],
            column_config=column_config_lst,
            on_select="rerun",
            selection_mode="single-row",
            hide_index=True,
        )
    if event is not None and with_event:
        show_details(event.selection.rows,df_xls["DataFrame"][idx_palmon])
        #event = None    
   
def menu_tab_dashboards():
    col_border=False
    st.header("Dashboard")
    df=df_xls["DataFrame"][idx_palmon]
    df1=df.copy()
    df1['Steps']=df['Step'].apply(lambda b: format_stars(b) )
    df1['Upgradable']=df1['Upgradable'].apply(lambda b: icon_upgradable(b)) 
    df1['Type']=df1['Type'].apply(lambda b: option_type[data_type['Type'].index(b)]+b)
    df=df1.iloc[:-1,:].sort_values(by=['Skill','Level','Achievement'],ascending=False,ignore_index=True)
    df_a=df1.iloc[:-1,:].sort_values(by=['Skill','Level','Achievement'],ascending=False,ignore_index=True)
    df_d=df1.iloc[:-1,:].sort_values(by=['Skill','Level','Achievement'],ascending=False,ignore_index=True)
    #df_a = df_a[(df_a['Skill'] == '⚔ Attack')].sort_values(by=['Skill','Level','Achievement'],ascending=False,ignore_index=True).head(7)
    df_a = df1[(df1['Skill'] != '🛡 Defend')].head(7)
    df_d = df_d[(df_d['Skill'] != '⚔ Attack')].head(7)

    row_d0 = st.columns(2,border=col_border, width="stretch")
    with row_d0[0]:
        st.subheader('⚔ Attack top 7')
        event_a = build_table_dashboard(df_a)
        #event_a = st.dataframe(
        #        df_a[['Name','Level','Upgradable','Steps','Achievement']],
        #        column_config=column_config_lst,
        #        on_select="rerun",
        #        selection_mode="single-row",                    
        #        hide_index=True,
        #    )
        if event_a is not None:
            st.session_state["event_a"]=event_a.selection.rows
            show_details(event_a.selection.rows,df_a,True)
            #if 'event_a' not in st.session.state:
            event_a = None  
    
    with row_d0[1]:
        st.subheader('🛡 Defend top 7')
        event_d = build_table_dashboard(df_d)
        #event_d = st.dataframe(
        #        df_d[['Name','Level','Upgradable','Steps','Achievement']],
        #        column_config=column_config_lst,
        #        on_select="rerun",
        #        selection_mode="single-row",                    
        #        hide_index=True,
        #    )
        if event_d is not None:
            st.session_state["event_d"]=event_d.selection.rows
            show_details(event_d.selection.rows,df_d,True)
            #if 'event_d' not in st.session.state:
            event_d = None                
        
    row_d1 = st.columns(2,border=col_border, width="stretch")
    with row_d1[0]:
        st.subheader('Average Level by Type')
        #df1c=avg_lvl_df['Types']=avg_lvl_df['Type'].apply(lambda b: option_type[data_type['Type'].index(b)])
        avg_lvl_df = df1.set_index('Type').groupby('Type').apply(lambda x: large_num_format(x['Level'].sum() / x['Level'].count()), include_groups=True).to_frame('Level')
        avg_lvl_df
        #avg_lvl_df.index.names = ['Type']
        #avg_lvl_df['Types']=avg_lvl_df['Type'].apply(lambda b: option_type[data_type['Type'].index(b)])

    with row_d1[1]:
        st.subheader('Average power by Type')
        avg_pwr_df = df1.set_index('Type').groupby('Type').apply(lambda x: large_num_format(x['RankPower'].sum() / x['Level'].count()), include_groups=True).to_frame('Power')
        #avg_pwr_df['Type']=avg_pwr_df['Type'].apply(lambda b: option_type[data_type['Type'].index(b)])
        avg_pwr_df    

def menu_tab_downloads():
    #st.title(body="Download file data test", text_alignment="center")
    st.subheader("Choose local data (csv)", divider=False)
    
    range_cols = st.columns(3)
    range_cols[0].download_button(
        label="Palmons data",
        data=df_xls["DataFrame"][idx_palmon].to_csv().encode("utf-8"),
        file_name="base_data.csv",
        mime="text/csv",
        icon=":material/download:",
    )
    range_cols[1].download_button(
        label="EXP costs",
        data=df_xls["DataFrame"][idx_costs].to_csv().encode("utf-8"),
        file_name="exp_data.csv",
        mime="text/csv",
        icon=":material/download:",
    )
    range_cols[2].download_button(
        label="COMP costs",
        data=df_xls["DataFrame"][idx_comp].to_csv().encode("utf-8"),
        file_name="comp_data.csv",
        mime="text/csv",
        icon=":material/download:",
    )    

# ======================================================================================================
#
#    Definition PAGES
#
# ======================================================================================================
def pg_home():
    st.title(f"{app_title} App")
    write_one_info(get_device_type())
    if df_xls["DisplayName"][idx_palmon] is not None:
        menu_build_tabs()
    else:
        file_err()
        
def pg_menu_0():
    menu_tab_show(0)

def pg_menu_200():
    menu_tab_show(200)
    
def page1():
    st.title(f"{app_title} 1st page")

def page2():
    st.title("Second page")
    st.header("os.environ")
    os.environ
    st.header("os.sysconf_names")
    os.sysconf_names
    st.header("user_agent")
    #os.stat
    user_agent = request.headers.get('User-Agent')
    user_agent_parsed = parse(user_agent)

# ======================================================================================================
#
#    Start MAIN page
#
# ======================================================================================================
app_title='Test Excel File'
st.set_page_config(
    page_title=app_title,
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={        # <===================================== #top right menu (triple dots) near GitHub icon
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
#st.title(f"{app_title} App")
# Widgets shared by all the pages
#st.sidebar.selectbox("Foo", ["A", "B", "C"], key="foo")
#st.sidebar.checkbox("Bar", key="bar")

#pg = st.navigation([
#    st.Page(page_loadxls, title="Load Excel file", icon=":material/favorite:"),
#    st.Page(page_tabs,title="Data", icon=":material/favorite:"),
#    st.Page(page1, title="First page", icon="🔥"),
#    st.Page(page2, title="Second page", icon=":material/favorite:"),
#])
#pg.run()

if 1 == 1:    # <=====================================
    with st.sidebar:
        menu_load_excel()
if 1 == 2:    # <=====================================   
    if df_xls["DisplayName"][idx_palmon] is not None:
        menu_build_tabs()
    else:
        file_err()

if 1 == 1:    # <=====================================
    pages = {
        "Home":[ st.Page(pg_home, title="Home", icon=":material/home:") ],
        "Resources": [
            st.Page(pg_menu_0, title="Full list"),
            st.Page(pg_menu_200, title="CSV downloads"),
        ],
        "Tests": [
            st.Page(page1, title="Page 1"),
            st.Page(page2, title="Page 2"),
        ],
    }
    pg = st.navigation(pages)
    pg.run()    




            
#write_js_menu()
# ======================================================================================================
#
#    End MAIN page
#
# ======================================================================================================


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

