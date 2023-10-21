import streamlit as st

with st.form("my_form"):
    st.write("Your Email Address")
    st.text_input("", placeholder="email...")
    options = st.selectbox(
        "What topic would you like to discuss?",
        ("Job Inquires", "Proposal", "Others")
    )
    st.write("Text")
    st.text_area("")
    st.form_submit_button("Submit")


st.session_state