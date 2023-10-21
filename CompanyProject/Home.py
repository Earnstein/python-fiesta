import streamlit as st
import pandas as pd


st.set_page_config(layout="wide")
with open("Home.css") as style:
    st.markdown(f"<style>{style.read()}</style>", unsafe_allow_html=True)
st.header("The Best Company")
st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed diam nonummy nibh euismod tincidunt ut "
         "laoreet dolore Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat "
         "volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper"
         " suscipit lobortis nisl ut aliquip ex ea commodo consequatmagna aliquam erat volutpat. Ut wisi enim ad minim veniam"
         ", quis nostrud exerci  dolore magna aliquam tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat")

st.subheader("Our Team")
col1, col2, col3 = st.columns(3)

df_company_data = pd.read_csv("company_data.csv")
with col1:
    for index, row in df_company_data[:4].iterrows():
        st.header(f"{row['first name']} {row['last name']}")
        st.write(f"{row['role']}")
        st.image(f"company-images/{row['image']}")
        st.write("\n")
        st.write("\n")

with col2:
    for index, row in df_company_data[4:8].iterrows():
        st.header(f"{row['first name']} {row['last name']}")
        st.write(f"{row['role']}")
        st.image(f"company-images/{row['image']}")
        st.write("\n")
        st.write("\n")

with col3:
    for index, row in df_company_data[8:12].iterrows():
        st.header(f"{row['first name']} {row['last name']}")
        st.write(f"{row['role']}")
        st.image(f"company-images/{row['image']}")
        st.write("\n")
        st.write("\n")
