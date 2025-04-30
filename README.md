# Multi-Language Invoice Extractor

The **Multi-Language Invoice Extractor** is a smart web application that uses **Google Gemini 1.5 Flash** to automatically extract structured information from invoice images. With an intuitive, dark-themed interface built using **Streamlit**, users can upload invoice files in JPG, JPEG, or PNG format and get accurate, detailed summaries or ask custom questions related to the invoice content.

This tool supports **multiple languages**, including **English, Hindi, Marathi, Gujarati**, and more, making it ideal for processing invoices from diverse linguistic regions.

##  What It Does

- Extracts:
  - Invoice number and date
  - Customer name and contact details
  - Itemized products/services
  - Total amount, tax details (e.g., VAT/GST), payment terms
- Supports both default summarization and user-defined queries
- Works across multiple languages
- Displays results in clean, readable format

## Built With

- **Streamlit** – For building the UI
- **Google Generative AI (Gemini 1.5 Flash)** – For invoice analysis
- **Pillow (PIL)** – For image file handling
- **dotenv** – For secure API key management

## Use Cases

- Businesses looking to automate invoice processing
- Multilingual document handling
- Quick summarization of financial documents
- Custom query-based extraction from invoices

##  Highlights

- Dark-mode UI with modern styling
- Optional custom question input
- Secure API integration using environment variables
- Easy deployment and local use via Streamlit

## Note

Ensure invoices are clear and legible for best results. API usage depends on your Google Gemini plan and rate limits.
