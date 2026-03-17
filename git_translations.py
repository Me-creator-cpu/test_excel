import streamlit as st
import pandas as pd
from pandas import json_normalize
from datetime import datetime, timedelta
from pathlib import Path
from github import Auth
from github import Github
import base64
import json

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
    form_file_update = st.form('form_file_update',width='stretch',height='stretch')
    height = st.slider("Set the height of the text area", 100, 1000, 100)
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
    #json_data
    #ret_val = texts_trad['data'][textId][0][langu]
    subTitle('df')
    df = pd.DataFrame(json_data['data'])
    df
    for x in df:
        st.write(x)
    #edited_df = st.data_editor(df.T)
    subTitle('df2')
    df2=df.T
    df2
    #pivoted_df = df.T.pivot(index='Agent', columns='Region', values='Sales')
    subTitle('df3')
    df3=df2.copy()
    df3=st.dataframe(
        df3,
        column_config={
            "textid": st.column_config.TextColumn( "textid", pinned = True ),
            "langu": st.column_config.TextColumn( "langu", pinned = False ), 
        },
        width="stretch",
        hide_index=None,
    )
    df3

def page_github():
    st.subheader(get_text_trad(site_langu,'menu_git_translate'), divider=True)
    form_file_param(file_txt=json_file)

    json_to_frame()

page_github()
