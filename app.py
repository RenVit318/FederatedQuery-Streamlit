import streamlit as st
from FDP_handling import getFDPs, navigateFDP
from Query_handling import executeQuery


STANDARD_QUERY = """ 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?s ?label
WHERE {
  ?s rdfs:label ?label .
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
              st.rerun()  # Refresh view to prevent key errors

  


  st.subheader("Query")
  query = st.text_area(label="Type your SPARQL query here", value=STANDARD_QUERY, height=250)
  query_on_fdp = st.checkbox('Execute query on FDP instead of Triplestore')

  if 'query_excecute' not in st.session_state:
    st.session_state.query_execute = False # Need this for nested buttons. Main button forgets its state after first run.
  st.write(st.session_state.query_execute)
  if st.button("Execute Query") or st.session_state.query_execute:
    st.write('check 1')
    st.session_state.query_execute = True
    st.write(st.session_state.query_execute)
    if query_on_fdp:
      for FDP in st.session_state.fdp_urls:
        st.write(f'executing query for {FDP}')
        st.error('This code is not implemented yet')
        #TODO: Implement this code

    else:
      for FDP in st.session_state.fdp_urls:
        navigateFDP(FDP)
      
      st.write("Found the following datasets connected to the provided FAIR Data Points:")
      for dataset in st.session_state.datasets:
        st.write(f'- {dataset}')
     
      st.write('Yes!!')
      executeQuery(query)
      st.session_state.query_execute = False
      




def main():
  setupContent()



if __name__ == '__main__':
  main()
