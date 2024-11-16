import time
from dotenv import load_dotenv  # type: ignore
import streamlit as st  # type: ignore
import os
from PIL import Image  # type: ignore
import google.generativeai as genai  # type: ignore
from functools import lru_cache

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get responses from Gemini Pro Vision model
def get_gemini_response(input_text, image):
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Add instructions to the model to ensure it provides only law-related information
    legal_prompt = "Please provide legal advice or information based on the input provided. Do not provide any unrelated or non-legal advice. "
    
    # Handle both text and image, optimized separately
    if input_text and image:  # Both text and image provided
        response = model.generate_content([legal_prompt + input_text, image])
    elif input_text:  # Only text provided
        response = model.generate_content([legal_prompt + input_text])
    elif image:  # Only image provided
        response = model.generate_content(image)
    else:
        response = "Please provide a valid input."
    return response.text

# Cache responses to avoid redundant API calls
@lru_cache(maxsize=100)
def cached_response(input_text, image):
    return get_gemini_response(input_text, image)

# Initialize Streamlit app
st.set_page_config(page_title="Legal Advisory Chat App")

st.header("Legal Advisory AI Application")

# Input fields for user interaction
input_text = st.text_input("Legal Query: ", key="input")
uploaded_file = st.file_uploader("Choose an image with legal content...", type=["jpg", "jpeg", "png"])

# Display uploaded image
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # Resize the image to a smaller size for faster processing (200x200 for example)
    image = image.resize((200, 200))  # Resize to 200x200 pixels for faster processing
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button
submit = st.button("Get Legal Advice")

# Process input and display response
if submit:
    with st.spinner('Processing your request...'):
        # Start the clock for performance monitoring
        start_time = time.time()

        # Check if the input query is cached
        response = cached_response(input_text, image)
        
        # Stop the clock and calculate the time taken
        elapsed_time = time.time() - start_time

        st.subheader("The Legal Response is")
        st.write(response)

        # Show the time taken for processing
        st.write(f"Time taken: {elapsed_time:.2f} seconds")

    # Add a disclaimer to ensure that the response is not considered formal legal advice
    st.markdown("**Disclaimer:** The response provided is for informational purposes only and should not be construed as formal legal advice. Please consult a qualified attorney for specific legal concerns.")
