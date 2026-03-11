import streamlit as st
import pandas as pd
import numpy as np

def greet():
    return "Hello!"

action = "greet"
st.write(eval(action + "()"))

test_data=np.random.randn(10, 1) #('col %d' % i for i in range(20)))
test_data=('tab%d' % i for i in range(4))
test_data