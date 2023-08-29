import streamlit as st
import psycopg2

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = ''
try:
    rows = run_query("SELECT * from mytable;")
    #rows = run_query("SELECT * FROM subscribers;")
    # Print results.
    if not rows:
        st.info("0 rows fetched")
    else:
        for row in rows:
            st.write(f"{row[0]} has a :{row[1]}:")
except Exception as e:
    st.error(e)
