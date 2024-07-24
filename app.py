import streamlit as st
from user_comment_samples import show_results
import google.generativeai as genai
import time
import random
import os 
from PIL import Image
import io

genai.configure(api_key="key daalo")

def use_model(instruction_tuning, image_bytes):
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    final_instruction = f'''
    On behalf of me, write a comment on the tweet. Here is your configuration:
    {instruction_tuning}
    '''
    
    try:
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        response = model.generate_content([final_instruction, image])
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"


def read_instruction_tuning():
    try:
        with open("artifacts/instruction_tuning.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        st.error("instruction_tuning.txt file not found in the artifacts directory.")
        return None
    except Exception as e:
        st.error(f"Error reading instruction_tuning.txt: {str(e)}")
        return None
  

# Configuration
def configuration():
    st.title("Chatbot Configuration")

    if 'config' not in st.session_state:

        st.session_state.config = {}
    if 'chat_samples' not in st.session_state:
        st.session_state.chat_samples = []

    # Configuration questions
    st.session_state.config['Tone'] = st.radio("1. What tone should the chatbot use in comments?", 
        ["Positive and encouraging", "Neutral and factual", "Humorous and witty", "Supportive and empathetic", "Sarcastic and playful"])

    st.session_state.config['Detail Level'] = st.select_slider("2. How detailed should the chatbot's comments be?", 
        options=["Very brief (1-2 sentences)", "Moderate detail (2-3 sentences)", "Detailed (3-4 sentences)", "As much detail as possible", "Varies based on the tweet"], 
        value="Moderate detail (2-3 sentences)")

    st.session_state.config['Handling Controversial Topics'] = st.radio("3. How should the chatbot handle controversial topics?", 
        ["Avoid them", "Address them carefully", "Be neutral", "Provide a balanced view", "Follow user's stance"])

    st.session_state.config['Humor Type'] = st.selectbox("4. What kind of humor do you prefer in comments?", 
        ["Light and playful", "Sarcastic", "Puns", "No humor", "Mixed"])

    st.session_state.config['Language Formality'] = st.select_slider("5. How formal should the language be in comments?", 
        options=["Very formal", "Formal", "Semi-formal", "Informal", "Very informal"], 
        value="Semi-formal")

    st.session_state.config['Handling Negative Comments'] = st.radio("6. How should the chatbot respond to negative tweets or comments?", 
        ["Ignore them", "Respond positively", "Respond neutrally", "Address the negativity carefully", "Follow user's preference"])

    st.session_state.config['Content Focus'] = st.multiselect("7. What type of content should the chatbot focus on when commenting?", 
        ["News and current events", "Entertainment and pop culture", "Technology and innovation", "Personal updates and stories", "A mix of all"], 
        default=["A mix of all"])

    st.session_state.config['Handling Misunderstandings'] = st.selectbox("8. How should the chatbot handle misunderstandings in comments?", 
        ["Apologize and clarify", "Provide additional context", "Ask for clarification from the user", "Move on and comment on the next tweet", "Follow user's preference"])

    st.session_state.config['Interactivity Level'] = st.select_slider("9. How interactive should the chatbot be in comments?", 
        options=["Ask follow-up questions", "Make statements only", "Mix of questions and statements", "Share related links or resources", "Follow user's interaction style"], 
        value="Mix of questions and statements")

    # Display configuration
    col1, col2, col3 = st.columns(3)
    colors = {
        "Tone": "#FF9999", "Detail Level": "#99FF99", "Handling Controversial Topics": "#9999FF",
        "Humor Type": "#FFFF99", "Language Formality": "#FF99FF", "Handling Negative Comments": "#99FFFF",
        "Content Focus": "#FFCC99", "Handling Misunderstandings": "#CCFF99", "Interactivity Level": "#99CCFF"
    }

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

    # Chat samples section
    st.subheader("(Optional) Provide chatbot some of your chat samples to mimic your writing style")
    
    # Direct text input
    new_sample = st.text_area("Enter chat samples here (one per line):", height=150)
    
    # File upload
    uploaded_file = st.file_uploader("Or upload a text file containing chat samples", type=["txt"])

    if st.button("Submit"):
        # Create instruction tuning string
        instruction_tuning = "Your Chatbot Configuration:\n" + "\n".join([f"{k}: {v}" for k, v in st.session_state.config.items()])
        instruction_tuning += "\n\nChat Samples:\n"
        
        # Add samples from direct text input
        if new_sample:
            samples = new_sample.split('\n')
            for sample in samples:
                if sample.strip():  # Only add non-empty lines
                    st.session_state.chat_samples.append(sample.strip())
                    instruction_tuning += f"{sample.strip()}\n"
        
        # Add samples from existing chat_samples
        for sample in st.session_state.chat_samples:
            instruction_tuning += f"{sample}\n"
        
        # Add samples from uploaded file
        if uploaded_file:
            file_contents = uploaded_file.getvalue().decode("utf-8")
            instruction_tuning += f"\nUploaded samples:\n{file_contents}"

        # Save instruction_tuning as an artifact
        artifact_dir = "artifacts"
        os.makedirs(artifact_dir, exist_ok=True)
        artifact_path = os.path.join(artifact_dir, "instruction_tuning.txt")
        
        with open(artifact_path, "w") as f:
            f.write(instruction_tuning)

        # Display progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i in range(100):
            # Update progress bar
            progress_bar.progress(i + 1)
            status_text.text(f"Processing: {i+1}%")
            
            # Add a delay to make the entire process take about 10 seconds
            time.sleep(0.1)  # 100 iterations * 0.1 seconds = 10 seconds total

        status_text.text("Processing complete!")
        time.sleep(1)  # Pause for a moment at 100%
        
        # Clear the progress bar and status text
        progress_bar.empty()
        status_text.empty()

        return 



configuration()
# RUN THE MODEL
st.title("Chatbot Interface")
instruction_tuning = read_instruction_tuning()
uploaded_file = st.file_uploader("Input the Tweet", type=["txt", "pdf", "doc", "docx", "jpeg", "jpg", "png"])

if uploaded_file is not None:
    file_contents = uploaded_file.read()

    if st.button("Get Response"):
        with st.spinner("Generating response..."):
            if uploaded_file.type.startswith('image'):
                response = use_model(instruction_tuning, file_contents)
                st.image(file_contents, caption="Uploaded Image", use_column_width=True)
            else:
                # For text files, we'll pass the content as a string
                text_content = file_contents.decode('utf-8', errors='ignore')
                response = use_model(instruction_tuning, text_content)
                st.text("Uploaded file content:")
                st.code(text_content)
        
        st.subheader("Bot Response:")
        st.text_area("", value=response, height=200, key="bot_response")

else:
    st.info("Please upload a file to get a response.")
