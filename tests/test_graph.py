import streamlit as st
import graphviz

def build_graph_links(df,parent,child):
    graph = graphviz.Digraph()
    graph.edge("run", "intr")
    df
    for p,c in df[[parent,child]]:
        st.write(p,c)

    return st.graphviz_chart(graph),df

st.header("Graphviz")     