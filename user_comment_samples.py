import streamlit as st
from io import StringIO
import time
import random
from activate_bot import run_bot

def show_results():
    time_to_switch = False
    if "config" in st.session_state:
        st.subheader("Your Chatbot Configuration:")
        
        # Create three columns
        col1, col2, col3 = st.columns(3)
        
        # Define color for each category
        colors = {
            "Tone": "#FF9999",
            "Detail Level": "#99FF99",
            "Handling Controversial Topics": "#9999FF",
            "Humor Type": "#FFFF99",
            "Language Formality": "#FF99FF",
            "Handling Negative Comments": "#99FFFF",
            "Content Focus": "#FFCC99",
            "Handling Misunderstandings": "#CCFF99",
            "Interactivity Level": "#99CCFF"
        }
        
        # Distribute configuration items across columns
        columns = [col1, col2, col3]
        for i, (key, value) in enumerate(st.session_state.config.items()):
            with columns[i % 3]:
                st.markdown(f"""
                <div style="
                background: linear-gradient(45deg, {colors[key]}, {colors[key]}dd);
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 15px;
                color: black;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                ">
                <strong style="
                font-weight: 600;
                font-size: 1.0em;
                text-transform: uppercase;
                letter-spacing: 1px;
                display: block;
                margin-bottom: 5px;
                ">{key}</strong>
                <span style="
                font-size: 1.2em;
                display: block;
                font-weight: 300;
                ">{value}</span>
                </div>
                """, unsafe_allow_html=True)
        
    # Add a section for chat samples
    st.subheader("Provide chatbot some of your chat samples to mimic your writing style")
    st.write("Please provide some of your chat samples below. You can either enter them directly or upload a text file.")

    # Option to enter chat samples directly
    chat_samples_direct = st.text_area("Enter your chat samples here (one per line):", height=200)

    # Option to upload a file
    uploaded_file = st.file_uploader("Or upload a text file containing chat samples", type=["txt"])

    if st.button("Submit Samples"):
        if chat_samples_direct or uploaded_file:
            # Create a progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(100):
                # Update progress bar
                progress_bar.progress(i + 1)
                status_text.text(f"Processing: {i+1}%")
                
                # Add a realistic delay
                time.sleep(random.choice([0, 0, 0, 0, 0, 0, 0 , 0 , 0 , 1, 0, 0, 0, 0, 0, 0, 0]) + 0.02)  # Adjust this value to make the process faster or slower

            status_text.text("Processing complete!")
            time.sleep(1)  # Pause for a moment at 100%
            
            # Clear the progress bar and status text
            progress_bar.empty()
            status_text.empty()

            # Set the flag in session state to indicate bot activation
            st.session_state.bot_activated = True

            st.success("Chat samples submitted and processed successfully!")

            run_bot()
        else:
            st.warning("Please either enter some chat samples or upload a file before submitting.")
        