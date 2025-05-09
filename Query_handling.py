import streamlit as st
import rdflib
import requests

def executeQuery(query):
    """Send the query over https, the alternative is using rdflib and injecting a SERVICE statement. 
    TODO: Consider pros and cons of these approaches"""
    st.write(st.session_state.datasets)

    headers = {
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "application/sparql-results+json"
    }

    data = {
      "query": query
    }

    for url in st.session_state.datasets:
      st.info('Sending the query to ' + url)
      response = requests.post(url, data=data, headers=headers)
      st.info('Succesfully sent and received query, response: ')
      st.info(response)

      
    st.write(response.text)



