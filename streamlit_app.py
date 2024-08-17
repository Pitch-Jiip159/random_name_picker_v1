import streamlit as st
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
    st.image("https://your-logo-url-here.png", width=150)  # Replace with your logo URL
    
with col2:
    st.title('🎁 Random Name Picker for Buddy Game')

with col3:
    st.write("")

# Initialize session state for names, departments, and picked names
if 'names_list' not in st.session_state:
    st.session_state.names_list = []

if 'picked_names' not in st.session_state:
    st.session_state.picked_names = []

# User input form
with st.form(key='name_form'):
    name = st.text_input("Enter your name")
    department = st.text_input("Enter your department")
    submit_button = st.form_submit_button(label='Submit')

# Add new name and department to the list
if submit_button and name and department:
    st.session_state.names_list.append({"Name": name, "Department": department})
    st.success(f"{name} from {department} added successfully!")

# Display the list of names on the left
st.sidebar.title("Participants")
for person in st.session_state.names_list:
    st.sidebar.write(f"{person['Name']} ({person['Department']})")

# Function to pick a random name
def pick_random_name():
    available_names = [person for person in st.session_state.names_list if person['Name'] not in st.session_state.picked_names]
    if available_names:
        selected_person = random.choice(available_names)
        st.session_state.picked_names.append(selected_person['Name'])
        return selected_person['Name'], selected_person['Department']
    else:
        return None, None

# Pick a random name button
if st.button('🎲 Pick a Random Name'):
    with st.spinner('Picking a name...'):
        time.sleep(2)  # Simulate a delay
    name, department = pick_random_name()
    if name:
        st.markdown(f"<h2 style='color:green;'>🎉 Picked Name: {name}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='color:gray;'>Department: {department}</h4>", unsafe_allow_html=True)
    else:
        st.warning('All names have been picked.')

# Reset all (Reset game)
if st.button('🔄 Reset Game (Clear All)'):
    st.session_state.names_list = []
    st.session_state.picked_names = []
    st.info('The game has been reset. All participants and picked names have been cleared.')

# Reset picked names only
if st.button('🔄 Reset Picked Names'):
    st.session_state.picked_names = []
    st.info('The list of picked names has been reset. Participants remain in the game.')
