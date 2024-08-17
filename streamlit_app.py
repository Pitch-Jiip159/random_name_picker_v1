import streamlit as st
import pandas as pd
import random
import time

# Function to set background color
def set_bg_color():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-color: #f0f0f5;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg_color()

# Streamlit App Title and Layout
col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://your-logo-url-here.png", width=150)
    
with col2:
    st.title('🎁 Random Name Picker for Buddy Game')

with col3:
    st.write("")

# Load CSV file into DataFrame
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

# Function to pick a random name
def pick_random_name(df, picked_names):
    available_names = df[~df['Name'].isin(picked_names)]
    if not available_names.empty:
        selected_name = available_names.sample(n=1).iloc[0]
        picked_names.append(selected_name['Name'])
        return selected_name['Name'], selected_name.get('Department Name', 'N/A')
    else:
        return None, None

# Function to reset the picked names list
def reset_list():
    return []

# File uploader
uploaded_file = st.file_uploader("📄 Upload a CSV file", type="csv")

if uploaded_file is not None:
    df = load_data(uploaded_file)
    
    # Initialize or load picked names list
    if 'picked_names' not in st.session_state:
        st.session_state.picked_names = []

    col1, col2 = st.columns([2, 1])

    with col1:
        # Pick a random name button
        if st.button('🎲 Pick a Random Name'):
            with st.spinner('Picking a name...'):
                time.sleep(2)  # Simulate a delay
            name, department = pick_random_name(df, st.session_state.picked_names)
            if name:
                st.markdown(f"<h1 style='color:white; background-color:green; padding: 20px; text-align: center;'>🎉 {name} 🎉</h1>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='color:gray; text-align: center;'>Department: {department}</h4>", unsafe_allow_html=True)
            else:
                st.warning('All names have been picked.')

        # Reset button
        if st.button('🔄 Reset List'):
            st.session_state.picked_names = reset_list()
            st.info('The list has been reset.')

    with col2:
        st.write("🎯 All Names:")
        # Show the list of names, highlighting picked ones
        for _, row in df.iterrows():
            name = row['Name']
            department = row.get('Department Name', 'N/A')
            if name in st.session_state.picked_names:
                st.markdown(f"✅ **{name}** - {department}", unsafe_allow_html=True)
            else:
                st.write(f"{name} - {department}")

else:
    st.info("Please upload a CSV file.")
