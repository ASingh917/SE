from dotenv import load_dotenv # type: ignore
import streamlit as st # type: ignore
import os
from PIL import Image # type: ignore
import google.generativeai as genai # type: ignore

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini Pro model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])  # Start a chat session

# Function to get responses from Gemini Pro model
def get_gemini_response(input_text, image=None):
    if input_text and image:  # Both text and image provided
        response = chat.send_message([input_text, image], stream=True)
    elif input_text:  # Only text provided
        response = chat.send_message(input_text, stream=True)
    elif image:  # Only image provided
        response = chat.send_message(image, stream=True)
    else:
        return "Please provide a valid input."
    
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Q&A and Vision Demo")

st.header("Gemini AI Application")

# Input fields for user interaction
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display uploaded image
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button
submit = st.button("Generate Response")

# Process input and display response
if submit:
    response = get_gemini_response(input_text, image)
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)  # Display response chunk by chunk
