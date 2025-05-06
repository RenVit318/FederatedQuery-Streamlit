import streamlit as st
from FDP_handling import getFDPs
from Query_handling import executeQuery


STANDARD_QUERY = """ SELECT *
WHERE {
  ?s ?p ?o
} LIMIT 10"""


def setupContent():
  st.title("FAIR Hackathon Query App")
  st.write("Welcome to the web app to send a SPARQL query to one or more FAIR Data Points and to a triple store connected to it (if any).")
  st.write("Below you can insert the URLs of the FAIR Data Points you want to include in your query and define your query.")

  st.divider()

  st.header("SPARQL Query")
  
  st.subheader("FAIR Data Points")
  fdp_uris = getFDPs()
  for fdp_uri in fdp_uris:
    st.write(fdp_uri)


  st.subheader("Query")
  query = st.text_area(label="Type your SPARQL query here", placeholder=STANDARD_QUERY)
  if st.button("Execute Query"):
    executeQuery()
  




def main():
  setupContent()



if __name__ == '__main__':
  main()
