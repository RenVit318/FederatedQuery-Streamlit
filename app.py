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

  # Load the FDPs from standard file
  if "fdp_urls" not in st.session_state:
    st.session_state.fdp_urls = getFDPs()


  # Section to add a new FDP
  st.write("Add a new FAIR Data Point")
  new_fdp = st.text_input("URL of FAIR Data Point:")
  if st.button("Add FDP") and new_fdp:
      if new_fdp not in st.session_state.fdp_urls:
          st.session_state.fdp_urls.append(new_fdp)
          st.success(f"Added {new_fdp}")
      else:
          st.warning("This URL is already in the list.")
  
  # Section to display and edit existing fdp_urls
  for i, fdp_url in enumerate(st.session_state.fdp_urls):
      col1, col2, col3 = st.columns([3, 1, 1])
      with col1:
          edited_fdp_url = st.text_input(f"FDP {i+1}", value=fdp_url, key=f"fdp_{i}")
      with col2:
          if st.button("Update", key=f"update_{i}"):
              if edited_fdp_url and edited_fdp_url != fdp_url:
                  st.session_state.fdp_urls[i] = edited_fdp_url
                  st.success(f"Updated fdp_url {i+1} to {edited_fdp_url}")
      with col3:
          if st.button("Delete", key=f"delete_{i}"):
              st.session_state.fdp_urls.pop(i)
              st.success(f"Deleted {fdp_url}")
              st.experimental_rerun()  # Refresh view to prevent key errors

  


  st.subheader("Query")
  query = st.text_area(label="Type your SPARQL query here", value=STANDARD_QUERY)
  if st.button("Execute Query"):
    executeQuery()
  




def main():
  setupContent()



if __name__ == '__main__':
  main()
