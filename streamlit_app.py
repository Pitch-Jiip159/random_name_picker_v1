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

# Initialize session state for group token, host status, names, and picked names
if 'group_token' not in st.session_state:
    st.session_state.group_token = None

if 'is_host' not in st.session_state:
    st.session_state.is_host = False

if 'names_list' not in st.session_state:
    st.session_state.names_list = []

if 'picked_names' not in st.session_state:
    st.session_state.picked_names = []

# Group creation or joining
if st.session_state.group_token is None:
    st.title("🎉 Create or Join a Buddy Game")

    # Host creates the group
    if st.button("🛠️ Create a Group"):
        st.session_state.group_token = st.text_input("Enter a unique token for your group (e.g., a word or number):")
        st.session_state.is_host = True
        st.success(f"Group created successfully! Share this token with participants: {st.session_state.group_token}")

    # Participant joins the group
    group_token_input = st.text_input("Enter the group token to join:")
    if st.button("🔑 Join Group") and group_token_input == st.session_state.group_token:
        st.session_state.is_host = False
        st.success("You have successfully joined the group!")
    elif group_token_input and st.session_state.group_token is not None:
        st.error("Invalid group token. Please try again.")
else:
    st.title(f"🎁 Buddy Game (Group: {st.session_state.group_token})")

    # User input form (only for participants)
    if not st.session_state.is_host:
        with st.form(key='name_form'):
            name = st.text_input("Enter your name")
            department = st.text_input("Enter your department")
            submit_button = st.form_submit_button(label='Submit')

        # Add new name and department to the list (only if not a duplicate)
        if submit_button and name and department:
            if name not in [person['Name'] for person in st.session_state.names_list]:
                st.session_state.names_list.append({"Name": name, "Department": department})
                st.success(f"{name} from {department} added successfully!")
            else:
                st.warning(f"{name} is already in the list. Try another name.")
    
    # Display the list of names (only for the host)
    if st.session_state.is_host:
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

# Allow host to end the game and reset everything, including the group token
if st.session_state.is_host and st.button('🚪 End Game (Reset Everything)'):
    st.session_state.group_token = None
    st.session_state.is_host = False
    st.session_state.names_list = []
    st.session_state.picked_names = []
    st.info('The game has been ended, and everything has been reset.')
