import streamlit as st
import pandas as pd
import random
import time
import base64

# Function to set colorful background with green and orange pastel theme
def set_bg_color():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: linear-gradient(135deg, #A8E6CF, #FFDAC1);
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg_color()

# Function to play sound
def play_sound():
    sound_file = "https://www.soundjay.com/button/sounds/button-3.mp3"  # Example sound file
    sound_html = f"""
    <audio autoplay>
    <source src="{sound_file}" type="audio/mp3">
    </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

# Streamlit App Title and Layout
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.image("https://logos-world.net/wp-content/uploads/2023/03/AIS-Logo.png", width=150)
    
with col2:
    st.title('🎁 Welcome to OCM Party!')

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
    
    # Initialize or load picked names list and history
    if 'picked_names' not in st.session_state:
        st.session_state.picked_names = []
    if 'history' not in st.session_state:
        st.session_state.history = []

    col1, col2 = st.columns([2, 1])

    with col1:
        # Pick a random name button with slot machine effect
        if st.button('🎲 Pick a Random Name', use_container_width=True):
            with st.spinner('Spinning...'):
                name_slot = st.empty()
                department_slot = st.empty()
                
                # Slot machine effect: cycle through names quickly before stopping
                for _ in range(30):  # Number of spins
                    name = df.sample(n=1).iloc[0]['Name']
                    department = df.sample(n=1).iloc[0].get('Department Name', 'N/A')
                    name_slot.markdown(f"<h2 style='color:white; background-color:gray; padding: 10px; text-align: center;'>🎰 {name} 🎰</h2>", unsafe_allow_html=True)
                    department_slot.markdown(f"<h4 style='color:gray; text-align: center;'>Department: {department}</h4>", unsafe_allow_html=True)
                    time.sleep(0.1)  # Adjust speed for the slot machine effect
            
            # Finally pick the random name
            name, department = pick_random_name(df, st.session_state.picked_names)
            if name:
                st.session_state.history.append(name)  # Save to history
                play_sound()  # Play sound
                name_slot.markdown(f"<h1 style='color:white; background-color:green; padding: 20px; text-align: center;'>🎉 {name} 🎉</h1>", unsafe_allow_html=True)
                department_slot.markdown(f"<h4 style='color:gray; text-align: center;'>Department: {department}</h4>", unsafe_allow_html=True)
            else:
                st.warning('All names have been picked.')

        # Arrange Back and Reset List buttons in the same row
        col_back, col_reset = st.columns([1, 1])
        with col_back:
            if st.button('⬅️ Back', use_container_width=True):
                if st.session_state.history:
                    last_name = st.session_state.history.pop()  # Remove last picked name from history
                    st.session_state.picked_names.remove(last_name)  # Remove last picked name from the list

        with col_reset:
            if st.button('🔄 Reset List', use_container_width=True):
                st.session_state.picked_names = reset_list()
                st.session_state.history = []
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
