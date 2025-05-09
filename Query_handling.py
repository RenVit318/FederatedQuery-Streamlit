import streamlit as st
import rdflib
import requests

def executeQuery(query):
    """Send the query over https, the alternative is using rdflib and injecting a SERVICE statement. 
    TODO: Consider pros and cons of these approaches"""
    for url in st.session_state.datasets:
      st.info('Sending the query to ' + url)
      response = requests.post(url, data={'query': query})
      st.info('Succesfully sent and received query, response: ' + response)

      
    st.write(response.text)



