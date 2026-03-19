import streamlit as st
import pandas as pd
from pandas import json_normalize
from datetime import datetime, timedelta
from pathlib import Path
from github import Auth
from github import Github
import base64
import json
from collections import defaultdict


json_file='./textes.json'
site_langu='en'
if 'site_langu' in st.session_state:
    site_langu=st.session_state.site_langu

def write_data(sInfo, data):
    with st.expander(f'{sInfo}', expanded=False, icon=':material/table_view:',width='stretch',height='content'):
        data

def get_text_trad(langu='en',textId='text_id'):
    ret_val = ''
    try:
        texts_trad=st.session_state.texts_trad
        ret_val = texts_trad['data'][textId][0][langu]
    except:
        ret_val=f'Trad err {textId}/{langu}'
    return ret_val

def git_read_file(fileName):
    try:
        with open(fileName) as data:
            content = data.read()
            st.write(f'content is: {content}') 
            return content  
    except:
        content = 'Test content'
        return content  

def form_file_param(file_txt='data/todo.txt'):
    raw_data_txt=open(file_txt, mode='r').read()
    data_txt=''
    if raw_data_txt is not None:
        textsplit = raw_data_txt.splitlines()
        for x in textsplit:
            data_txt += f'{x}\n'
    try:
        lbl=get_text_trad(site_langu,'file_update')
    except:
        lbl='Translations'
    #with st.expander(f'{lbl}', expanded=False, icon=':material/table_view:',width='stretch',height='content'):
    form_file_update = st.form('form_file_update',width='stretch',height='stretch')
    height = st.slider("Set the height of the text area", 100, 1000, 400)
    with form_file_update:
        txt_update = st.text_area(
            label=f'{lbl} {file_txt}',
            value=data_txt,
            label_visibility='visible',
            height=int(height)
            )
    #submit = form_file_update.form_submit_button('Update')
    submit = form_file_update.form_submit_button(get_text_trad(site_langu,'btn_update'))
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
        new_text=str(content)
        try:
            repo_upd_result=repo.update_file(contents.path, "committing files", new_text, contents.sha, branch=repo_branch)
            repo_upd_result
            container_git = st.container(border=False, width='stretch', height='stretch')
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

def subTitle(txt):
    st.subheader(f'{txt}', divider=True)           

def json_to_frame():
    with open(json_file, encoding='utf-8', errors='ignore') as f:
        json_data = json.load(f, strict=False) 
    df = pd.DataFrame(json_data['data'])    

    df3=pd.DataFrame(json_data['data']).T.copy()
    df3.index.name = "textid"
    df3.rename(columns={df3.columns[0]: "langu"}, inplace=True)
    
    df3['en']=df3['langu'].apply(lambda b: json_langu(b,'en'))
    df3['fr']=df3['langu'].apply(lambda b: json_langu(b,'fr'))

    subTitle('editor_df')
    
    if 'df_edit' not in st.session_state:
        st.session_state.df_edit=df3

    editor_df = st.data_editor(
        df3['textid','en','fr'], 
        key="updated_trad", 
        num_rows="dynamic",
        on_change=df_change
    )
    
    row_menu = st.columns(2,border=False, width="stretch")
    with row_menu[0]:
        if st.button("Cancel changes"):
            cancel_change()
    with row_menu[1]:
        if st.button("Save changes"):
            cancel_change()            

    edited_rows=None
    if 'updated_trad' in st.session_state:
        edited_rows = st.session_state.updated_trad['edited_rows']

    # pour fonction "Save changes"
    if edited_rows is not None:
        subTitle('edited_rows')
        edited_rows
        affected_index = list(edited_rows.keys())[0]
        affected_val_en = edited_rows[affected_index]['en']
        affected_val_fr = edited_rows[affected_index]['fr']
        #st.toast(f'index:{affected_index},en:{affected_val_en},fr:{affected_val_fr}', icon='ℹ️️', duration='short')
        #filtered_df = df.T.copy().iloc[affected_index]
        filtered_df = df.T.copy().iloc[11]
        st.write(f'index:{affected_index},en:{affected_val_en},fr:{affected_val_fr}')
        subTitle('res3')
        updated_json=json_data
        for i in edited_rows.keys():
            st.write(f'i={i}')
            res3 = df3.index[i]
            res3
            affected_val_en = edited_rows[i]['en']
            affected_val_fr = edited_rows[i]['fr']
            updated_json['data'][res3][0]['en']=affected_val_en
            updated_json['data'][res3][0]['fr']=affected_val_fr

        subTitle('updated_json')
        #updated_json=json_data
        #updated_json['data'][res3][0]['en']='Coucou'
        updated_json

def json_langu(val_langu,langu):
    #val_langu=json.load(val, strict=False)
    ret_val = val_langu[langu]
    return ret_val

def df_change():
    if 'updated_trad' in st.session_state:
        edited_rows = st.session_state.updated_trad['edited_rows']    
        st.toast('editor_df on_change', icon='ℹ️️', duration='short')

def cancel_change():
    if 'updated_trad' in st.session_state:
        try:
            del st.session_state['updated_trad']
        except:
            return None

def page_github():
    st.subheader(get_text_trad(site_langu,'menu_git_translate'), divider=True)
    tab1, tab2 = st.tabs(["Table", "RAW"])
    with tab1:
        subTitle('Table editor')
        json_to_frame()
    with tab2:
        subTitle('JSON file content')
        form_file_param(file_txt=json_file)    
    #form_file_param(file_txt=json_file)
    #json_to_frame()

page_github()
