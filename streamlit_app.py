import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import statistics
from openpyxl import load_workbook
import locale
import logging
import sys
import os
import json
from user_agents import parse
import extra_streamlit_components as stx    #https://github.com/Mohamed-512/Extra-Streamlit-Components
import matplotlib.pyplot as plt

from pictures import *
#sys.path.insert(0, "./tests")  # add "tests" path to search list
#import test_graph as gv
import graphviz

#from myproject.models import some_model
#Me-creator-cpu/test_excel/tests/test_graph.py

#GitHub 
from pathlib import Path
from github import Auth
from github import Github

#Import auto des modules
#It is important to import sys and set the directory path before you import the file.
#import sys
#import os
#sys.path.insert(0, os.path.abspath('relative/path/to/application/folder'))
#import [file]
#https://stackoverflow.com/questions/49039436/how-to-import-a-module-from-a-different-folder

#img.flag_en
#import platform
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

# ======================================================================================================
# Optimisations
# df["col"][row_indexer] = value ==> Use `df.loc[row_indexer, "col"] = values` instead
# ======================================================================================================

# Définitions variables
df_xls = None
local_xls='./data/PS - Estimation (version 1).xlsx'
#uploaded_file = None
excel_loaded=False
tabs_data=[]
tabs = None
global texts_trad
texts_trad = None
run_every = None

#def init_session():
pages_base={}
pages_add={}
if 'pages_base' not in st.session_state:
    st.session_state.pages_base = pages_base
if 'pages_add' not in st.session_state:
    st.session_state.pages_add = pages_add 

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
cols_data = ['Name','Type','Skill','Level','Upgradable','Step','Stars','Stock','Comp 1','Comp 2','Comp 3','Comp 4','Comp 5','Unused1','Star 1','Star 2','Star 3','Star 4','Star 5','Achievement','Needs','Unused2','Cost to max','Unused3','Unused4','RankPower','Rank','Team','Unused5','URL','URL Mutation','Unused6','Unused7','Mutation 1','Mutation 2','Unused8']
cols_exp = ['Level from', 'Level to', 'Cost']
cols_comp = ['Level from', 'Cost']
cols_mut = ['Level', 'Step', 'Substep', 'Cost level']
cols_mut_full = ['Cost type', 'Cost']
cols_stars = ['Stars level', 'Unit Cost', 'Total']
cols_boss = ['Stars level', 'Unit Cost', 'Total']
cols_boss_data = ['Name','Type', 'Level', 'Stars','Comp 1','Comp 2','Comp 3','Comp 4','Comp 5','URL']
cols_equip = ['Level', 'Opus pearls']
cols_equip_nov = ['Step', 'Name', 'Stars', 'Cost']
cols_traits = ['Category', 'Type', 'Sub type', 'Name', 'Level', 'Bonus', 'Unit']

df_pal_data=None
df_costs_exp=None
df_costs_comp=None
df_costs_mut=None
df_costs_mut_full=None
df_costs_stars=None
df_costs_boss=None
df_boss_data=None
df_equip_data=None
df_equip_nov=None
df_traits=None

idx_palmon=0
idx_costs=1
idx_comp=2
idx_mut=3
idx_val=4
idx_stars=5
idx_boss=6
idx_boss_data=7
idx_equip=8
idx_equip_nov=9
idx_traits=10
idx_cal=50
idx_info=60
#✨

data_init={"Value":[""]}

data = { #                    0                  1                  2                    3                4                        5                    6                    7                8                 9                       10
        "Worksheet":      ["Palmon_data",    "Tableaux",        "Tableaux",         "Tableaux",         "Valeurs",                "Stars",           "Valeurs",            "Valeurs",        "Valeurs",      "Equipement",          "Equipement"],
        "DisplayName":    ["Palmons",        "Upgrade costs",   "Competencies",     "Mutation costs",   "Upgrade full costs",     "Stars",           "Boss",               "Boss data",      "Equipments",   "Equipments Explorer", "Traits"],
        "Range":          ["A:AJ",           "A:C",             "H:I",              "N:Q",              "A:B",                    "A:C",             "D:E",                "H:Q",            "Z:AA",         "A:D",                 "F:L"],
        "SkipRows":       [0,                1,                 1,                  1,                  0,                        0,                 1,                    1,                1,              1,                     1],
        "UpToRow":        [46,               302,               31,                 224,                4,                        7,                 5,                    5,                12,             42,                    96],
        "DisplayColumns": [cols_data,        cols_exp,          cols_comp,          cols_mut,           cols_mut_full,            cols_stars,        cols_boss,            cols_boss_data,   cols_equip,     cols_equip_nov,        cols_traits],
        "DataFrame":      [df_pal_data,      df_costs_exp,      df_costs_comp,      df_costs_mut,       df_costs_mut_full,        df_costs_stars,    df_costs_boss,        df_boss_data,     df_equip_data,  df_equip_nov,          df_traits],
        "Description":    ["Full list",      "EXP per level",   "Any palmon type",  "UR only",          "Defined values",         "Omni UR costs",   "Upgrade costs",      "Boss details",   "Upgrade costs","Upgrade costs",       "Traits list"],
        "MenuParent":     [idx_palmon,       idx_cal,           idx_cal,            idx_cal,            idx_info,                 None,              idx_boss,             idx_boss,         idx_cal,        idx_cal,               idx_traits],
       }

#"DataFrame":      [pd.DataFrame(data_init),      pd.DataFrame(data_init),      pd.DataFrame(data_init),      pd.DataFrame(data_init),       pd.DataFrame(data_init),        pd.DataFrame(data_init),    pd.DataFrame(data_init),        pd.DataFrame(data_init),     pd.DataFrame(data_init),  pd.DataFrame(data_init)],

data_menu_rootv2={
        "m0":   "Palmons",
        "m50":  "Calculators",
        "m60":  "Informations",
        "m6":   "Boss"
        }

data_menu_v2={
        "m0":   {idx_palmon},                       #idx_palmon
        "m50":  {idx_costs,idx_comp,idx_mut},       #idx_cal
        "m60":  {idx_val,idx_equip,idx_equip_nov},  #idx_info
        "m6":   {idx_boss,idx_boss_data}            #idx_boss
        }

df_xls = pd.DataFrame(data)
data_flags={'en':flag_en,'fr':flag_fr}

option_skill=["⚔ Attack","🛡 Defend"]
data_skills={
    "Skill":["Attack","Defend"],
    "Icon":option_skill
}
data_skill_ico={"Attack":"⚔️","Defend":"🛡️"}
data_type={
    "Type":["Water",      "Fire",    "Electricity",    "Wood",    "Any"],
    "Icon":["💧",        "🔥",      "⚡",             "🪵",     "🌐"] ,
    "Color":["#2784F5","#F54927",    "#EEF527",    "#F57D27",    "#27F549"]
}
data_values={
    "Value":["Energy","Crystals","Pieces","Level300"],
    "Icon":["🟢",     "💎",     "🧩",    "🔝"],
}
map_values={"Energy":"🟢Energy",
            "Crystals":"💎Crystals",
            "Pieces":"🧩Pieces",
            "Level300":"🔝Level300" }
bonus_value={0:"",1:"",2:"",3:"+5%",4:"+10%",5:"+20%",6:"+25%",7:"+30%"}
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
column_config_team={
    "Name": st.column_config.TextColumn( "Name", pinned = True ),
    "Type": st.column_config.TextColumn( "Type", pinned = True ),
    "Skill": st.column_config.TextColumn( "Skill", pinned = True ),
    "Level":st.column_config.NumberColumn(width="small",format="compact"),
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

def key_menu(key):
    try:
        ret_val=data_menu_rootv2.get(key)
    except:
        ret_val=None
    return ret_val

def key_values(key,lst=data_menu_v2):
    try:
        ret_val=lst.get(key)
    except:
        ret_val=None
    return ret_val

def get_cell_value(d,src,ret,valsrc):
    #data_type.get("Color")[data_type["Type"].index("Fire")]
    try:
        return d.get(ret)[d[src].index(valsrc)]
    except:
        return None
def is_in_list(lst,val):
    try:
        if lst.index(val)>=0:
            return True
        else:
            return False
    except:
        return False

def on_tab_change():
    st.toast(f"You opened the {st.session_state.animal} tab.")
    with st.session_state.tabsv2:
    #with st.container(horizontal=True):
        st.write(f'This is the {st.session_state.animal}')

def on_dyntab_change():
    st.toast(f"You opened the {st.session_state.menuv2_tab} tab.")
    with st.session_state.tabsv2:
    #with st.container(horizontal=True):
        st.write(f'This is the {st.session_state.menuv2_tab}')
        data_menu_v2[st.session_state.menuv2_tab]

def build_menu_v2():
    cat, dog, owl = st.tabs(
        ["Cat", "Dog", "Owl"], on_change=on_tab_change, key="animal"
    )
    st.session_state.tabsv2=st.container(horizontal=True)
    with st.session_state.tabsv2:
        #st.empty()
        #st.write(f'Test build_menu_v2')
        dyntabs = test_menu_v2()
        lstdynsubtabs=[]
        st.divider()
        #dyn_tabs=st.tabs(["m0","m50","m60","m6"], on_change=on_dyntab_change, key="menuv2_tab")
        dyn_tabs=st.tabs(list(data_menu_rootv2.keys()), on_change=on_dyntab_change, key="menuv2_tab")
        for v in data_menu_rootv2.keys():
            lstdynsubtabs.append(data_menu_rootv2[v])
        lstdynsubtabs
        dynsubtabs=','.join(lstdynsubtabs)
        dynsubtabs
        test_dummy()
        return True
        dyn_subtabs=st.tabs(lstdynsubtabs, on_change=on_dyntab_change, key="menuv2_tab")

def test_menu_v2():    
    prev_m=None
    lstdyntabs=[]
    for m in data_menu_v2:
        st.write(f'menu={m}, value={key_values(m)}, nb tabs={len(key_values(m))}, name={key_values(m,data_menu_rootv2)}')
        lstdyntabs.append(m)
        for sm in key_values(m):
            subtab = df_xls["DisplayName"][sm]
            st.write(f'menu={m}, submenu={(sm)}, name={subtab}')
        if prev_m!=m:
            st.divider()
        prev_m=m
    return ','.join(lstdyntabs)

def test_liste_pages():
    #pages = {
    #    'Nom menu':[ 
    #        st.Page(target, title='Nom page', icon="🏠"),
    #        st.Page(target, title='Nom page', icon="🏠"),
    #    ],
    #}
    #menu_tab_show(idx)
    menu_parent=''
    menu_page=''
    lstpages_v2=[]  
    prev_m=None
    for m in data_menu_v2:
        menu_parent=key_values(m,data_menu_rootv2)
        st.write(f'menu={m}, value={key_values(m)}, nb tabs={len(key_values(m))}, name={key_values(m,data_menu_rootv2)}')
        for sm in key_values(m):
            subtab = df_xls["DisplayName"][sm]
            st.write(f'menu={m}, submenu={(sm)}, name={subtab}')
            #pg=st.Page(menu_tab_show(sm), title=subtab, icon="🏠")
            lstpages_v2.append(pg)
        if prev_m!=m:
            st.divider()
        prev_m=m
    #pages_v2={'menu v2':lstpages_v2}
    #pages=pages+pages_v2

def test_liste():
    prev_m=None
    for m in data_menu_v2:
        st.write(f'menu={m}, value={key_values(m)}, nb tabs={len(key_values(m))}, name={key_values(m,data_menu_rootv2)}')
        for sm in key_values(m):
            subtab = df_xls["DisplayName"][sm]
            st.write(f'menu={m}, submenu={(sm)}, name={subtab}')
        if prev_m!=m:
            st.divider()
        prev_m=m

def test_dummy():
    st.toast(f"Building Menu v2.")
    page_v2_idx_palmon      =st.Page(pg_v2_idx_palmon, title="Full list", icon=":material/security:")
    page_v2_dashboard       =st.Page(pg_menu_100, title=get_text_trad('dashboards'),icon="📊")

    page_v2_idx_costs       =st.Page(pg_v2_idx_costs, title="Upgrade costs", icon=":material/security:")
    page_v2_idx_comp        =st.Page(pg_v2_idx_comp, title="Competencies", icon=":material/security:")
    page_v2_idx_mut         =st.Page(pg_v2_idx_mut, title="Mutation costs", icon=":material/security:")
    
    page_v2_idx_val         =st.Page(pg_v2_idx_val, title="Upgrade full costs", icon=":material/security:")
    page_v2_idx_equip       =st.Page(pg_v2_idx_equip, title="Equipments", icon=":material/security:")
    page_v2_idx_equip_nov   =st.Page(pg_v2_idx_equip_nov, title="Equipments Explorer", icon=":material/security:")

    page_v2_idx_boss        =st.Page(pg_v2_idx_boss, title="Boss", icon=":material/security:")
    page_v2_idx_boss_data   =st.Page(pg_v2_idx_boss_data, title="Boss data", icon=":material/security:")

    menu_v2_m0  =[page_v2_idx_palmon,page_v2_dashboard]
    menu_v2_m50 =[page_v2_idx_costs,page_v2_idx_comp,page_v2_idx_mut]
    menu_v2_m60 =[page_v2_idx_val,page_v2_idx_equip,page_v2_idx_equip_nov]
    menu_v2_m6  =[page_v2_idx_boss,page_v2_idx_boss_data]

    settings = st.Page(pg_options, title="Settings v2", icon=":material/settings:")
    account_pages = [settings]
    page_dict_m0    = {}
    page_dict_m50   = {}
    page_dict_m60   = {}
    page_dict_m6    = {}

    page_dict_m0["Palmons"]         = menu_v2_m0
    page_dict_m50["Calculators"]    = menu_v2_m50
    page_dict_m60["Informations"]   = menu_v2_m60 #"Upgrades data"
    page_dict_m6["Boss"]            = menu_v2_m6

    #if len(page_dict) > 0:
    pages_add = page_dict_m0 | page_dict_m50 | page_dict_m60 | page_dict_m6
    st.session_state.pages_add = pages_add
    pg = st.navigation(page_dict_m0 | page_dict_m50 | page_dict_m60 | page_dict_m6)
    pg.run()
    st.toast(f"Menu v2.")
    #if st.query_params["first_key"] == "1":
    #st.query_params.first_key = 2
    #st.query_params.clear()

def pg_menu_dyn():
    if st.query_params['menu_id'] is not None:
        st.toast(f"st.query_params['menu_id'] is not None => {st.query_params['menu_id']}")
        menu_tab_show(int(st.query_params['menu_id']))
    else:
        st.toast(f"Aucun st.query_params")

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

def write_no_streamlit_link():
    #st.toast("Style applyed")
    hide_st_style = """
                    <style>
                    ._container_gzau3_1 _viewerBadge_nim44_23 {display:none;visibility: hidden;}
                    ._profileContainer_gzau3_53 {display:none;visibility: hidden;}
                    ._link_gzau3_10 {display:none;visibility: hidden;}
                    [data-testid="appCreatorAvatar"] {display:none;visibility: hidden;}
                    [data-testid="stToolbarActionButtonLabel"] {display:none;visibility: hidden;}
                    [data-testid="stToolbarActionButtonIcon"] {display:none;visibility: hidden;}
                </style>
                """
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
    msg_no_file=get_text_trad('no_file')
    return st.markdown(f":orange-badge[⚠️ {msg_no_file}]")

def write_info(msg,val):
    return st.markdown(f":orange-badge[{msg} : {val}]")

def write_one_info(msg):
    return st.info(f"{msg}", icon="ℹ️", width="stretch")

def write_debug_html(txt,color):
    st.markdown(f"{txt} <span style='color:{color}'>{color}</span>",
                        unsafe_allow_html=True)

def write_coming_soon():
    maintenance=st.container(border=False, width='stretch', height='content')
    with maintenance:
        st.subheader("Coming soon...", divider=False)
        st.image(img_maintenance, caption=None, width="content")
    return maintenance

def df_highlight(value,threshold):
    return "background-color: yellow;"

def df_highlight_cond(value,threshold):
    #https://discuss.streamlit.io/t/how-i-can-color-a-st-data-editor-cell-based-on-a-condition/114385/2
    # couleur sur condition
    return "background-color: yellow;" if value<threshold else None 
    #styled_df=df.style.applymap(highlight,threshold=4,subset=["rating"])
    #edited_df = st.data_editor(styled_df)    

def data_info(df):
    tabs_cols=df.columns.values.tolist()
    tabs_cols
    tabs_idx=df.index.tolist()
    tabs_idx    

def pic(pic_url=None,pic_width='content',force=False):
    bln=False
    if pic_url is not None and use_pics:
        bln=True
    if bln or force:
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
        try:
            df['URL'] = df['URL'].fillna('')
            #st.toast("df['URL'].fillna('')")
        except:
            df=df
        if show_table == True:
            with st.expander(xls_sheet, expanded=False, icon=':material/table_view:', width='stretch'):
                st.dataframe(df)
    except:
        df = None
    return df

def get_data(file,idx,show_table=False):
    # FutureWarning: ChainedAssignmentError: behaviour will change in pandas 3.0!
    # df["col"][row_indexer] = value
    # voir pour remplacer avec: df.loc[row_indexer, "col"] = values

    #df_xls["DataFrame"][idx]=get_data_from_excel(
    data_values=get_data_from_excel(
                                                xls_file=file,
                                                xls_sheet=df_xls["Worksheet"][idx],
                                                skip=df_xls["SkipRows"][idx],
                                                rng_cols=df_xls["Range"][idx],
                                                rng_rows=df_xls["UpToRow"][idx],
                                                rencols=df_xls["DisplayColumns"][idx],
                                                show_table=show_table
                                                )
    #df_xls.loc[idx, "DataFrame"] = None
    df_xls.loc[idx, "DataFrame"] = data_values
    if 1==2:
        row_debug = st.columns(2,border=True, width="stretch")
        with row_debug[0]:
            st.write('df_xls')
            df_xls.loc[idx, "DataFrame"]
        with row_debug[1]:
            st.write('data_values')
            data_values

def get_data_v0(file,idx,show_table=False):
    # FutureWarning: ChainedAssignmentError: behaviour will change in pandas 3.0!
    # df["col"][row_indexer] = value
    # voir pour remplacer avec: df.loc[row_indexer, "col"] = values

    #Try using '.loc[row_indexer, col_indexer] = value' instead, to perform the assignment in a single step.
    # au lieu de: df["foo"][df["bar"] > 5] = 100
    # utiliser: df.loc[df["bar"] > 5, "foo"] = 100
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
        return option_skill[data_skills['Skill'].index(value)]
    except:
        return value

def icon_upgradable(value):
    try:
        return '✅' if int(value)==1 else '🟥' 
    except:
        return '🟥'

def check_needs(value):
    try:
        if int(value)<0:
            return 0
        else:
            return int(value)
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
        #st.toast('JSON file loaded', icon='ℹ️️', duration='short')
    except:
        st.toast('Error loading JSON file', icon='🔴', duration='short')
    return json_data

def get_text_trad(textId='text_id'):
    ret_val = ''
    langu=st.session_state.site_langu
    try:
        texts_trad=st.session_state.texts_trad
        ret_val = texts_trad['data'][textId][0][langu]
    except:
        st.session_state.texts_trad = read_json_trads()
        ret_val=f'Trad err {textId}/{langu}'
    return ret_val

def get_text_trad_old(langu='en',textId='text_id'):
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
    df=get_df_idx(idx_palmon)
    if df is not None:
        return st.success(f'{now} - File loaded', icon="✅")
    else:
        return st.warning(f'{now} - File is NOT loaded', icon="⚠️")

def build_table_params(df):
    try:
        st.dataframe(df,
             column_config={
                0: st.column_config.TextColumn("Parameter", pinned = True),
                1: st.column_config.TextColumn("Value"),},
             hide_index=False,
             #height='content'
                    )    
    except:
        return st.empty()

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
      
def build_chart_bar(df_chart,xField,yField,sLabel,selMin=1,selMax=30,with_slider=True, with_switch=False):
    if df_chart is not None:
        switch_axis = False
        try:
            if with_switch:
                switch_axis = st.toggle(get_text_trad('switch_axis'))
        except:
            switch_axis = False
        x_Field = xField
        y_Field = yField
        if switch_axis:
            x_Field = yField
            y_Field = xField            
        #st.bar_chart(df_chart, x=x_Field, y=y_Field, stack=False)

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
            #df2=df_chart[['Level from',yField]]
            #df2['Selection']=df2.apply(lambda row: row['Cost'] if range_level_min <= row['Level from'] <= range_level_max else 0, axis=1)
            df2=df_chart[[xField,yField]]
            df2['Selection']=df2.apply(lambda row: row[yField] if range_level_min <= row[xField] <= range_level_max else 0, axis=1)
            
            st.bar_chart(df2, x=x_Field, y=[y_Field,'Selection'], color=["#0068c9", "#ff4b4b"], stack=False)            
            df = df_chart.loc[(df_chart[x_Field] >= int(range_level_min)) & (df_chart[x_Field] <= int(range_level_max))]
            total_txt=get_text_trad('total_nrj_cost')
            to_txt=get_text_trad('to')
            total_col = f"{total_txt} {range_level_min} {to_txt} {range_level_max}"
            try:
                st.markdown(f":orange-badge[{total_col} : {large_num_format(int(df[y_Field].sum()))}]")
            except:
                st.markdown(f":orange-badge[{total_col} : {int(df[y_Field].sum())}]")
            excel_loaded=True
            return range_level_min, range_level_max
        else:
            st.bar_chart(df_chart, x=x_Field, y=y_Field, stack=False)
            df = df_chart.loc[(df_chart[xField] >= int(selMin)) & (df_chart[xField] <= int(selMax))]
            total_txt=get_text_trad('total_cry_cost')
            to_txt=get_text_trad('to')
            total_col = f"{total_txt} {selMin} {to_txt} {selMax}"
            st.markdown(f":orange-badge[{total_col} : {int(df[yField].sum())}]")
            return selMin,selMax

def build_graph_select():
    st.set_page_config(
        layout="wide",
    )
    field_1 = 'Level' #get_text_trad('level') #'Level'
    field_2 = 'Stars' #get_text_trad('stars') #'Stars'
    on = st.toggle(f'{get_text_trad('switch_axis')} {field_1}/{field_2}')
    if on:
        field_x = field_2
        field_y = field_1
    else:
        field_x = field_1
        field_y = field_2

    df_srv=get_df_idx()
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

def obj_row(nb_cells=2,with_border=False):
    return st.columns(nb_cells,border=with_border, width="stretch")

def obj_multiselect(df,column):
    return st.multiselect(f"Filter values for {column}:", 
                          df[column].unique(), 
                          default=list(df[column].unique()))    

def get_df_base():
    try:
        #return get_df_idx(idx_palmon)
        idx=idx_palmon
        data_values=get_data_from_excel(xls_file=local_xls,
                                        xls_sheet=df_xls["Worksheet"][idx],
                                        skip=df_xls["SkipRows"][idx],
                                        rng_cols=df_xls["Range"][idx],
                                        rng_rows=df_xls["UpToRow"][idx],
                                        rencols=df_xls["DisplayColumns"][idx],
                                        show_table=False
                                        )        
        return data_values
    except:
        return None

def get_df_idx(idx=idx_palmon):
    try:
        #return get_df_idx(idx_palmon)
        data_values=get_data_from_excel(xls_file=local_xls,
                                        xls_sheet=df_xls["Worksheet"][idx],
                                        skip=df_xls["SkipRows"][idx],
                                        rng_cols=df_xls["Range"][idx],
                                        rng_rows=df_xls["UpToRow"][idx],
                                        rencols=df_xls["DisplayColumns"][idx],
                                        show_table=False
                                        )        
        return data_values
    except:
        return None

def get_df_idx_old_ko(idx=idx_palmon):
    try:
        return df_xls["DataFrame"][idx].copy(deep=True)
    except:
        return None

def data_to_tiles(df_data=None): 
    df_srv = get_df_idx() #get_df_base()
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

def build_table_dashboard(df,with_select=True):
    if with_select:
        return st.dataframe(
                    df[['Name','Type','Level','Upgradable','Steps','Achievement']],
                    column_config=column_config_lst,
                    on_select="rerun",
                    selection_mode="single-row",                    
                    hide_index=True,
                )
    else:   
        return st.dataframe(
                    df[['Name','Type','Level','Upgradable','Steps','Achievement']],
                    column_config=column_config_lst,
                    hide_index=True,
                )

def build_table_team(df):
    return st.dataframe(
                df[['Name','Type','Level','Steps']],
                column_config=column_config_team,
                hide_index=True,
            )

def get_team_simu(df_ref,teamNb=1,with_main=True):
    df_t1=df_ref.head(7*int(teamNb)).tail(7)
    if with_main:
        st.write(f'Team {teamNb}')
        build_table_team(df_t1)
    with st.expander('Details',expanded=False, width='stretch'):
        df_t1_tcd1=df_t1[["Type","Name"]].head(7).groupby(["Type"]).agg("count").reset_index()
        df_t1_tcd1["Bonus"]=df_t1_tcd1['Name'].apply(lambda b: key_values(b,bonus_value) )
        df_t1_tcd2=df_t1[["Type","Level"]].head(7).groupby(["Type"]).agg("mean").reset_index()
        df_t1_tcd3=df_t1[["Skill","Level"]].head(7).groupby(["Skill"]).agg("count").reset_index()
        st.dataframe(df_t1_tcd1,hide_index=True)
        st.dataframe(df_t1_tcd2,hide_index=True)
        st.dataframe(df_t1_tcd3,hide_index=True)    

def apply_col_iconame(name,skill,upg):
    #[:5]
    return  str(skill[:1])+str(upg[:1])+str(name)
    #return  str(name) + str(key_values(skill,data_skill_ico))

def apply_cols_icons(df):
    df['Steps']=df['Step'].apply(lambda b: format_stars(b) )
    df['Upgradable']=df['Upgradable'].apply(lambda b: icon_upgradable(b))
    #df['Skill']=df['Skill'].apply(lambda b: icon_skill(b)) 
    df['Type']=df['Type'].apply(lambda b: option_type[data_type['Type'].index(b)]+b)
    return df

def apply_cols_format(df):
    df['Steps']=df['Step'].apply(lambda b: format_stars(b) )
    df['Upgradable']=df['Upgradable'].apply(lambda b: icon_upgradable(b))
    df['Type']=df['Type'].apply(lambda b: option_type[data_type['Type'].index(b)]+b)
    df['Skill']=df['Skill'].apply(lambda b: icon_skill(b))     

def format_stars(x): #⭐
    try:
        return ("⭐" * int(x))[0:int(x)]
    except:
        return x

def calcul_upgrade_costs(from_lvl=1,to_lvl=300):
    df=get_df_idx(idx_costs)
    if df is not None:
        val_cost=df.loc[(df["Level from"] >= from_lvl) & (df["Level from"] <= to_lvl)]["Cost"].sum()
        return val_cost
    else:
        return None

def calcul_upgrade_comp_costs(from_lvl=1,to_lvl=30):
    if get_df_idx(idx_palmon) is not None:
        #df = df_xls["DataFrame"][idx_comp]
        #val_cost=df.loc[(df["Level from"] >= from_lvl) & (df["Level from"] <= to_lvl)]["Cost"].sum()
        val_cost=get_upgrade_comp_costs(from_lvl,to_lvl)
        return large_num_format(val_cost)
    else:
        return None

def get_upgrade_comp_costs(from_lvl=1,to_lvl=30):
    df=get_df_idx(idx_comp)
    if df is not None:
        val_cost=df.loc[(df["Level from"] >= from_lvl) & (df["Level from"] <= to_lvl)]["Cost"].sum()
        return int(val_cost)
    else:
        return None

def show_details(palmon,df,popup=False):
    #st.markdown(f":orange-badge[palmon : {palmon}]")
    df_costs = get_df_idx(idx_costs)
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

def on_paltab_change():
    #st.toast(f"You opened the {st.session_state.pal_type} tab.")
    tabid=data_type['Type'].index(st.session_state.pal_type)
    tabobj=get_session_variable('tab'+str(tabid))
    with tabobj:
        pal_per_type(st.session_state.pal_type)

def pal_view_types():
    df=get_df_idx(idx=idx_palmon)
    test=df['Type'].unique()
    tab1,tab2,tab3,tab4=st.tabs(data_type['Type'][:4], on_change=on_paltab_change, key="pal_type")
    #tab1,tab2,tab3,tab4=st.tabs(["Water","Fire","Wood","Electricity"], on_change=on_paltab_change, key="pal_type")
    for i in range(len(data_type['Type'])-1):
        tab_key='tab'+str(i)
        if get_session_variable(tab_key) is None:
            add_session_variable(tab_key,st.empty())

    if 1 == 2:
        #tab1,tab2,tab3,tab4=st.tabs(["Water","Fire","Wood","Electricity"], key="pal_type")
        if tab1.open:
            with tab1:
                pal_per_type(st.session_state.pal_type)
        if tab2.open:
            with tab2:
                pal_per_type(st.session_state.pal_type)
        if tab3.open:
            with tab3:
                pal_per_type(st.session_state.pal_type)
        if tab4.open:
            with tab4:
                pal_per_type(st.session_state.pal_type)           

def pal_per_type(type):
    df=get_df_idx(idx=idx_palmon)
    df=df.loc[(df["Type"] == type) & (df["Level"]>0)].sort_values(by=['Level','Achievement'],ascending=False,ignore_index=False)
    menu_tab_palmons(df_source=df,with_event=True,with_expander=False,with_select=False)

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

    df_cost = get_df_idx(idx_costs)
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
        try:
            df_info.loc[df.index[0], 'Achievement'] = percent_format(df_info.loc[df.index[0], 'Achievement'])
        except:
            df_info.loc[df.index[0], 'Achievement'] = df_info.loc[df.index[0], 'Achievement']
        try:
            df_info.loc[df.index[0], 'Cost to max'] = large_num_format(df_info.loc[df.index[0], 'Cost to max'])
        except:
            df_info.loc[df.index[0], 'Cost to max'] = df_info.loc[df.index[0], 'Cost to max']
        df_info=df_info.reset_index().T
        st.dataframe(df_info,
                    column_config={
                        "Achievement": col_progress(0,1,"Achievement","Achievement","percent"),                     
                     },
                     hide_index=False) 
    with row1[0]:
        st.metric("Level upgrade", level_pal, level_max)
    with row1[1]:
        df_costs = get_df_idx(idx_costs)
        max_upg=df_costs.loc[(df_costs["Cost"] >= 1)]["Level to"].max()
        cost_upg=calcul_upgrade_costs(df.loc[df.index[0], 'Level'],max_upg)
        st.metric("Cost", large_num_format(cost_upg), level_max)
    with row2[0]:
        st.write(get_text_trad('menu_calc_comp'))
        build_table_any(df[cols_comp])
    with row2[1]:
        st.write(get_text_trad('menu_calc_costs'))
        df_comp_u=df[cols_comp].convert_dtypes()
        df_comp_costs = get_df_idx(idx_costs)
        total_comp_costs=int(0)
        for i in [1,2,3,5]:
            comp_cost=int( get_upgrade_comp_costs( df_comp_u.loc[df.index[0], f'Comp {i}'],10 if i==5 else 30 ) )
            df_comp_u.loc[df.index[0], f'Comp {str(i)}']=int(comp_cost)
            #df_comp_u.loc[df.index[0], f'Comp {str(i)}']=str(large_num_format(comp_cost))
            total_comp_costs=total_comp_costs+comp_cost
            #df_comp_u.loc[df.index[0], f'Comp {i}']=calcul_upgrade_comp_costs( df_comp_u.loc[df.index[0], f'Comp {i}'],10 if i==5 else 30 )
        #total_comp_costs=get_upgrade_comp_costs( df_comp_u.loc[df.index[0], 0],30)
        #df_comp_u.loc[df.index[0], 'Comp 1']+df_comp_u.loc[df.index[0], 'Comp 2']
        build_table_any(df_comp_u[cols_comp])
        write_info('Total competencies cost',large_num_format(total_comp_costs))
    with row1[2]:
        st.metric("Competencies cost", large_num_format(total_comp_costs), 'Max')

def calc_dreamium():
    if 'updated_df' in st.session_state:
        df = st.session_state.updated_df
    else:
        df = pd.DataFrame(
            [
                {"dreamium": "I",   "level": 1, "quantity": 0, "calculated": '0'},
                {"dreamium": "II",  "level": 2, "quantity": 0, "calculated": '0'},
                {"dreamium": "III", "level": 3, "quantity": 0, "calculated": '0'},
                {"dreamium": "IV",  "level": 4, "quantity": 0, "calculated": '0'},
                {"dreamium": "V",   "level": 5, "quantity": 0, "calculated": '0'},
            ]
        )

    #styled_df=df.style.applymap(df_highlight,threshold=4,subset=["quantity"])
    pic(url_logo_03)
    st.subheader(get_text_trad('calc_dreamium'))
    edited_df = st.data_editor(
        df,
        #styled_df,
        column_config={
            "dreamium": "Dreamium",
            #"level": "Level",
            "level": None,
            "quantity": st.column_config.NumberColumn(
                "Input quantity",
                min_value=0,
                step=1,
                format="%d",
            ),
            "calculated":st.column_config.TextColumn("Calculated")
        },
        disabled=["dreamium", "level", "calculated"],
        hide_index=True,
        key="my_key",
        on_change=df_change,
        kwargs=dict(selected_rows=df),
        #kwargs=dict(selected_rows=styled_df),
    )
    #st.markdown(f"Your favorite command is **{favorite_command}** 🎈")

def calc_dreamium_final(df_source,df_input):
    rows = df_source.index.tolist()
    for i in rows:
        #df_source["calculated"][i]=str(df_source["quantity"][i])
        df_source.loc[i, "calculated"]=str(df_source["quantity"][i])
    
    for i in df_input:
        for l in rows:
            #calc_qty=df_source["calculated"][l].replace(' ','')
            calc_qty=str2number(df_source["calculated"][l])
            #df_source["calculated"][l]=large_num_format(calc_qty + df_input[i]["quantity"]*(4**(i-l)))
            df_source.loc[l, "calculated"]=large_num_format(calc_qty + df_input[i]["quantity"]*(4**(i-l)))
    st.session_state.updated_df=df_source

def str2number(val):
    try:
        t=str(val).replace(' ','')
        return int(t)
    except:
        return int(0)

def df_change(selected_rows):   
    input_df=st.session_state["my_key"]["edited_rows"]
    calc_dreamium_final(selected_rows,input_df)

# ======================================================================================================
#
#    Definition fonctions pages/menu
#
# ======================================================================================================
#./data/PS - Estimation (version 1).xlsx
def local_load_excel(getnewfile=True):
    if getnewfile:
        uploaded_file  = local_xls
        excel_loaded=False
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            file = pd.ExcelFile(uploaded_file)
            if file is not None:
                excel_loaded=True
            else:
                uploaded_file=None

        if get_df_idx(idx_costs) is not None:
            excel_loaded=True
            st.session_state.uploaded_file = uploaded_file
        else:
            excel_loaded=False
    else:
        uploaded_file = st.session_state.uploaded_file
    
    tabs_data=[]
    row, col = df_xls.shape
    for i in range(row):
        get_data(uploaded_file,i,False)
        if int(i)!=int(idx_stars):
            tabs_data.append(stx.TabBarItemData(id=i, 
                                                title=df_xls["DisplayName"][i], 
                                                description=df_xls["Description"][i], ) )
    add_session_variable("tabs_data",tabs_data)

def menu_load_excel(with_expander=True,getnewfile=True,expanded=False):
    if getnewfile:
        if with_expander:
            container=st.expander(get_text_trad('xls'), expanded=expanded, width="stretch")
        else:
            container=st.container(border=False, width='stretch', height='content')
        with container:
            uploaded_file  = st.file_uploader(get_text_trad('xls_sel'), type = 'xlsx')
            excel_loaded=False
            if uploaded_file is not None:
                st.session_state.uploaded_file = uploaded_file
                file = pd.ExcelFile(uploaded_file)
                if file is not None:
                    excel_loaded=True
                else:
                    uploaded_file=None
            expanded=False
            
        if get_df_idx(idx_costs) is not None:
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
    if get_df_idx(idx_palmon) is not None:
        idx_tab = idx
    else:
        if int(idx) < 100:
            idx_tab = 999
        else:
            idx_tab = idx

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
        case 8:    #idx_equip
            menu_tab_equip()
        case 9:    #idx_equip_nov
            menu_tab_equip_nov()
        case 10:   #idx_traits
            menu_tab_traits()
        case 100:
            menu_tab_dashboards()
        case 150:
            menu_tab_graph()
        case 200:
            menu_tab_downloads()
        case _:
            return file_err()

def menu_tab_comp():
    st.subheader(df_xls["DisplayName"][idx_comp])
    
    df = get_df_idx(idx_comp)
    range_level_min, range_level_max = build_chart_bar(df,'Level from','Cost','Competencies costs from level:',int(1),int(30))
    with st.expander(get_text_trad('data_graph'), expanded=False, width="stretch"):
        build_table_any(df.loc[(df['Level from'] >= range_level_min) & (df['Level from'] <= range_level_max)])

def menu_tab_costs():
    df = get_df_idx(idx_costs)
    df_pal=get_df_idx(idx_palmon)
    st.subheader(df_xls["DisplayName"][idx_costs])
    min_upg=df_pal.loc[(df_pal["Level"] >= 1)]["Level"].min()
    max_upg=df.loc[(df["Cost"] >= 1)]["Level to"].max()
    range_level_min, range_level_max = build_chart_bar(df,'Level from','Cost','Upgrade costs from level:',int(min_upg),int(max_upg))
    with st.container(horizontal_alignment="center", 
                      vertical_alignment="center", 
                      border=True):
        nb_pal=st.slider('Nb palmons', min_value=1, max_value=7, value=1, step=1)
        cost_unit=calcul_upgrade_costs(from_lvl=range_level_min,to_lvl=range_level_max)
        event_points=int(cost_unit)/int(2000)
        cost_nb=int(cost_unit)*int(nb_pal)
        event_points_nb=int(cost_nb)/int(2000)
        row1 = st.columns(3,border=False, width="stretch")
        row2 = st.columns(3,border=False, width="stretch")
        row3 = st.columns(3,border=False, width="stretch")
        with row1[0]:
            st.write(f"{get_text_trad('text_001')} {nb_pal} UR:")
        with row1[1]:
            st.write(large_num_format(cost_nb))
        with row2[0]:
            st.write(f"{get_text_trad('text_002')}")
        with row2[1]:    
            if event_points>=int(15000):
                st.markdown(f':green[{large_num_format(event_points)}]')
            else:
                st.write(large_num_format(event_points))
        with row3[0]:
            st.write(f"{get_text_trad('text_003')} {nb_pal} UR:")
        with row3[1]:
            if event_points_nb>=int(15000):
                st.markdown(f':green[{large_num_format(event_points_nb)}]')
            else:
                st.write(large_num_format(event_points_nb))
        
    with st.expander(get_text_trad('data_graph'), expanded=False, width="stretch"):
        build_table_any(df.loc[(df['Level from'] >= range_level_min) & (df['Level to'] <= range_level_max)])    

def menu_tab_mut():
    st.header(df_xls["DisplayName"][idx_mut]) 
    df = get_df_idx(idx_mut)
    df_energy=df.loc[(df['Step'] != 0)]
    df_crystal=df.loc[(df['Step'] == 0)]  
    st.subheader("🟢Energy")
    range_level_min, range_level_max = build_chart_bar(df_energy,'Level','Cost level','Mutation costs from level:',int(df_energy['Level'].min()),int(df_energy['Level'].max()))
    st.subheader("💎Crystals")
    build_chart_bar(df_crystal,'Level','Cost level','Mutation costs from level:',int(df_crystal['Level'].min()),int(df_crystal['Level'].max()),False)
    with st.expander(get_text_trad('data_graph'), expanded=False, width="stretch"):
        st.subheader("🟢Energy", divider="green")
        build_table_any(df_energy.loc[(df['Level'] >= range_level_min) & (df['Level'] <= range_level_max)])
        st.subheader("💎Crystals", divider="blue")
        build_table_any(df_crystal.loc[(df['Level'] >= range_level_min) & (df['Level'] <= range_level_max)])        

def menu_tab_equip():
    st.header("✨"+df_xls["DisplayName"][idx_equip]) 
    df = get_df_idx(idx_equip)
    range_level_min, range_level_max = build_chart_bar(df,'Level','Opus pearls','Costs from level:',int(df['Level'].min()),int(df['Level'].max()),with_slider=True, with_switch=False)
    with st.expander(get_text_trad('data_graph'), expanded=False, width="stretch"):
        build_table_any(df.loc[(df['Level'] >= range_level_min) & (df['Level'] <= range_level_max)])

def get_equip_nov_categ(val,part=1):
    s=str(val).split(" ", 1)
    if part==1:
        return s[0]
    else:
        if len(s)==1:
            v='0'
        else:
            v=s[1]
        return s[0],v

def menu_tab_equip_nov():
    st.header("✨"+df_xls["DisplayName"][idx_equip_nov]) 
    df = get_df_idx(idx_equip_nov)
    df
    lambda_steps = lambda x: str(x['Step']) + '.' + str(x['Stars'])
    lambda_name_ver = lambda x: (str(x['Name']).split(" ", 1)[0],str(str(x['Name'])+" ").split(" ", 1)[1])
    df['Steps'] = df.apply(lambda_steps, axis=1)
    df[['Category','Stage']]=df.apply(lambda_name_ver,axis=1, result_type='expand')
    #df['Steps']=df[['Step','Stars']].apply(lambda a,b: a+'.'+b)
    #df['Stage']=df['Name'].apply(lambda a: get_equip_nov_categ(a,2))
    df_g=df[['Step','Cost']].set_index('Step').groupby(["Step"]).agg("sum").reset_index()
    range_level_min, range_level_max = build_chart_bar(df_g,'Step','Costs','Costs from level:',int(df['Step'].min()),int(df['Step'].max()),with_slider=True, with_switch=False)
    opt_cat = obj_multiselect(df,'Category')
    with st.expander(get_text_trad('data_graph'), expanded=False, width="stretch"):
        df
        build_table_any(df.loc[(df['Step'] >= range_level_min) & (df['Step'] <= range_level_max) & (df["Category"].isin(opt_cat))])

def menu_tab_traits():
    st.header("🎓"+df_xls["DisplayName"][idx_traits]) 
    df = get_df_idx(idx_traits).fillna('%')
    df['Type']=df['Type'].apply(lambda b: icon_skill(b))
    with st.container(horizontal=True, horizontal_alignment="center"):
        opt_cat = obj_multiselect(df,'Category')
        opt_type = obj_multiselect(df,'Type')
        opt_level = obj_multiselect(df,'Level')    
    df_a=df.loc[(df["Type"].isin(opt_type)) & (df["Category"].isin(opt_cat)) & (df["Level"].isin(opt_level))].copy(deep=True)
    df_a["Unit"].fillna('pct')
    build_table_any(df_a)

def menu_tab_val():
    rowval = st.columns(2,border=False, width="stretch")
    with rowval[0]:
        st.subheader(df_xls["DisplayName"][idx_val]) 
        build_table_full_costs(get_df_idx(idx_val))
    with rowval[1]:
        st.subheader(df_xls["DisplayName"][idx_stars])
        df=get_df_idx(idx_stars)
        df_stars=df.copy(deep=True)
        df_stars = df_stars[:-1]
        df_stars['Stars level']=df_stars['Stars level'].apply(lambda b: format_stars(b) )
        df_stars.at['Total','Unit Cost']=df_stars['Unit Cost'].mean()
        df_stars.at['Total','Total']=df_stars['Total'].sum()
        df_stars.at['Total','Stars level']='Average / Total'
        build_table_any(df_stars)       

def menu_tab_boss():
    rowpic = st.columns([1,2,1],border=False, width="stretch")
    rowval = st.columns(2,border=False, width="stretch")
    with rowpic[1]:
        pic(img_menu_boss)
    with rowval[0]:
        df=get_df_idx(idx_boss)
        st.subheader(df_xls["DisplayName"][idx_stars]) 
        df_boss=df.copy(deep=True)
        df_boss['Stars']=df_boss['Stars'].apply(lambda b: format_stars(b) )
        df_boss['Total']=df_boss['Unit cost'].apply(lambda b: int(b)*int(5) )
        build_table_any(df_boss)
    with rowval[1]:
        st.subheader(df_xls["DisplayName"][idx_comp])
        try:
            df2=get_df_idx(idx_boss_data)
            df_boss_det=df2.copy(deep=True)
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
    pic(img_menu_boss)
    try:
        df=get_df_idx(idx_boss_data)
        df_boss_det=df.copy(deep=True)
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
def menu_tab_palmons(df_source=None,with_event=True,with_expander=True,with_select=True):
    if df_source is None:
        st.subheader(df_xls["DisplayName"][idx_palmon])
        df = get_df_idx(idx_palmon)
    else:
        df = df_source
    column='Type'
    if type(df)==type(3.14): #float
        return
    if with_select:
        #options = st.pills(f"Filter values for {column}:", df[column].unique(), selection_mode="multi", default=list(df[column].unique()))
        options = st.multiselect(f"Filter values for {column}:", df[column].unique(), default=list(df[column].unique()))
        lbl=get_text_trad('opt_owned')
        if st.toggle(f'{lbl}'):
            df=df.loc[(df["Level"]>0)]
    else:
        options = df[column].unique()
    df = df[df[column].isin(options)]    
    df = df.sort_values(by=['Level','Achievement'],ascending=False,ignore_index=False)
    df['Type_txt']=df['Type']
    df['Type']=df['Type'].apply(lambda b: option_type[data_type['Type'].index(b)])
    df['Skill']=df['Skill'].apply(lambda b: option_skill[0] if b=='Attack' else option_skill[1]) 
    df['Upgradable']=df['Upgradable'].apply(lambda b: icon_upgradable(b)) 
    df['Needs']=df['Needs'].apply(lambda b: check_needs(b)) 
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
    st.header(get_text_trad('dashboards'))
    df=get_df_idx(idx_palmon)

    column='Type'
    try:
        options = st.multiselect(f"Filter values for {column}:", df[column].unique(), default=list(df[column].unique()))
        df_pie=df.copy(deep=True)
        #df1=df.copy(deep=True)
        df1=get_df_idx(idx_palmon)
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
        
        st.subheader(f'⚔ {get_text_trad('dashboard_title_a')}')
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
        st.subheader(f'🛡 {get_text_trad('dashboard_title_b')}')
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
            st.subheader(get_text_trad('dashboard_avg_level'))
            avg_lvl_df = df1.set_index('Type').groupby('Type').apply(lambda x: large_num_format(x['Level'].sum() / x['Level'].count()), include_groups=False).to_frame('Level')
            avg_lvl_df
            avg_lvl_df = df1.set_index('Type').groupby('Type').apply(lambda x: x['Level'].sum() / x['Level'].count(), include_groups=False).to_frame('Level')
            st.bar_chart(avg_lvl_df, y='Level', horizontal=True)
        with row_d1[1]:
            st.subheader(get_text_trad('dashboard_avg_power'))
            avg_pwr_df = df1.set_index('Type').groupby('Type').apply(lambda x: large_num_format(x['RankPower'].sum() / x['Level'].count()), include_groups=False).to_frame('Power')
            avg_pwr_df  
            avg_pwr_df = df1.set_index('Type').groupby('Type').apply(lambda x: x['RankPower'].sum() / x['Level'].count(), include_groups=False).to_frame('Power')
            st.bar_chart(avg_pwr_df, y='Power', horizontal=True)        
    
        row_d2 = st.columns(2,border=col_border, width="stretch")
        with row_d2[0]:
            st.subheader(get_text_trad('dashboard_avg_skill'))
            df_tcd1['Type']=df_tcd1['Type'].apply(lambda b: option_type[data_type['Type'].index(b)]+b)
            build_pivot_table(df_tcd1,'Level','Type','Skill')
        with row_d2[1]:
            st.subheader(get_text_trad('dashboard_nb_type'))
            df_tcd2['Type']=df_tcd2['Type'].apply(lambda b: option_type[data_type['Type'].index(b)]+b)
            #build_main_chart(df_tcd2,None,'Type','Level')
            #build_pivot_table(df_tcd3,'Level','Type','Skill')
            df_tcd2 = df1.set_index('Type').groupby('Type').apply(lambda x: x['Level'].count(), include_groups=False).to_frame('Nb')
            df_tcd2
    
        row_d3 = st.columns(2,border=col_border, width="stretch")
        with row_d3[1]:
            df_tcd3 = df_pie.set_index('Type').groupby('Type').apply(lambda x: x['Level'].count(), include_groups=False).to_frame('Nb')
            donut1=build_graph_donut(df_tcd3,get_text_trad('dashboard_donut_pct'))
            donut1
        with row_d3[0]:
            df_tcd4 = df_pie.set_index('Type').groupby('Type').apply(lambda x: x['Level'].mean(), include_groups=False).to_frame('Nb')
            donut2=build_graph_donut(df_tcd4,get_text_trad('dashboard_donut_nb'))
            donut2
        
    except:
        st.empty() 
        
def build_graph_donut(df,titre):
    fig, ax = plt.subplots(1, 1, figsize=(4, 6))
    Labels = df.index.tolist()
    datas = df['Nb']
    range_colors = list(map(lambda x, y:  y , data_type['Type'], data_type['Color']))
    colors=range_colors[slice(len(Labels))]
    explode = list(map(lambda x:0.05, range(len(Labels))))
    plt.pie(datas, colors=colors, labels=Labels, autopct='%1.1f%%', pctdistance=0.85, 
            explode=explode, shadow={'ox': -0.03, 'edgecolor': '#DEDEDE', 'shade': 0.1})
            #shadow=True)
    
    # draw circle
    centre_circle=plt.Circle((0, 0), 0.70, fc='white')
    centre_text=plt.text(x=0, y=0, s=titre, color='black', size=10,ha='center',va='center_baseline')
    donut = plt.gcf()
    
    # Adding Circle in Pie chart
    donut.gca().add_artist(centre_circle)
    return donut

def menu_tab_graph():
    build_graph_select()

def menu_tab_downloads():
    #st.title(body="Download file data test", text_alignment="center")
    st.subheader("Choose local data (csv)")
    pic(url_logo_06)
    
    try:
        range_cols = st.columns(3)
        range_cols[0].download_button(
            #label="Palmons data",
            label=df_xls["DisplayName"][idx_palmon],
            data=get_df_idx(idx_palmon).to_csv().encode("utf-8"),
            file_name="base_data.csv",
            mime="text/csv",
            icon=":material/download:",
        )
        range_cols[1].download_button(
            #label="EXP costs",
            label=df_xls["DisplayName"][idx_costs],
            data=get_df_idx(idx_costs).to_csv().encode("utf-8"),
            file_name="exp_data.csv",
            mime="text/csv",
            icon=":material/download:",
        )
        range_cols[2].download_button(
            #label="COMP costs",
            label=df_xls["DisplayName"][idx_comp],
            data=get_df_idx(idx_comp).to_csv().encode("utf-8"),
            file_name="comp_data.csv",
            mime="text/csv",
            icon=":material/download:",
        ) 

        st.subheader("View local data")
        range_cols_view = st.columns(3)
        df=None
        with range_cols_view[0]:
            if st.button('View Base raw data'):
                df=get_df_idx(idx_palmon)
        with range_cols_view[1]:
            if st.button('View EXP raw data'):
                df=get_df_idx(idx_costs)
        with range_cols_view[2]:
            if st.button('View COMP raw data'):
                df=get_df_idx(idx_comp)
        if df is not None:
            st.dataframe(df,hide_index=True)            
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

def pg_v2_idx_palmon():
    menu_tab_show(idx_palmon)
def pg_v2_idx_costs():
    menu_tab_show(idx_costs)
def pg_v2_idx_comp():
    menu_tab_show(idx_comp)
def pg_v2_idx_mut():
    menu_tab_show(idx_mut)
def pg_v2_idx_val():
    menu_tab_show(idx_val)
def pg_v2_idx_equip():
    menu_tab_show(idx_equip)
def pg_v2_idx_equip_nov():
    menu_tab_show(idx_equip_nov)  
def pg_v2_idx_boss():
    menu_tab_show(idx_boss)
def pg_v2_idx_boss_data():
    menu_tab_show(idx_boss_data)

def pg_menu_0():
    menu_tab_show(0)
def pg_menu_050():    
    pal_view_types()
def pg_menu_100():
    menu_tab_show(100)
def pg_menu_200():
    menu_tab_show(200)

def pg_v2_calc_dreamium():
    calc_dreamium()  

def pg_simu_team():
    st.subheader(get_text_trad('menu_simu'))
    df=get_df_base().copy(deep=True).sort_values(by=['Level','Achievement'],ascending=False,ignore_index=False)
    lst_type=df['Skill'].unique()
    with st.container(horizontal=True, horizontal_alignment="center"):
        opt_skill = obj_multiselect(df,'Skill')
        opt_type = obj_multiselect(df,'Type')
    
    row_d0 = obj_row()
    with row_d0[0]:
        st.write(f'⚔️{lst_type[0]}')
        df_a=df.loc[(df["Type"].isin(opt_type)) & (df['Skill'].str.contains("Attack")) & (df["Level"]>0)].copy(deep=True)
        apply_cols_format(df_a)
        build_table_dashboard(df_a,False)        
    with row_d0[1]:
        st.write(f'🛡️{lst_type[1]}')    
        df_b=df.loc[(df["Type"].isin(opt_type)) & (df['Skill'].str.contains("Defend")) & (df["Level"]>0)].copy(deep=True)
        apply_cols_format(df_b)
        build_table_dashboard(df_b,False)
    
    st.subheader(f'🏆Team 1 simulation')
    row_d2 = obj_row()
    with row_d2[0]:
        st.write('⚔️Top Attack 4 & 🛡️Top Defend 3')
        df_simu=pd.concat([df_a.head(4), df_b.head(3)], ignore_index=True, sort=False)
        build_table_dashboard(df_simu,False)
        get_team_simu(df_simu,teamNb=1,with_main=False) 
    with row_d2[1]:
        st.write('💪Top 7')        
        df_result=df.loc[(df["Type"].isin(opt_type)) & (df["Skill"].isin(opt_skill)) & (df["Level"]>0)].copy(deep=True)
        apply_cols_format(df_result)
        build_table_dashboard(df_result.head(7),False)
        get_team_simu(df_result.head(7),teamNb=1,with_main=False)

    st.subheader('🔎Teams selection')
    df_ref=df.copy(deep=True)
    apply_cols_format(df_ref)
    df_ref['Name'] = df_ref.apply(lambda x: apply_col_iconame(x['Name'], x['Skill'],x['Upgradable']), axis=1)
    row_d4 = obj_row(4)
#pg_simu_team    
    with row_d4[0]:
        get_team_simu(df_ref,teamNb=1)
    with row_d4[1]:
        get_team_simu(df_ref,teamNb=2)
    with row_d4[2]:
        get_team_simu(df_ref,teamNb=3)
    with row_d4[3]:
        get_team_simu(df_ref,teamNb=4)

def pg_info_device():
    ico="📱" if is_mobile() else "💻"
    st.title(f"{ico}Device info")
    #pic(url_logo_03)
    write_one_info(f"is_mobile: {is_mobile()}")
    write_one_info(get_device_type())    

def pg_info_os():
    st.title("💻Server OS information")
    st.subheader("os.environ")
    df_os_environ = pd.DataFrame([dict(os.environ)]).T
    build_table_params(df_os_environ) 
    st.subheader("os.sysconf_names")
    df_os_sysconf_names = pd.DataFrame([os.sysconf_names]).T
    build_table_params(df_os_sysconf_names) 

def pg_info_file():
    st.subheader(f'📋{get_text_trad('info_file')}', divider=False)
    try:
        if st.session_state.uploaded_file is not None:
            obj_fle=st.session_state.uploaded_file
            fileinfo={
               get_text_trad('info_file_name'):obj_fle.name,
               get_text_trad('info_file_type'):obj_fle.type,
               get_text_trad('info_file_size'):large_num_format(obj_fle.size)
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
                    get_text_trad('wks'),
                    file.sheet_names,
                    index=None,
                    placeholder=get_text_trad('wks_sel'),
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
    except:
        st.empty()
       
def page4():
    #write_coming_soon()
    st.subheader('Options', divider=True)
    site_langu=st.session_state.site_langu
    if st.session_state.texts_trad is None:
        st.session_state.texts_trad = read_json_trads()
    if st.button("Load JSON"):
        st.session_state.texts_trad = read_json_trads()
    test_trad = get_text_trad('text_id')
    write_one_info(test_trad)
    st.divider()
    test_trad = get_text_trad('menu_home')
    write_one_info(test_trad)
    st.divider()
    st.button('Clear Cache', on_click=clear_cache)
    st.divider()
    container_xls = st.container(border=False, width='stretch', height='content')
    with container_xls:
        check_file_loaded()
        check_github_access()
    #st.query_params.get_all() #TypeError: QueryParamsProxy.get_all() missing 1 required positional argument: 'key'
    #st.query_params.to_dict()

def pg_options():
    pic(url_logo_01)
    st.subheader('Options', divider=True)
    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Excel file","JSON file","Maintain JSON","Errors","Others"], key="tab_option")
    with tab1:
        #Excel
        check_file_loaded()
        if st.button("Reload"):
            local_load_excel(True)       
    with tab2:
        #JSON
        st.button('Load JSON', on_click=read_json_trads)
        st.button('Clear Cache', on_click=clear_cache)
    with tab3:
        #Git JSON
        form_file_param(file_txt='./textes.json')
    with tab4:
        #Errors
        err_details=st.toggle('ShowErrorDetails', True)
        st.set_option('client.showErrorDetails', err_details)
    with tab5:
        #Others
        file_txt='./data/todo.txt'
        file_txt='./test_w_api.txt'
        with st.expander('Text file', expanded=False, icon=':material/table_view:', width='stretch'):
            if st.button("Load Text file"):
                st.text(test_read_txt(file_txt))
            if st.button("Update Text file"):
                test_append_txt(file_txt)
            if st.button("Write Text file"):
                test_write_txt(file_txt)
        with st.expander('Other', expanded=False, icon=':material/table_view:', width='stretch'):
            if st.button("Test listing"):
                test_listing()
            if st.button("Donut graph"):
                build_graph_donut_test()
            if st.button("Colors"):
                test_colors()
        with st.expander('Github', expanded=False, icon=':material/table_view:', width='stretch'):
            check_github_access()
            if st.button("Get issues"):
                test_github_issues()

def pg_options_old():
    pic(url_logo_01)
    with st.expander('JSON file', expanded=False, icon=':material/table_view:', width='stretch'):
        st.button('Load JSON', on_click=read_json_trads)
        st.button('Clear Cache', on_click=clear_cache)
    st.divider()
    err_details=st.toggle('ShowErrorDetails', True)
    st.set_option('client.showErrorDetails', err_details)
    container_xls = st.container(border=False, width='stretch', height='content')
    with container_xls:
        check_file_loaded()
    #container_txt = st.container(border=True, width='stretch', height='content')
    #with container_txt:
    file_txt='./data/todo.txt'
    file_txt='./test_w_api.txt'
    with st.expander('Form & Git', expanded=False, icon=':material/table_view:', width='stretch'):
        form_file_param(file_txt='./textes.json')
    with st.expander('Text file', expanded=False, icon=':material/table_view:', width='stretch'):
        if st.button("Load Text file"):
            st.text(test_read_txt(file_txt))
        if st.button("Update Text file"):
            test_append_txt(file_txt)
        if st.button("Write Text file"):
            test_write_txt(file_txt)
    with st.expander('Other', expanded=False, icon=':material/table_view:', width='stretch'):
        if st.button("Test listing"):
            test_listing()
        if st.button("Donut graph"):
            build_graph_donut_test()
        if st.button("Colors"):
            test_colors()
    with st.expander('Github', expanded=False, icon=':material/table_view:', width='stretch'):
        check_github_access()
        if st.button("Get issues"):
            test_github_issues()

def pg_test_menu_v2():
    build_menu_v2()

def pg_tips_img():
    st.subheader('Tips', divider=True)
    for x in os.listdir('.//data'):
        if x.startswith("Costs_") or x.startswith("Palmon_"):
            st.image('./data/'+x, caption=x)    
            
def test_listing():
    for x in os.listdir('.//data'):
        if x.endswith(".jpg"):
            st.badge(x, icon=":material/check:", color="green")
            st.image('./data/'+x, caption=x)
        else:
            st.text(x)


def build_graph_nodes(graph,df,parent,child):
    n=["skill+type"]
    df_g=df[[parent,child,'Type','Skill']]
    row, col = df_g.shape
    for r in range(row):
        p=df_g[parent][r]
        c=df_g[child][r]
        t=df_g['Skill'][r]
        color=get_cell_value(data_type,"Type","Color",p)
        if color is None:
            graph.edge(p, c)
        else:
            no_arrow=is_in_list(n,p+t)
            ico=get_cell_value(data_type,"Type","Icon",p)
            graph.node(c, data_skill_ico.get(t) + c, shape = "plaintext")
            graph.node(p, ico+p, style = "filled", color = color)          
            if no_arrow==False:
                graph.node(p+t, data_skill_ico.get(t), shape = "plaintext")   
                n.append(p+t)
    n=[]    

def build_graph_links_hier(df,parent,child):
    n=["skill+type"]
    graph = graphviz.Digraph(graph_attr={'rankdir':'LR','layout':'neato'}) #option_type
    df_sorted=df.sort_values(by=['Type','Skill','Mutation 2','Mutation 1'],ascending=True,ignore_index=False)
    df_g=df_sorted[[parent,child]]
    df_sorted

    #build_graph_nodes(graph,df,parent,child)
    #build_graph_nodes(graph,df_sorted,'Name','Mutation 1')
    #build_graph_nodes(graph,df_sorted,'Mutation 1','Mutation 2')

    row, col = df_g.shape
    for r in range(row):
        p=df_g[parent][r]
        c=df_g[child][r]
        t=df_sorted['Skill'][r]
        m1=df_sorted['Mutation 1'][r]
        m2=df_sorted['Mutation 2'][r]

        color=get_cell_value(data_type,"Type","Color",p)
        if color is None:
            graph.edge(p, c)
        else:
            no_arrow=is_in_list(n,p+t)
            ico=get_cell_value(data_type,"Type","Icon",p)
            ico_skill=data_skill_ico.get(t)
            graph.node(c, ico_skill+c, shape = "plaintext")
            graph.node(p, ico+p, style = "filled", color = color) 
            st.write(p,c,t,m1,m2) 
            if no_arrow==False:
                graph.node(p+t, ico_skill, shape = "plaintext")   
                graph.edge(p, p+t, style = "filled", color = color)
                n.append(p+t)
            if m2!='Non':         #Mutation 2 existe
                if m1!='Non':     #Mutation 1 existe
                    graph.edge(m1, m2, style = "filled", color = color)
            #        graph.node(m2, m1, shape = "plaintext")
            #        graph.edge(m2, m1, style = "filled", color = color)
                else:           #Mutation 2 existe mais pas de Mutation 1
                    graph.edge(c, m2, style = "filled", color = color)
            #        graph.node(m2, m2, shape = "plaintext")
            #        graph.edge(m2, c, style = "filled", color = color)
            else:               #Aucune Mutation
                graph.edge(p+t, c, style = "filled", color = color)
            #graph.edge(p+t, c, style = "filled", color = color)

    n=[]
    return st.graphviz_chart(graph)

def build_graph_data(df):
    df
    row, col = df.shape
    nodes=[] #Parent / Child
    node={"parent":"","child":"","type":"","color":"","typeico":"","skillico":""}
    for r in range(row):
        ptype=df['Type'][r]
        color=get_cell_value(data_type,"Type","Color",ptype)
        ptypeico=get_cell_value(data_type,"Type","Icon",ptype)
        skillico=data_skill_ico.get(df['Skill'][r])
        if df['Mutation 1'][r]!='Non':
            node['parent']=df['Name'][r]
            node['child']=df['Mutation 1'][r]
            node['type']=ptype
            node['color']=color
            node['typeico']=ptypeico
            node['skillico']=skillico
            nodes.append(node)
        if df['Mutation 2'][r]!='Non':
            if df['Mutation 1'][r]!='Non':
                node['parent']=df['Mutation 1'][r]
                node['child']=df['Mutation 2'][r]
                node['type']=ptype
                node['color']=color
                node['typeico']=ptypeico
                node['skillico']=skillico
                nodes.append(node)
            else:
                node['parent']=df['Name'][r]
                node['child']=df['Mutation 2'][r]
                node['type']=ptype
                node['color']=color
                node['typeico']=ptypeico
                node['skillico']=skillico
                nodes.append(node)
        node['parent']=df['Type'][r]
        node['child']=df['Skill'][r]
        node['type']=ptype
        node['color']=color
        node['typeico']=ptypeico
        node['skillico']=skillico
        nodes.append(node)
        node['parent']=df['Skill'][r]
        node['child']=df['Name'][r]
        node['type']=ptype
        node['color']=color
        node['typeico']=ptypeico
        node['skillico']=skillico
        nodes.append(node)

    st.write(nodes)


def build_graph_links(df,parent,child):
    n=["skill+type"]
    graph = graphviz.Digraph(graph_attr={'rankdir':'LR','layout':'neato'}) #option_type
    df_g=df[[parent,child]]
    row, col = df_g.shape
    for r in range(row):
        p=df_g[parent][r]
        c=df_g[child][r]
        t=df['Skill'][r]
        m=df['Mutation 1'][r]
        color=get_cell_value(data_type,"Type","Color",p)
        if color is None:
            graph.edge(p, c)
        else:
            no_arrow=is_in_list(n,p+t)
            ico=get_cell_value(data_type,"Type","Icon",p)
            graph.node(c, data_skill_ico.get(t) + c, shape = "plaintext")
            graph.node(p, ico+p, style = "filled", color = color)          
            if no_arrow==False:
                graph.node(p+t, data_skill_ico.get(t), shape = "plaintext")   
                graph.edge(p, p+t, style = "filled", color = color)
                n.append(p+t)
            graph.edge(p+t, c, style = "filled", color = color)
    n=[]
    return st.graphviz_chart(graph)

def pg_tests_df():
    idx=idx_palmon
    st.write('get_df_idx')
    df1=get_df_idx(idx_palmon)
    df1
    st.divider()
    avg_lvl_df = df1.set_index('Type').groupby('Type').apply(lambda x: x['Level'].sum() / x['Level'].count(), include_groups=False).to_frame('Level')
    avg_lvl_df

def pg_tests():
    #st.empty()
    df=get_df_idx()
    #dot=build_graph_links(df,'Type','Name')
    build_graph_data(df)
    
@st.fragment(run_every="1s")
def test_colors():
    color_r = st.slider("Red value", 0, 255, 25)
    color_g = st.slider("Green value", 0, 255, 25)
    color_b = st.slider("Blue value", 0, 255, 25)
    rgb_hex=rgb2hex(color_r,color_g,color_b)
    write_info('rgb_hex',rgb_hex)
    df = pd.DataFrame(
        {
            "col1": (0,1),
            "col2": (1,1),
            "col3": (rgb_hex,rgb_hex),
        }
    )
    st.area_chart(
        df,
        x="col1",
        y="col2",
        color="col3",
    )

def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

@st.fragment(run_every="1s")
def check_github_access():
    if 'REPLICATE_API_TOKEN' in st.secrets.tests:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets.tests.REPLICATE_API_TOKEN
    else:
        st.warning('No API key provided!', icon='⚠️')

    if 'DB_TOKEN' in st.secrets:
        st.success('DB_TOKEN key already provided!', icon='✅')
        replicate_api = st.secrets['DB_TOKEN']
    else:
        st.warning('No DB_TOKEN key provided!', icon='⚠️')    

def test_read_txt(file_txt):
    data_txt=''
    with open(file_txt, mode='r') as f:
        data_txt = f.read()
    return data_txt

def test_append_txt(file_txt):
    try:
        with open(file_txt, mode='a') as f:
            f.write("Hello again\n")
            f.flush()
            f.close()
        return st.success('update OK', icon='✅')
    except:
        return st.error('update KO', icon='🚨')

def form_file_param(file_txt='data/todo.txt'):
    #get_text_trad('download')
    raw_data_txt=open(file_txt, mode='r').read()
    data_txt=''
    if raw_data_txt is not None:
        textsplit = raw_data_txt.splitlines()
        for x in textsplit:
            data_txt += f'{x}\n'
    lbl=get_text_trad('file_update')
    form_file_update = st.form('form_file_update')
    with form_file_update:
        txt_update = st.text_area(
            label=f'{lbl} {file_txt}',
            value=data_txt,
            label_visibility='visible',
            height='content'
            )
    submit = form_file_update.form_submit_button('Update')

    if submit:
        update_file_param(file_txt=file_txt,content=txt_update)

def update_file_param(file_txt='data/todo.txt',content=None):
    retval = False
    if content is not None:
        upd_file_txt=file_txt
        github_token = st.secrets.tests.REPLICATE_API_TOKEN
        auth = Auth.Token(github_token)
        g = Github(auth=auth)
        org_name = "Me-creator-cpu"
        repo_name = "test_excel"
        repo_branch = "main"
        repo = g.get_repo(f"{org_name}/{repo_name}")
        contents = repo.get_contents(upd_file_txt, ref=repo_branch)
        if 1 == 2:
            new_text=test_read_txt(file_txt)
            new_text+="This is the 1st line to write...\n"
            new_text+="This is the 2nd line to write...\n"
        new_text=str(content)
        try:
            repo_upd_result=repo.update_file(contents.path, "committing files", new_text, contents.sha, branch=repo_branch)
            repo_upd_result
            container_git = st.container(border=False, width='stretch', height='content')
            with container_git:
                st.success('write OK', icon='✅')
                test_read_txt(file_txt)
                read_json_trads(sFile=file_txt)
        except:
            st.error('write KO', icon='🚨')        
        retval = True
    else:
        retval = False
    return retval

def test_write_txt(file_txt='data/todo.txt'):
    upd_file_txt=file_txt #'data/todo.txt'
    github_token = st.secrets.tests.REPLICATE_API_TOKEN
    auth = Auth.Token(github_token)
    g = Github(auth=auth)
    org_name = "Me-creator-cpu"
    repo_name = "test_excel"
    repo_branch="main"
    repo = g.get_repo(f"{org_name}/{repo_name}")
    contents = repo.get_contents(upd_file_txt, ref=repo_branch)
    new_text=test_read_txt(file_txt)
    new_text+="This is the 1st line to write...\n"
    new_text+="This is the 2nd line to write...\n"
    try:
        repo_upd_result=repo.update_file(contents.path, "committing files", new_text, contents.sha, branch=repo_branch)
        repo_upd_result
        container_git = st.container(border=False, width='stretch', height='content')
        with container_git:
            st.success('write OK', icon='✅')
            test_read_txt(file_txt)
    except:
        st.error('write KO', icon='🚨')
    #try:
    #    with open(file_txt, mode='w') as f:
    #        f.write("This is the 1st line to write...\n")
    #        f.write("This is the 2nd line to write...\n")
    #        f.close()
    #    return st.success('write OK', icon='✅')
    #except:
    #    return st.error('write KO', icon='🚨')
    

def test_github_repo():
    #test_github.py
    st.empty()

# ======================================================================================================
def build_graph_donut_test():
    rowval = st.columns(2,border=False, width="stretch")
    with rowval[0]:
        # create data
        size_of_groups=[12,11,3,30]
        
        # Create a pieplot
        plt.pie(size_of_groups)
        #figsize(float, float), default: rcParams["figure.figsize"] (default: [6.4, 4.8])
        
        # add a circle at the center to transform it in a donut chart
        my_circle=plt.Circle( (0,0), 0.8, color='white')
        my_text=plt.text(x=0, y=0, s='Test', color='black', size=10,ha='center',va='center_baseline')
        #https://matplotlib.org/stable/api/text_api.html#matplotlib.text.Text
        #s works, text does not (matplotlib==3.2.2)
        #text works, s does not (matplotlib==3.5.1)
    
        p=plt.gcf()
        p.set_size_inches(3.2, 2.4)
        p.gca().add_artist(my_circle)
        
        p
        #plt.show()

    with rowval[1]:
        #https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_and_donut_labels.html
        #https://www.geeksforgeeks.org/python/donut-chart-using-matplotlib-in-python/
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        
        recipe = ["225 g flour",
                  "90 g sugar",
                  "1 egg",
                  "60 g butter",
                  "100 ml milk",
                  "1/2 package of yeast"]
        
        data = [225, 90, 50, 60, 100, 5]
        
        wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)
        
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")
        
        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = f"angle,angleA=0,angleB={ang}"
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                        horizontalalignment=horizontalalignment, **kw)
        
        ax.set_title("Matplotlib bakery: A donut")
        fig
    
    rowval2 = st.columns(2,border=False, width="stretch")
    with rowval2[0]:
         st.empty()
    with rowval2[1]:
        # Setting labels for items in Chart
        Employee = ['Roshni', 'Shyam', 'Priyanshi', 'Harshit', 'Anmol']
        Labels = Employee.copy()
        
        # Setting size in Chart based on given values
        Salary = [40000, 50000, 70000, 54000, 44000]
        
        # colors
        colors = ['#FF0000', '#0000FF', '#FFFF00', '#ADFF2F', '#FFA500']
        # explosion
        explode = (0.05, 0.05, 0.05, 0.05, 0.05)
        
        # Pie Chart
        plt.pie(Salary, colors=colors, labels=Employee,
                autopct='%1.1f%%', pctdistance=0.85,
                explode=explode)
        
        # draw circle
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig2 = plt.gcf()
        
        # Adding Circle in Pie chart
        fig2.gca().add_artist(centre_circle)
        
        # Adding Title of chart
        plt.title('Employee Salary Details')
        
        # Displaying Chart
        fig2
        
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

app_title=get_text_trad('app_title')
#app_title='Application pour Eva 🥰'

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
    top_nav = st.toggle(get_text_trad('side_nav'), False)
    nav_sections = st.toggle(get_text_trad('side_page'), True)
    use_pics = st.toggle(get_text_trad('side_pics'), False)
    range_langu = st.columns(2, vertical_alignment='center')
    with range_langu[0]:
        on = st.toggle("EN / FR")
    st.session_state.site_langu='fr' if on else 'en'
    site_langu=st.session_state.site_langu
    with range_langu[1]:
        pic(data_flags[site_langu],24,force=True)
    menu_load_excel()
    st.session_state.stream=st.toggle(get_text_trad('side_file'), False)



if site_langu != langu:
    #st.toast('RELOADING', icon='ℹ️️', duration='short')
    menu_load_excel(with_expander=False,getnewfile=False)
langu = st.session_state.site_langu

local_load_excel()

if use_pics:
    st.markdown("""
        <style>
        	[data-testid="stHeader"] {
        		background-image: linear-gradient(90deg, rgb(0, 102, 204), rgb(102, 255, 255));
        	}
        </style>""",
        unsafe_allow_html=True)

write_no_streamlit_link()
#🧮📱
pages = {
    get_text_trad('menu_home'):[ 
        st.Page(pg_home, title=get_text_trad('menu_home_1'), icon="🏠"),
    ],
    get_text_trad('menu_myteam'):[ 
        st.Page(pg_menu_0, title=get_text_trad('full_list'),icon="🗂️"),
        #st.Page(pg_menu_050, title='Per type',icon="🗂️"),
        st.Page(pg_menu_100, title=get_text_trad('dashboards'),icon="📊"),
    ],
    get_text_trad('menu_calc'):[
        st.Page(pg_v2_idx_costs, title=get_text_trad('menu_calc_costs'), icon="💰"),
        st.Page(pg_v2_idx_comp, title=get_text_trad('menu_calc_comp'), icon="🎓"),
        st.Page(pg_v2_idx_mut, title=get_text_trad('menu_calc_mut'), icon="🧬"),
        st.Page(pg_simu_team, title=get_text_trad('menu_simu'), icon="📐"),
        st.Page(pg_v2_calc_dreamium, title=get_text_trad('menu_calc_dream'), icon="💎"),
    ],
    get_text_trad('menu_upg'):[
        st.Page(pg_v2_idx_val, title=get_text_trad('menu_upg_costs'), icon="🚀"),
        st.Page(pg_v2_idx_equip, title=get_text_trad('menu_upg_equip'), icon="🧰"),
        st.Page(pg_v2_idx_equip_nov, title=get_text_trad('menu_upg_nov'), icon="🎒"),
    ],
    get_text_trad('menu_boss'):[
        st.Page(pg_v2_idx_boss, title=get_text_trad('menu_boss_all'), icon="🐦‍🔥"),
        st.Page(pg_v2_idx_boss_data, title=get_text_trad('menu_boss_data'), icon="🗂️"),
    ],
    get_text_trad('menu_resources'): [
        st.Page(pg_tips_img, title=get_text_trad('menu_tips'),icon="🌟"),
        st.Page(pg_menu_200, title=get_text_trad('download'),icon="📥"),
    ],
    get_text_trad('menu_info'): [
        st.Page(pg_info_device, title=get_text_trad('menu_info_device'),icon="📱" if is_mobile() else "💻"),
        st.Page(pg_info_os, title=get_text_trad('menu_info_os'),icon="🖥️"),
        st.Page(pg_info_file, title=get_text_trad('menu_info_file'),icon="📋"),
    ],
    get_text_trad('menu_param'): [
        st.Page(pg_options, title=get_text_trad('menu_options'),icon='⚙️'), #🛠️
        st.Page('./git_translations.py', title=get_text_trad('menu_git_translate'),icon='🛠️'),
    ],
    "Tests": [
        st.Page(pg_tests_df, title='Tests DF',icon='🛠️'),
        st.Page(pg_tests, title='Tests',icon='🛠️'),
        st.Page('./tests/test_eval.py', title='Tests EVAL',icon='🛠️'),
        st.Page('./tests/test2_github.py', title='Test Github',icon='🛠️'),
        st.Page('./tests/test_graph.py', title='Test graphviz',icon='🛠️'),
        st.Page(pg_test_menu_v2, title='Test Menu v2',icon='🛠️')
    ],    
}
st.session_state.pages_base = pages

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