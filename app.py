# Import Libraries
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configure API
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

# Load model
model = genai.GenerativeModel("gemini-1.5-flash")

# Functions
def get_gemini_response(input_text, image, prompt):
    response = model.generate_content([input_text, image, prompt])
    return response.text 

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = {
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# App UI
st.set_page_config(page_title='Multi-Language Invoice Extractor', layout='wide')

# Page Title with color
st.markdown(
    "<h1 style='text-align: center; color: #498d91;'>Multi-Language Invoice Extractor</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: grey;'>Upload your invoice and extract key information easily.</p>",
    unsafe_allow_html=True
)

# Upload file
uploaded_file = st.file_uploader(
    "Upload your invoice (JPG, JPEG, PNG)", 
    type=["jpg", "jpeg", "png"]
)

# Inform about auto-analysis
st.markdown(
    "<p style='text-align: center; color: #b22222;'>If you leave the question field blank, the invoice will be automatically analyzed.</p>",
    unsafe_allow_html=True
)

# Multiline Text Input for user question
user_prompt = st.text_area(
    "Ask your question about the invoice",
    placeholder="Type your question here...",
    height=150,
    max_chars=500,
    help="Ask anything related to the invoice like date, total amount, etc.",
    key="user_prompt"
)

# Button for submission
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    submit = st.button("Analyze Invoice", key="submit", help="Click to analyze the uploaded invoice.")

# Default prompt if user gives no question
default_input_prompt = '''
Analyze the invoice and extract key information like invoice number, date, customer details, total amount, taxes, and payment terms.
'''

# Handle submit
if submit:
    if uploaded_file is not None:
        try:
            with st.spinner('Analyzing the invoice, please wait...'):
                image_data = input_image_setup(uploaded_file)

                # Check if user typed something
                if user_prompt.strip() != "":
                    final_prompt = user_prompt
                else:
                    final_prompt = default_input_prompt

                # Display the uploaded image
                st.image(uploaded_file, caption="Uploaded Invoice", use_container_width=True)

                # Get response from the model
                response = get_gemini_response(final_prompt, image_data, final_prompt)

            st.success("Invoice analyzed successfully!")
            st.subheader("Extracted Information:", anchor="extracted-info")

            # Display extracted information
            st.markdown("<h3 style='color: #1e90ff;'>Key Information:</h3>", unsafe_allow_html=True)
            st.write(response)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload an invoice image before analyzing.")