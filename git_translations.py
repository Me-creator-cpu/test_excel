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
#import uuid
import string
import random


json_file='./textes.json'
site_langu='en'
if 'site_langu' in st.session_state:
    site_langu=st.session_state.site_langu

if 'dek' not in st.session_state:
    #st.session_state.dek = str(uuid.uuid4())
    st.session_state.dek = id_generator()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_id_dek():
    if 'dek' not in st.session_state:
        st.session_state.dek = id_generator()
    return st.session_state.dek

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

def text_crlf(raw_data_txt):
    data_txt=''
    if raw_data_txt is not None:
        textsplit = raw_data_txt.splitlines()
        for x in textsplit:
            data_txt += f'{x}\n'
    return data_txt

def form_file_param(file_txt='data/todo.txt'):
    raw_data_txt=open(file_txt, mode='r').read()
    data_txt=''
    #if raw_data_txt is not None:
    #    textsplit = raw_data_txt.splitlines()
    #    for x in textsplit:
    #        data_txt += f'{x}\n'
    data_txt=text_crlf(raw_data_txt)
    
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

def update_value():
    """
    Located on top of the data editor.
    """
    #st.session_state.dek = str(uuid.uuid4())
    st.session_state.dek = id_generator()

def subTitle(txt):
    st.subheader(f'{txt}', divider=True)           

def json_to_frame():
    if 'edited_rows' not in st.session_state:
        json_data=None
        df=None
        df3=None
        editor_df=None
    with open(json_file, encoding='utf-8', errors='ignore') as f:
        json_data = json.load(f, strict=False) 
    df = pd.DataFrame(json_data['data'])    

    df3=pd.DataFrame(json_data['data']).T.copy()
    df3.index.name = "textid"
    df3.rename(columns={df3.columns[0]: "langu"}, inplace=True)
    
    df3['en']=df3['langu'].apply(lambda b: json_langu(b,'en'))
    df3['fr']=df3['langu'].apply(lambda b: json_langu(b,'fr'))

    subTitle('Table editor')
    
    if 'df_edit' not in st.session_state:
        st.session_state.df_edit=df3

    editor_df = st.data_editor(
        df3, 
        #key=st.session_state.dek,
        key=get_id_dek(),
        #key="updated_trad",
        column_config={"langu": None},
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
    #if 'updated_trad' in st.session_state:
    #   edited_rows = st.session_state.updated_trad['edited_rows']
    if 'dek' in st.session_state:
        edited_rows = st.session_state.dek['edited_rows']

    # pour fonction "Save changes"
    if edited_rows is not None:
        updated_json=json_data
        for i in edited_rows.keys():
            res3 = df3.index[i]
            for j in ['en','fr']:
                try:
                    updated_json['data'][res3][0][j]=edited_rows[i][j]
                except:
                    txt_upd=False            

        with st.expander('Update to save', 
                         expanded=False, 
                         icon=':material/table_view:'):
            json_data
            st.text_area(
                label='JSON new',
                value=updated_json,
                label_visibility='visible',
                height=int(400)
                )

def json_langu(val_langu,langu):
    #val_langu=json.load(val, strict=False)
    ret_val = val_langu[langu]
    return ret_val

#def df_change():
#    if 'updated_trad' in st.session_state:
#        edited_rows = st.session_state.updated_trad['edited_rows']    
#        st.toast('editor_df on_change', icon='ℹ️️', duration='short')

def df_change():
    if 'dek' in st.session_state:
        edited_rows = st.session_state.dek['edited_rows']    
        st.toast('editor_df on_change', icon='ℹ️️', duration='short')

def cancel_change():
    if 'updated_trad' in st.session_state:
        try:
            del st.session_state['updated_trad']
        except:
            dummy=None
    if 'df_edit' in st.session_state:
        try:
            del st.session_state['df_edit']
        except:
            dummy=None
    if 'edited_rows' in st.session_state:
        try:
            del st.session_state['edited_rows']
        except:
            dummy=None
    if 'dek' in st.session_state:
        try:
            del st.session_state['dek']
        except:
            dummy=None       
    st.rerun()

def page_github():
    st.subheader(get_text_trad(site_langu,'menu_git_translate'), divider=True)
    tab1, tab2 = st.tabs(["Table", "RAW"])
    with tab1:
        json_to_frame()
    with tab2:
        subTitle('JSON file content')
        form_file_param(file_txt=json_file)    

page_github()
