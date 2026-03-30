import streamlit as st
import graphviz

def build_graph_links(df,parent,child):
    graph = graphviz.Digraph()
    graph.edge("run", "intr")

    return st.graphviz_chart(graph)

st.header("Graphviz")     