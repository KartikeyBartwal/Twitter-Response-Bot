import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import io

# Configure the Google AI API (make sure to set this environment variable)

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


def run_bot(instruction_tuning):
    st.title("Chatbot Interface")
    uploaded_file = st.file_uploader("Input the Tweet", type=["txt", "pdf", "doc", "docx", "jpeg", "jpg", "png"])

    if uploaded_file is not None:
        file_contents = uploaded_file.read()
        
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
    

def main():
    st.set_page_config(page_title="Chatbot App", page_icon="🤖")
    
    instruction_tuning = read_instruction_tuning()
    
    if instruction_tuning:
        run_bot(instruction_tuning)
    else:
        st.warning("Unable to load instruction tuning. Please check the file and try again.")

if __name__ == "__main__":
    main()
