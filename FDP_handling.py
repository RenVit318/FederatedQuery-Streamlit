import requests
import rdflib
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import DCAT
import sys

#QUERIES
QUERY_CONTAINS = prepareQuery(
    "SELECT ?cat WHERE {?x ldp:contains ?cat}",
    initNs = {"ldp": rdflib.URIRef("http://www.w3.org/ns/ldp#")}
)

QUERY_ACCESSLINK = prepareQuery(
    "SELECT ?acl WHERE {?x dcat:accessURL ?acl}",
    initNs = {"dcat": DCAT}
)



def parseRDFIntoGraph(url):
    g = rdflib.Graph()
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        g.parse(data=response.text, format='turtle') # This is an assumption. Fix this?

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error while fetching URL {url}: {e}")
    except Exception as e:
        print(f"Unexpected error while handling URL {url}: {type(e).__name__} - {e}")
        sys.exit(1)

    return g


def navigateFDP(url):
    """From the URL of FDP"""
    if 'datasets' not in st.session_state:
        st.session_state.datasets = []
    
    g = parse_rdf_into_graph(url)
    catalogs = g.query(QUERY_CONTAINS)
    for row_c in catalogs:
        g_cat = parse_rdf_into_graph(row_c.cat)
        datasets = g_cat.query(QUERY_CONTAINS)
        for row_ds in datasets:
            g_ds = parse_rdf_into_graph(row_ds.cat)
            distributions = g_ds.query(QUERY_CONTAINS)
            for row_db in distributions:
                g_db = parse_rdf_into_graph(row_db.cat)
                access_links = g_db.query(QUERY_ACCESSLINK)

                for row_acl in access_links:
                    st.session_state.datasets.append(row_acl.acl)
    
    


def getFDPs():
    with open('fdp_uris.txt', 'r') as f:
        fdp_uris = f.readlines() 
    return fdp_uris
