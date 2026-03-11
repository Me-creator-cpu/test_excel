import streamlit as st
import pandas as pd

def greet():
    return "Hello!"

action = "greet"
st.write(eval(action + "()"))
