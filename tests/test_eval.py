import streamlit as st
import pandas as pd
import numpy as np

def greet():
    return "Hello!"

action = "greet"
st.write(eval(action + "()"))

test_data=np.random.randn(10, 20) #('col %d' % i for i in range(20)))
test_data