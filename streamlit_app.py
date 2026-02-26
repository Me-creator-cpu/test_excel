import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import statistics
from openpyxl import load_workbook
import locale
import logging
import os
import platform
import json
from user_agents import parse
import extra_streamlit_components as stx    #https://github.com/Mohamed-512/Extra-Streamlit-Components

#import altair as alt
#from io import StringIO
#from io import BytesIO
#from flask import Flask, request
#from flask import request
#import request
#import matplotlib.pyplot as plte
#import statistics Library
#import xlsxwriter
#from openpyxl.utils.dataframe import dataframe_to_rows

st_logger = logging.getLogger('streamlit')
st_logger.setLevel(logging.WARNING)

pal_test=None    # Test pour class

# ======================================================================================================
# URL: https://testexcel-xwu5zapqqz8ukerpqqvxhu.streamlit.app/
# ======================================================================================================
#https://icones8.fr/icons/set/drapeau--style-color
url_maintenance = 'https://scontent-cdg4-2.cdninstagram.com/v/t39.30808-6/632313034_122190805178516338_8580667498397042596_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=100&ig_cache_key=MzgyOTQ0NTI2ODQzMDE5MTIzMQ%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6InhwaWRzLjEwODB4MTA4MC5zZHIuQzMifQ%3D%3D&_nc_ohc=9CUwkXAvwyQQ7kNvwEUeiQU&_nc_oc=Adl4KQ39JfzgHhJP82DLmvNVwanWYMjllSvAo3CYNeWo6SSNScuZBDmntao9H9gSRXg&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-cdg4-2.cdninstagram.com&_nc_gid=jgbS-gOsY44BPhZBZhuRuA&oh=00_AfsArBnqm8Qm_KKklrV7twUzlavNPKn7bpYkHMG93C4WZw&oe=69A36204'
url_menu_boss = 'https://i.ytimg.com/vi/ka0jFGAPnqQ/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAuTuC7wOYDNJ4TqjlsXACLakFfwg'

# ======================================================================================================
# Optimisations
# df["col"][row_indexer] = value ==> Use `df.loc[row_indexer, "col"] = values` instead
# ======================================================================================================

# Définitions variables
df_xls = None
#uploaded_file = None
excel_loaded=False
tabs_data=[]
tabs = None
global texts_trad
texts_trad = None
run_every = None

#def init_session():
if 'texts_trad' not in st.session_state:
    st.session_state.texts_trad = None
if 'site_langu' not in st.session_state:
    st.session_state.site_langu = None    

if 'df_data' not in st.session_state:
    st.session_state.df_data = df_xls
if 'uploaded_file' not in st.session_state:
    uploaded_file = None
    st.session_state.uploaded_file = uploaded_file
else:
    uploaded_file = st.session_state.uploaded_file

if "excel_loaded" not in st.session_state:
    st.session_state.excel_loaded = False
if "tabs_data" not in st.session_state:
    st.session_state.tabs_data = tabs_data

if "stream" not in st.session_state:
    st.session_state.stream = False
    
# Définitions variables de sélection de dataframes
event = None
event_a = None
event_d = None
event_detail = None

# Définitions DataFrame et Excel
#cols_data = ['Name','Type','Skill','Level','Upgradable','Step','Stars','Stock','Star 1','Star 2','Star 3','Star 4','Star 5','Unused1','Comp 1','Comp 2','Comp 3','Comp 4','Comp 5','Achievement','Needs','Unused2','Cost to max','Unused3','Unused4','RankPower','Rank','Team','Unused5','URL','URL Mutation','Unused6','Unused7','Mutation 1','Mutation 2','Unused8']
cols_data = ['Name','Type','Skill','Level','Upgradable','Step','Stars','Stock','Comp 1','Comp 2','Comp 3','Comp 4','Comp 5','Unused1','Star 1','Star 2','Star 3','Star 4','Star 5','Achievement','Needs','Unused2','Cost to max','Unused3','Unused4','RankPower','Rank','Team','Unused5','URL','URL Mutation','Unused6','Unused7','Mutation 1','Mutation 2','Unused8']
cols_exp = ['Level from', 'Level to', 'Cost']
cols_comp = ['Level from', 'Cost']
cols_mut = ['Level', 'Step', 'Substep', 'Cost level']
cols_mut_full = ['Cost type', 'Cost']
cols_stars = ['Stars level', 'Unit Cost', 'Total']
cols_boss = ['Stars level', 'Unit Cost', 'Total']
cols_boss_data = ['Name','Type', 'Level', 'Stars','Comp 1','Comp 2','Comp 3','Comp 4','Comp 5','URL']

df_pal_data=None
df_costs_exp=None
df_costs_comp=None
df_costs_mut=None
df_costs_mut_full=None
df_costs_stars=None
df_costs_boss=None
df_boss_data=None

idx_palmon=0
idx_costs=1
idx_comp=2
idx_mut=3
idx_val=4
idx_stars=5
idx_boss=6
idx_boss_data=7
#✨
data = { #                    0                  1                  2                    3                4                        5                    6                    7
        "Worksheet":      ["Palmon_data",    "Tableaux",        "Tableaux",         "Tableaux",         "Valeurs",                "Stars",           "Valeurs",            "Valeurs"],
        "DisplayName":    ["Palmons",        "Upgrade costs",   "Competencies",     "Mutation costs",   "Upgrade full costs",     "Stars",           "Boss",               "Boss data"],
        "Range":          ["A:AJ",           "A:C",             "H:I",              "N:Q",              "A:B",                    "A:C",             "D:E",                "H:Q"],
        "SkipRows":       [0,                1,                 1,                  1,                  0,                        0,                 1,                    1],
        "UpToRow":        [41,               302,               31,                 224,                4,                        7,                 5,                    5],
        "DisplayColumns": [cols_data,        cols_exp,          cols_comp,          cols_mut,           cols_mut_full,            cols_stars,        cols_boss,            cols_boss_data],
        "DataFrame":      [df_pal_data,      df_costs_exp,      df_costs_comp,      df_costs_mut,       df_costs_mut_full,        df_costs_stars,    df_costs_boss,        df_boss_data],
        "Description":    ["Full list",      "EXP per level",   "Any palmon type",  "UR only",          "Defined values",         "Omni UR costs",   "Boss upgrade costs", "Boss details"],
       }
df_xls = pd.DataFrame(data)
data_flags={"en":"https://img.icons8.com/?size=100&id=t3NE3BsOAQwq&format=png&color=000000","fr":"https://img.icons8.com/?size=100&id=3muzEmi4dpD5&format=png&color=000000"}
option_skill=["⚔ Attack","🛡 Defend"]
data_skills={
    "Skill":["Attack","Defend"],
    "Icon":option_skill
}
data_type={
    "Type":["Water",  "Fire",    "Electricity",    "Wood",    "Any"],
    "Icon":["💧",    "🔥",      "⚡",             "🪵",     "🌐"] 
}
data_values={
    "Value":["Energy","Crystals","Pieces","Level300"],
    "Icon":["🟢",     "💎",     "🧩",    "🔝"],
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
    "Type_txt": None,
    "Cost upgrade": st.column_config.NumberColumn(
        "Cost upgrade",
        format="compact",
    )
}
column_config_lst={
    "Name": st.column_config.TextColumn( "Name", pinned = True ),
    "Type": st.column_config.TextColumn( "Type", pinned = True ),
    "Skill": st.column_config.TextColumn( "Skill", pinned = True ),
    #"Type": st.column_config.SelectboxColumn( "Type", pinned = True,options=option_type ),
    #"Skill": st.column_config.SelectboxColumn( "Skill", pinned = True,options=option_skill ),
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
    "Type_txt": None,
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

def is_mobile():
    if st.context:
        headers = st.context.headers
        user_agent_string = headers.get("User-Agent", "")
        if not user_agent_string:
            return False
        ua = user_agent_string.lower()
        if 'iphone' in ua:
            return True
        if 'android' in ua and 'mobile' in ua:
            return True
        if 'windows phone' in ua:
            return True
        if 'blackberry' in ua:
            return True
    else:
        return False
    return False
    
def get_device_type():
    headers = st.context.headers
    user_agent = headers.get("User-Agent", "")    
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

def write_js_menu(bln=False): 
    # ---- HIDE STREAMLIT STYLE ----
    #class="stToolbarActionButton" data-testid="stToolbarActionButton"
    #
    hide_st_style = """
                <style>
                MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                stSidebar {visibility: display;}
                [data-testid="stSidebar"] {display: inline-block;}
                </style>
                """
    if bln:
        st.markdown(hide_st_style, unsafe_allow_html=True)    

def write_css_round_img():
    round_st_style = """
                <style>    
                    .circular_image {
                      width: 200px;
                      height: 200px;
                      border-radius: 50%;
                      overflow: hidden;
                      background-color: blue;
                      /* commented for demo
                      float: left;
                      margin-left: 125px;
                      margin-top: 20px;
                      */
                      
                      /*for demo*/
                      display:inline-block;
                      vertical-align:middle;
                    }
                    .circular_image img{
                      width:100%;
                    }    
                </style>
                """
    st.markdown(round_st_style, unsafe_allow_html=True)  
    
def do_nothing():
    return None
    
def file_err():
    msg_no_file=get_text_trad(site_langu,'no_file')
    return st.markdown(f":orange-badge[⚠️ {msg_no_file}]")

def write_info(msg,val):
    return st.markdown(f":orange-badge[{msg} : {val}]")

def write_one_info(msg):
    return st.info(f"{msg}", icon="ℹ️", width="stretch")

def write_coming_soon():
    maintenance=st.container(border=False, width='stretch', height='content')
    with maintenance:
        st.subheader("Coming soon...", divider=False)
        st.image(url_maintenance, caption=None, width="content")
    return maintenance

def pic(pic_url=None,pic_width='content'):
    if pic_url is not None and use_pics:
        st.image(pic_url, caption=None, width=pic_width)

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

def icon_skill(value):
    try:
        return option_skill[data_skills['Skill'].index(value)]+value
    except:
        return value

def icon_upgradable(value):
    try:
        return '✅' if int(value)==1 else '🟥' 
    except:
        return '🟥'

def icon_full_cost(value):
    try:
        df_data_values
    except:
        return value

def clear_cache():
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)
    st.toast('Cache cleared', icon='ℹ️️', duration='short')

def read_json_trads(sFile='textes.json'):
    json_data = None
    try:
        with open(sFile, encoding='utf-8', errors='ignore') as f:
            json_data = json.load(f, strict=False) 
        st.toast('JSON file loaded', icon='ℹ️️', duration='short')
    except:
        st.toast('Error loading JSON file', icon='🔴', duration='short')
    return json_data

def get_text_trad(langu='en',textId='text_id'):
    ret_val = ''
    try:
        texts_trad=st.session_state.texts_trad
        ret_val = texts_trad['data'][textId][0][langu]
    except:
        st.session_state.texts_trad = read_json_trads()
        ret_val=f'Trad err {textId}/{langu}'
    return ret_val

@st.fragment(run_every=run_every)
def check_file_loaded():
    now = datetime.now()
    if df_xls["DataFrame"][idx_palmon] is not None:
        return st.success(f'{now} - File loaded', icon="✅")
    else:
        return st.warning(f'{now} - File is NOT loaded', icon="⚠️")
        
def build_main_chart(raw_data,title_expander=None,x_axis=None,y_axis=None):
    if title_expander is not None:
        container = st.expander(title_expander, expanded=True, width="stretch")
    else:
        container = st.container(border=False, width='stretch', height='content')
    with container:
        st.bar_chart(
            raw_data,
            x=x_axis,
            y=y_axis,
            horizontal=True,
    )
      
def build_chart_bar(df_chart,xField,yField,sLabel,selMin=1,selMax=30,with_slider=True):
    if df_chart is not None:
        try:
            #switch_axis = st.toggle("Switch axis")
            switch_axis = st.toggle(get_text_trad(site_langu,'switch_axis'))
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
            total_txt=get_text_trad(site_langu,'total_nrj_cost')
            to_txt=get_text_trad(site_langu,'to')
            total_col = f"{total_txt} {range_level_min} {to_txt} {range_level_max}"
            try:
                st.markdown(f":orange-badge[{total_col} : {large_num_format(int(df[y_Field].sum()))}]")
            except:
                st.markdown(f":orange-badge[{total_col} : {int(df[y_Field].sum())}]")
            excel_loaded=True
            return range_level_min, range_level_max
        else:
            df = df_chart.loc[(df_chart[xField] >= int(selMin)) & (df_chart[xField] <= int(selMax))]
            total_txt=get_text_trad(site_langu,'total_cry_cost')
            to_txt=get_text_trad(site_langu,'to')
            total_col = f"{total_txt} {selMin} {to_txt} {selMax}"
            st.markdown(f":orange-badge[{total_col} : {int(df[yField].sum())}]")
            return selMin,selMax

def build_graph_select():
    st.set_page_config(
        layout="wide",
    )
    field_1 = 'Level' #get_text_trad(site_langu,'level') #'Level'
    field_2 = 'Stars' #get_text_trad(site_langu,'stars') #'Stars'
    on = st.toggle(f'{get_text_trad(site_langu,'switch_axis')} {field_1}/{field_2}')
    if on:
        field_x = field_2
        field_y = field_1
    else:
        field_x = field_1
        field_y = field_2
    df_srv = get_df_base().copy()
    max_upg=df_srv.loc[(df_srv["Level"] >= 1)].Level.max()+10
    min_upg=df_srv.loc[(df_srv["Level"] >= 10)].Level.min()-10
    #write_info('max_upg',max_upg)
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
                "scale": {"domain": [int(min_upg), int(max_upg)]},
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
    #source = df_srv[df_srv[column].isin(options)]
    source = df_srv[(df_srv[column].isin(options)) & (df_srv['Level'] >= int(min_upg))]
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
        menu_tab_palmons(df_source=df_selection,with_event=False,with_expander=True)
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
            ),
            "Unit cost": st.column_config.NumberColumn(format="compact"),
            "Total": st.column_config.NumberColumn(format="compact"),
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

def build_pivot_table(raw_data,val_value: str, val_index: str, val_columns: str,title_expander=None):
    if title_expander is not None:
        container_tb = st.expander(title_expander, expanded=True, width="stretch")
    else:
        container_tb = st.container(border=False, width='stretch', height='content')
    palmon_types_df = raw_data.pivot_table(values=val_value, index=val_index, columns=val_columns)
    with container_tb:
        st.dataframe(
            palmon_types_df.style.highlight_max(axis=0),
            column_config={
                "Type": st.column_config.TextColumn( "Type", pinned = True ),
                "Attack": st.column_config.NumberColumn( "⚔ Attack", step=".01" ), #:crossed_swords:
                "Defend": st.column_config.NumberColumn( "🛡 Defend", step=".01" ), #:shield:
                "Level": st.column_config.NumberColumn( "Level", step=".01" ),
                "Level": st.column_config.NumberColumn( "Count", step="0" ),
            },
            width="stretch",
            hide_index=None,
        )

def build_table_dashboard(df):
    return st.dataframe(
                df[['Name','Type','Level','Upgradable','Steps','Achievement']],
                column_config=column_config_lst,
                on_select="rerun",
                selection_mode="single-row",                    
                hide_index=True,
            )

def apply_cols_icons(df):
    df['Steps']=df['Step'].apply(lambda b: format_stars(b) )
    df['Upgradable']=df['Upgradable'].apply(lambda b: icon_upgradable(b))
    #df['Skill']=df['Skill'].apply(lambda b: icon_skill(b)) 
    df['Type']=df['Type'].apply(lambda b: option_type[data_type['Type'].index(b)]+b)
    return df
    
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
        #df = df_xls["DataFrame"][idx_comp]
        #val_cost=df.loc[(df["Level from"] >= from_lvl) & (df["Level from"] <= to_lvl)]["Cost"].sum()
        val_cost=get_upgrade_comp_costs(from_lvl,to_lvl)
        return large_num_format(val_cost)
    else:
        return None

def get_upgrade_comp_costs(from_lvl=1,to_lvl=30):
    if df_xls["DataFrame"][idx_palmon] is not None:
        df = df_xls["DataFrame"][idx_comp]
        val_cost=df.loc[(df["Level from"] >= from_lvl) & (df["Level from"] <= to_lvl)]["Cost"].sum()
        return int(val_cost)
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
    if "event_detail" in st.session_state:
        open_popup = True
    if open_popup == True:
        pal_deltail(palmon,df,200)
    del_session_variable("event_a")
    del_session_variable("event_d")
    del_session_variable("event_detail")
    del_session_variable("event_df")

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
    
    if 1 == 2:
        #pal_test=None
        pal_test=testClass(df.loc[df.index[0], 'Name'],df)
        if st.button("Test class"):
            write_info('pal_test',pal_test)
            write_info('pal_test.get_type()',pal_test.get_type()) 
        if pal_test is not None:
            if st.button("Get from class"):
                write_info('pal_test',pal_test) 
                write_info('pal_test.get_type()',pal_test.get_type())
                write_info('pal_test.get_level()',pal_test.get_level())
                write_info('pal_test.get_image()',pal_test.get_image())
    
    if pic_width == 300:
        cell_pic=2
    else:
        cell_pic=1
    row0 = st.columns([cell_pic, 1], border=col_border)
    row1 = st.columns(3,border=col_border, width="stretch")
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
        st.metric("Level upgrade", level_pal, level_max)
    with row1[1]:
        df_costs = df_xls["DataFrame"][idx_costs]
        max_upg=df_costs.loc[(df_costs["Cost"] >= 1)]["Level to"].max()
        cost_upg=calcul_upgrade_costs(df.loc[df.index[0], 'Level'],max_upg)
        st.metric("Cost", large_num_format(cost_upg), level_max)
    with row2[0]:
        st.write('Competencies')
        build_table_any(df[cols_comp])
    with row2[1]:
        st.write('Competencies upgrade costs')
        df_comp_u=df[cols_comp]
        df_comp_costs = df_xls["DataFrame"][idx_costs]
        total_comp_costs=0
        for i in [1,2,3,5]:
            comp_cost=get_upgrade_comp_costs( df_comp_u.loc[df.index[0], f'Comp {i}'],10 if i==5 else 30 )
            df_comp_u.loc[df.index[0], f'Comp {i}']=large_num_format(comp_cost)
            total_comp_costs=total_comp_costs+comp_cost
            #df_comp_u.loc[df.index[0], f'Comp {i}']=calcul_upgrade_comp_costs( df_comp_u.loc[df.index[0], f'Comp {i}'],10 if i==5 else 30 )
        #total_comp_costs=get_upgrade_comp_costs( df_comp_u.loc[df.index[0], 0],30)
        #df_comp_u.loc[df.index[0], 'Comp 1']+df_comp_u.loc[df.index[0], 'Comp 2']
        build_table_any(df_comp_u[cols_comp])
        write_info('Total competencies cost',large_num_format(total_comp_costs))
    with row1[2]:
        st.metric("Competencies cost", large_num_format(total_comp_costs), 'Max')

# ======================================================================================================
#
#    Definition fonctions pages/menu
#
# ======================================================================================================
def menu_load_excel(with_expander=True,getnewfile=True):
    if getnewfile:
        if with_expander:
            container=st.expander(get_text_trad(site_langu,'xls'), expanded=True, width="stretch")
        else:
            container=st.container(border=False, width='stretch', height='content')
        with container:
            uploaded_file  = st.file_uploader(get_text_trad(site_langu,'xls_sel'), type = 'xlsx')
            excel_loaded=False
            if uploaded_file is not None:
                st.session_state.uploaded_file = uploaded_file
                file = pd.ExcelFile(uploaded_file)
                if file is not None:
                    excel_loaded=True
                else:
                    uploaded_file=None
            expanded=False
            
        if df_xls["DataFrame"][idx_costs] is not None:
            excel_loaded=True
            st.session_state.uploaded_file = uploaded_file
        else:
            excel_loaded=False
    else:
        uploaded_file = st.session_state.uploaded_file
        #file = pd.ExcelFile(st.session_state.uploaded_file)    
    
        #st.toast(f'df_xls.shape={df_xls.shape}', icon='ℹ️️', duration='short')
        #st.toast(f'uploaded_file={uploaded_file}', icon='ℹ️️', duration='short')
        #st.toast(f'st.session_state.uploaded_file={st.session_state.uploaded_file}', icon='ℹ️️', duration='short')
    
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
    #if df_xls.loc[idx_palmon, "DataFrame"] is not None:
    if df_xls["DataFrame"][idx_palmon] is not None:
        idx_tab = idx
    else:
        idx_tab = 999
    match int(idx_tab):
        case 0:         #int(idx_palmon)
            menu_tab_palmons(with_expander=False)   
        case 1:         #int(idx_costs):
            menu_tab_costs()            
        case 2:        #int(idx_comp):
            menu_tab_comp()
        case 3:        #int(idx_mut):
            menu_tab_mut()
        case 4:        #int(idx_val):
            menu_tab_val()
        case 6:    #idx_boss
            menu_tab_boss()
        case 7:    #idx_boss_data
            menu_tab_boss_detail()
        case 100:
            menu_tab_dashboards()
        case 150:
            menu_tab_graph()
        case 200:
            menu_tab_downloads()
        case _:
            return st.empty()

def menu_tab_comp():
    st.subheader(df_xls["DisplayName"][idx_comp])
    df = df_xls["DataFrame"][idx_comp]
    range_level_min, range_level_max = build_chart_bar(df_xls["DataFrame"][idx_comp],'Level from','Cost','Competencies costs from level:',int(1),int(30))
    with st.expander(get_text_trad(site_langu,'data_graph'), expanded=False, width="stretch"):
        build_table_any(df.loc[(df['Level from'] >= range_level_min) & (df['Level from'] <= range_level_max)])
    
def menu_tab_costs():
    df = df_xls["DataFrame"][idx_costs]
    df_pal=df_xls["DataFrame"][idx_palmon]
    st.subheader(df_xls["DisplayName"][idx_costs])
    min_upg=df_pal.loc[(df_pal["Level"] >= 1)]["Level"].min()
    max_upg=df.loc[(df["Cost"] >= 1)]["Level to"].max()
    range_level_min, range_level_max = build_chart_bar(df_xls["DataFrame"][idx_costs],'Level from','Cost','Upgrade costs from level:',int(min_upg),int(max_upg))
    with st.expander(get_text_trad(site_langu,'data_graph'), expanded=False, width="stretch"):
        build_table_any(df.loc[(df['Level from'] >= range_level_min) & (df['Level to'] <= range_level_max)])    

def menu_tab_mut():
    st.header(df_xls["DisplayName"][idx_mut]) 
    df = df_xls["DataFrame"][idx_mut]
    df_energy=df.loc[(df['Step'] > 0)]
    df_crystal=df.loc[(df['Step'] == 0)]  
    st.subheader("🟢Energy")
    range_level_min, range_level_max = build_chart_bar(df_energy,'Level','Cost level','Mutation costs from level:',int(1),int(30))
    st.subheader("💎Crystals")
    build_chart_bar(df_crystal,'Level','Cost level','Mutation costs from level:',int(1),int(30),False)
    with st.expander(get_text_trad(site_langu,'data_graph'), expanded=False, width="stretch"):
        build_table_any(df_crystal.loc[(df['Level'] >= range_level_min) & (df['Level'] <= range_level_max)])
        build_table_any(df_energy.loc[(df['Level'] >= range_level_min) & (df['Level'] <= range_level_max)])

def menu_tab_val():
    rowval = st.columns(2,border=False, width="stretch")
    with rowval[0]:
        st.subheader(df_xls["DisplayName"][idx_val]) 
        build_table_full_costs(df_xls["DataFrame"][idx_val])
        #build_table_any(df_xls["DataFrame"][idx_val])
    with rowval[1]:
        st.subheader(df_xls["DisplayName"][idx_stars])
        df_stars=df_xls["DataFrame"][idx_stars].copy(deep=True)
        df_stars['Stars level']=df_stars['Stars level'].apply(lambda b: format_stars(b) )
        build_table_any(df_stars)       

def menu_tab_boss():
    rowval = st.columns(2,border=False, width="stretch")
    with rowval[0]:
        st.subheader(df_xls["DisplayName"][idx_stars]) 
        df_boss=df_xls["DataFrame"][idx_boss].copy(deep=True)
        df_boss['Stars']=df_boss['Stars'].apply(lambda b: format_stars(b) )
        df_boss['Total']=df_boss['Unit cost'].apply(lambda b: int(b)*int(5) )
        build_table_any(df_boss)
    with rowval[1]:
        st.subheader(df_xls["DisplayName"][idx_comp])
        try:
            df_boss_det=df_xls["DataFrame"][idx_boss_data].copy(deep=True)
            df_boss_det['Stars level']=df_boss_det['Stars'].apply(lambda b: format_stars(abs(b)) )
            df_boss_det['Skill']=df_boss_det['Type'].apply(lambda b: option_type[data_type['Type'].index(b)])
            st.dataframe(
                    df_boss_det,
                    column_config={
                        "Name": st.column_config.TextColumn("Name", pinned = True),
                        "Skill": st.column_config.TextColumn("Type", pinned = True),
                        "Type": None, #st.column_config.TextColumn("Type", pinned = False),
                        "Stars level": st.column_config.TextColumn("Stars level"),
                        "Stars": st.column_config.NumberColumn("Stars",format="compact"),
                        "Comp 1": None,
                        "Comp 2": None,
                        "Comp 3": None,
                        "Comp 4": None,
                        "Comp 5": None,
                        "URL": None,
                    },
                    hide_index=True,
                 )          
        except:
            st.empty()
            
def menu_tab_boss_detail():
    st.subheader(df_xls["DisplayName"][idx_boss_data])
    try:
        df_boss_det=df_xls["DataFrame"][idx_boss_data].copy(deep=True)
        #df_boss_det
        df_boss_det['Stars']=df_boss_det['Stars'].apply(lambda b: format_stars(b) )
        df_boss_det['Skill']=df_boss_det['Type'].apply(lambda b: option_type[data_type['Type'].index(b)])
        #build_table_any(df_boss_det)
        st.dataframe(
                df_boss_det,
                column_config={
                    "URL": st.column_config.ImageColumn("Base preview",width="large"),
                    "Name": st.column_config.TextColumn("Name", pinned = True),
                    "Skill": st.column_config.TextColumn("Type", pinned = True),
                    "Type": None, #st.column_config.TextColumn("Type", pinned = False),
                    "Stars level": st.column_config.NumberColumn("Stars level",format="compact"),
                    "Stars": st.column_config.TextColumn("Stars"),
                    "Comp 1": col_progress(mini=0,maxi=5,label="Comp 1",tooltip="Comp 1",numformat="%f"),
                    "Comp 2": col_progress(mini=0,maxi=5,label="Comp 2",tooltip="Comp 2",numformat="%f"),
                    "Comp 3": col_progress(mini=0,maxi=5,label="Comp 3",tooltip="Comp 3",numformat="%f"),
                    "Comp 4": col_progress(mini=0,maxi=5,label="Comp 4",tooltip="Comp 4",numformat="%f"),
                    "Comp 5": col_progress(mini=0,maxi=5,label="Comp 5",tooltip="Comp 5",numformat="%f"),                   
                },
                hide_index=True,
             )            
    except:
        st.empty()

@st.fragment
def menu_tab_palmons(df_source=None,with_event=True,with_expander=True):
    if df_source is None:
        st.subheader(df_xls["DisplayName"][idx_palmon])
        df = df_xls["DataFrame"][idx_palmon]
    else:
        df = df_source
    column='Type'
    options = st.multiselect(f"Filter values for {column}:", df[column].unique(), default=list(df[column].unique()))
    df = df[df[column].isin(options)]    
    df = df.sort_values(by=['Level','Achievement'],ascending=False,ignore_index=False)
    df['Type_txt']=df['Type']
    df['Type']=df['Type'].apply(lambda b: option_type[data_type['Type'].index(b)])
    df['Skill']=df['Skill'].apply(lambda b: option_skill[0] if b=='Attack' else option_skill[1]) 
    df['Upgradable']=df['Upgradable'].apply(lambda b: icon_upgradable(b)) 
    df_display=df[cols_palmon]
    event = None
    if with_expander:
        container=st.expander('List',expanded=True, width='stretch')
    else:
        container = st.container(border=False, width='stretch', height='content')
    with container:
        event = st.dataframe(
            df, 
            column_config=column_config_lst,
            on_select='rerun',
            selection_mode='single-row',
            hide_index=True,
            height='content'
        )
    if event is not None and with_event:
        show_details(event.selection.rows,df) 

def menu_tab_dashboards():
    col_border=False
    st.header(get_text_trad(site_langu,'dashboards'))
    df=df_xls["DataFrame"][idx_palmon]
    
    column='Type'
    try:
        options = st.multiselect(f"Filter values for {column}:", df[column].unique(), default=list(df[column].unique()))
        
        df1=df.copy()
        df1['Steps']=df['Step'].apply(lambda b: format_stars(b) )
        df1['Upgradable']=df1['Upgradable'].apply(lambda b: icon_upgradable(b)) 
        #df1['Skill']=df1['Skill'].apply(lambda b: icon_skill(b)) 
        df1['Type']=df1['Type'].apply(lambda b: option_type[data_type['Type'].index(b)]+b)
    
        df2=df.copy()
        df2=df2.iloc[:-1,:].sort_values(by=['Skill','Level','Achievement'],ascending=False)
        df=df1.iloc[:-1,:].sort_values(by=['Skill','Level','Achievement'],ascending=False,ignore_index=True)
    
        df2=df2[(df2['Level'] >= 100)]

        df_tcd1=df2.copy()
        df_tcd2=df2.copy()
        df_tcd3=df2.copy()
        df_tcd1=df_tcd1[["Type","Skill","Level"]]
        df_tcd2=df_tcd2[["Type","Skill","Level"]]
        df_tcd3=df_tcd3[["Type","Skill","Level"]]
        #df_tcd2.set_index('Type').groupby(['Type','Skill']).apply(lambda x: x['Level'].count(), include_groups=True).to_frame('Level')
        #df_tcd2.set_index('Type').groupby('Type').apply(lambda x: x['Level'].sum() / x['Level'].count(), include_groups=True).to_frame('Level')
        df_tcd2=df_tcd2.groupby(["Type", "Skill"]).agg("count").reset_index()
        df_tcd3=df_tcd3.groupby(["Type", "Skill"]).agg("mean").reset_index()
        
        df_a=df2.copy()
        df_d=df2.copy()
        df_a = df_a[df_a[column].isin(options)]
        df_d = df_d[df_d[column].isin(options)]    
        df_a = df_a[df2['Skill'].isin(['⚔ Attack','Attack','⚔ AttackAttack'])].head(7)
        df_d = df_d[df2['Skill'].isin(['🛡 Defend','Defend','🛡 DefendDefend'])].head(7)
        
        st.subheader('⚔ Attack top 7')
        df_a = apply_cols_icons(df_a)
        build_table_dashboard(df_a)
        #event_a = build_table_dashboard(df_a)
        #if event_a is not None:
        #    detail=event_a.selection.rows.copy()
        #    st.session_state["event_detail"]=event_a.selection.rows
        #    st.session_state["event_df"]=df_a
        #    #st.session_state["event_a"]=event_a.selection.rows
            #show_details(event_a.selection.rows,df_a,True)
            #event_a = None   
        #event_detail    st.session_state.event_detail
        st.subheader('🛡 Defend top 7')
        df_d = apply_cols_icons(df_d)
        build_table_dashboard(df_d)
        #event_d = build_table_dashboard(df_d)
        #if event_d is not None:
        #    st.session_state["event_detail"]=event_d.selection.rows
        #    st.session_state["event_df"]=df_d
            #st.session_state["event_d"]=event_d.selection.rows
            #show_details(event_d.selection.rows,df_d,True)
            #event_a = None
            #event_d = None  

        #if "event_detail" in st.session_state:
        #    if st.session_state.event_detail is not None:
        #        show_details(st.session_state.event_detail,st.session_state.event_df,True)
        #        del_session_variable("event_detail")
        #        del_session_variable("event_df")
        
        row_d1 = st.columns(2,border=col_border, width="stretch")
        with row_d1[0]:
            st.subheader('Average Level by Type')
            avg_lvl_df = df1.set_index('Type').groupby('Type').apply(lambda x: large_num_format(x['Level'].sum() / x['Level'].count()), include_groups=True).to_frame('Level')
            avg_lvl_df
            avg_lvl_df = df1.set_index('Type').groupby('Type').apply(lambda x: x['Level'].sum() / x['Level'].count(), include_groups=True).to_frame('Level')
            st.bar_chart(avg_lvl_df, y='Level', horizontal=True)
        
        with row_d1[1]:
            st.subheader('Average power by Type')
            avg_pwr_df = df1.set_index('Type').groupby('Type').apply(lambda x: large_num_format(x['RankPower'].sum() / x['Level'].count()), include_groups=True).to_frame('Power')
            avg_pwr_df  
            avg_pwr_df = df1.set_index('Type').groupby('Type').apply(lambda x: x['RankPower'].sum() / x['Level'].count(), include_groups=True).to_frame('Power')
            st.bar_chart(avg_pwr_df, y='Power', horizontal=True)        

        row_d2 = st.columns(2,border=col_border, width="stretch")
        with row_d2[0]:
            st.subheader('Average Skill')
            df_tcd1['Type']=df_tcd1['Type'].apply(lambda b: option_type[data_type['Type'].index(b)]+b)
            build_pivot_table(df_tcd1,'Level','Type','Skill')
        with row_d2[1]:
            st.subheader('Nb Palmons per type')
            df_tcd2['Type']=df_tcd2['Type'].apply(lambda b: option_type[data_type['Type'].index(b)]+b)
            build_main_chart(df_tcd2,None,'Type','Level')
            #build_pivot_table(df_tcd3,'Level','Type','Skill')
            #df_tcd2

    except:
        st.empty()
        
def menu_tab_graph():
    build_graph_select()

def menu_tab_downloads():
    #st.title(body="Download file data test", text_alignment="center")
    st.subheader("Choose local data (csv)")
    try:
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
    except:
        st.empty()
        
# ======================================================================================================
#
#    Definition Classes
#
# ======================================================================================================
class Animal: 
    def __init__(self, name, legs):
        self.name = name
        self.legs = legs
        
class Dog(Animal):
    def sound(self):
        print("Woof!")
#Yoki = Dog("Yoki", 4)
#print(Yoki.name) # => YOKI
#print(Yoki.legs) # => 4
#Yoki.sound()     # => Woof!

class Palmon:
    def __init__(self, name, data):
        self.name = name
        self.data = data
    def __repr__(self):
        return self.name       
    def get_type(self):
        try:
            ret_val=self.data.Type.values[0]+self.data.Type_txt.values[0]
            return ret_val
        except:
            return None
    def get_level(self):
        try:
            return int(self.data.Level)
        except:
            return None
    def get_image(self):
        try:
            return self.data.URL.values[0]
        except:
            return None

# ======================================================================================================
#
#    Test Classes
#
# ======================================================================================================
def testClass(name,df):
    return Palmon(name,df)

# ======================================================================================================
#
#    Definition PAGES
#
# ======================================================================================================
def pg_home():
    st.title(f"{app_title} App")
    #write_one_info(get_device_type())
    if df_xls["DisplayName"][idx_palmon] is not None:
        menu_build_tabs()
    else:
        file_err()
        
def pg_menu_0():
    menu_tab_show(0)

def pg_menu_150():
    menu_tab_dashboards()

def pg_menu_200():
    menu_tab_show(200)
    
def page1():
    st.title(f"{app_title} Info")
    write_one_info(f"is_mobile: {is_mobile()}")
    write_one_info(get_device_type())    

def page2():
    st.title("Server OS information")
    st.subheader("os.environ")
    df_os_environ = pd.DataFrame([dict(os.environ)]).T
    st.dataframe(df_os_environ,hide_index=False,height='content')
    st.subheader("os.sysconf_names")
    df_os_sysconf_names = pd.DataFrame([os.sysconf_names]).T
    st.dataframe(df_os_sysconf_names,
                 column_config={
                    "Parameter": st.column_config.TextColumn("Parameter", pinned = True),
                    "Value": st.column_config.SelectboxColumn("Value"),},
                 hide_index=False,
                 height='content')

def page3():
    st.subheader(f'{get_text_trad(site_langu,'info_file')}', divider=False)
    if st.session_state.uploaded_file is not None:
        obj_fle=st.session_state.uploaded_file
        fileinfo={
           get_text_trad(site_langu,'info_file_name'):obj_fle.name,
           get_text_trad(site_langu,'info_file_type'):obj_fle.type,
           get_text_trad(site_langu,'info_file_size'):large_num_format(obj_fle.size)
        }
        st.dataframe(
            fileinfo,
            height = "content",
            width = "content",
            selection_mode = "single-row",
            hide_index=False,
            ) 
        file = pd.ExcelFile(st.session_state.uploaded_file)
        if file is not None:
            option = st.selectbox(
                get_text_trad(site_langu,'wks'),
                file.sheet_names,
                index=None,
                placeholder=get_text_trad(site_langu,'wks_sel'),
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
    else:
        file_err()
       
def page4():
    #write_coming_soon()
    st.subheader('Options', divider=True)
    site_langu=st.session_state.site_langu
    if st.session_state.texts_trad is None:
        st.session_state.texts_trad = read_json_trads()
    if st.button("Load JSON"):
        st.session_state.texts_trad = read_json_trads()
    test_trad = get_text_trad(site_langu,'text_id')
    write_one_info(test_trad)
    st.divider()
    test_trad = get_text_trad(site_langu,'menu_home')
    write_one_info(test_trad)
    st.divider()
    st.button('Clear Cache', on_click=clear_cache)
    st.divider()
    container_xls = st.container(border=False, width='stretch', height='content')
    with container_xls:
        check_file_loaded()
    #st.query_params.get_all() #TypeError: QueryParamsProxy.get_all() missing 1 required positional argument: 'key'
    #st.query_params.to_dict()

def pg_options():
    st.button('Load JSON', on_click=read_json_trads)
    st.button('Clear Cache', on_click=clear_cache)
    st.divider()
    err_details=st.toggle('ShowErrorDetails', True)
    st.set_option('client.showErrorDetails', err_details)
    container_xls = st.container(border=False, width='stretch', height='content')
    with container_xls:
        check_file_loaded()
    
# ======================================================================================================
#
#    Start MAIN page
#
# ======================================================================================================
site_langu='en'
langu='en'

if st.session_state.texts_trad is None:
    st.session_state.texts_trad = read_json_trads()
if st.session_state.site_langu is None:
    st.session_state.site_langu = site_langu

app_title=get_text_trad(site_langu,'app_title')

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

run_every = '1s' if st.session_state.stream else None

if is_mobile():
    write_js_menu()

with st.sidebar:
    top_nav = st.toggle("Top navigation", False)
    nav_sections = st.toggle("Page sections", True)
    use_pics = st.toggle("Show images", True)
    range_langu = st.columns(2, vertical_alignment='center')
    with range_langu[0]:
        on = st.toggle("EN / FR")
    st.session_state.site_langu='fr' if on else 'en'
    site_langu=st.session_state.site_langu
    with range_langu[1]:
        pic(data_flags[site_langu],24)
    menu_load_excel()
    st.session_state.stream=st.toggle("Check loaded", False)

if site_langu != langu:
    #st.toast('RELOADING', icon='ℹ️️', duration='short')
    menu_load_excel(with_expander=False,getnewfile=False)
langu = st.session_state.site_langu

if use_pics:
    st.markdown("""
        <style>
        	[data-testid="stHeader"] {
        		background-image: linear-gradient(90deg, rgb(0, 102, 204), rgb(102, 255, 255));
        	}
        </style>""",
        unsafe_allow_html=True)

pages = {
    get_text_trad(site_langu,'menu_home'):[ 
        st.Page(pg_home, title=get_text_trad(site_langu,'menu_home_1'), icon="🏠"),
    ],
    get_text_trad(site_langu,'menu_resources'): [
        st.Page(pg_menu_0, title=get_text_trad(site_langu,'full_list'),icon="🗂️"),
        st.Page(pg_menu_150, title=get_text_trad(site_langu,'dashboards'),icon="📊"),
        st.Page(pg_menu_200, title=get_text_trad(site_langu,'download'),icon="📥"),
    ],
    get_text_trad(site_langu,'menu_info'): [
        st.Page(page1, title=get_text_trad(site_langu,'menu_info_device'),icon="📱" if is_mobile() else "💻"),
        st.Page(page2, title=get_text_trad(site_langu,'menu_info_os'),icon="🖥️"),
        st.Page(page3, title=get_text_trad(site_langu,'menu_info_file'),icon="📋"),
    ],
    get_text_trad(site_langu,'menu_param'): [
        st.Page(pg_options, title="Options",icon="⚙️"), #🛠️
    ],    
}
pg = st.navigation(
    pages if nav_sections else [page for section in pages.values() for page in section],
    position="top" if top_nav else "sidebar"
)
pg.run()    

#write_js_script()            
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
