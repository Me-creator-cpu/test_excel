import streamlit as st
import pandas as pd
import numpy as np

def greet():
    return "Hello!"

action = "greet"
st.write(eval(action + "()"))

test_data=np.random.randn(10, 1) #('col %d' % i for i in range(20)))
test_data=('tab%d' % i for i in range(5))
test_data


if 'site_langu' in st.session_state:
    site_langu=st.session_state.site_langu
    st.write(f'site_langu={site_langu}')
else:
    st.write(f'site_langu not in st.session_state')