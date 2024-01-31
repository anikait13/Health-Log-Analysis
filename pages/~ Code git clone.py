import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.title("Code Plagarism 😔")

col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
with col6:
    if st.button("Dashboard"):
        switch_page("dashboard")

st.warning("The repository was plagiarized by others as it was set to public for deployment.")
st.write("Repository is set to private now. Source code will be sent as a .zip file")
st.image("images/Clones.png")