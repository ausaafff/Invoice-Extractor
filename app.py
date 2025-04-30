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

# Inject Custom CSS
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap');

    /* Global background and text color */
    .stApp {
        background-color: #1A252F;
        color: white;
        font-family: 'Poppins', sans-serif;
    }

    /* Title and Subtitle */
    h1 {
        text-align: center;
        color: #498D91;
        font-size: 2.8em;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #A0A0A0;
        font-size: 1.2em;
        margin-bottom: 30px;
    }

    /* File uploader styling */
    div[data-testid="stFileUploader"] {
        margin-bottom: 30px;
    }
    div[data-testid="stFileUploader"] > label {
        color: white;
        font-size: 20px;
        font-weight: 500;
    }
    div[data-testid="stFileUploader"] > div > div {
        border: 2px dashed #498D91;
        background-color: #2E3A46;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        transition: border-color 0.3s ease;
    }
    div[data-testid="stFileUploader"] > div > div:hover {
        border-color: #60A5A9;
    }

    /* Instruction text */
    .instruction {
        text-align: center;
        color: #b22222;
        font-size: 1em;
        margin-bottom: 20px;
    }

    /* Text area styling */
    div[data-testid="stTextArea"] {
        margin-bottom: 30px;
    }
    div[data-testid="stTextArea"] > label {
        color: white;
        font-size: 20px;
        font-weight: 500;
    }
    div[data-testid="stTextArea"] textarea {
        background-color: #0F1A20;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stTextArea"] textarea::placeholder {
        color: #A0A0A0;
        font-style: italic;
    }

    /* Button styling */
    div[data-testid="stButton"] button {
        background-color: #498D91;
        color: white;
        border: none;
        padding: 15px 40px; /* Increased padding for larger button */
        border-radius: 8px;
        font-size: 1.2em; /* Larger font size */
        font-weight: 500;
        transition: background-color 0.3s ease, transform 0.2s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stButton"] button:hover {
        background-color: #60A5A9;
        transform: translateY(-2px);
    }

    /* Spinner, success, and error messages */
    .stSpinner > div > div {
        color: white;
        font-size: 1.1em;
    }
    .stSuccess {
        color: #28A745;
        font-size: 1.1em;
        text-align: center;
    }
    .stError {
        color: #b22222;
        font-size: 1.1em;
        text-align: center;
    }

    /* Results container */
    .results {
        background-color: #2E3A46;
        padding: 25px;
        border-radius: 10px;
        color: white;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        margin-top: 20px;
    }
    .results h3 {
        color: #1e90ff;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Subtitle
st.markdown("<h1>Multi-Language Invoice Extractor</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Upload your invoice and extract key information easily.</p>", unsafe_allow_html=True)

# Upload File Section
uploaded_file = st.file_uploader(
    "Upload your invoice (JPG, JPEG, PNG)", 
    type=["jpg", "jpeg", "png"]
)

# Instruction Text
st.markdown(
    "<p class='instruction'>If you leave the question field blank, the invoice will be automatically analyzed.</p>",
    unsafe_allow_html=True
)

# Multiline Text Input for User Question
user_prompt = st.text_area(
    "Ask your question about the invoice",
    placeholder="Type your question here...",
    height=150,
    max_chars=500,
    help="Ask anything related to the invoice like date, total amount, etc.",
    key="user_prompt"
)

# Button for Submission
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    submit = st.button("Analyze Invoice", key="submit", help="Click to analyze the uploaded invoice.")

# Default Prompt if User Gives No Question
default_input_prompt = '''
Analyze the uploaded invoice and provide a detailed summary including: the invoice number, invoice date, 
customer name and contact information, itemized list of products or services, total amount due, tax details 
(such as VAT or GST), payment terms, and any other relevant notes. Present the extracted information in clear, 
complete sentences.'''

# Handle Submit
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
                st.image(uploaded_file, caption="Uploaded Invoice", use_column_width=True)
                # Get response from the model
                response = get_gemini_response(final_prompt, image_data, final_prompt)

            st.success("Invoice analyzed successfully!")
            st.markdown('<div class="results">', unsafe_allow_html=True)
            st.subheader("Extracted Information:", anchor="extracted-info")
            st.markdown("<h3>Key Information:</h3>", unsafe_allow_html=True)
            st.write(response)
            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload an invoice image before analyzing.")
