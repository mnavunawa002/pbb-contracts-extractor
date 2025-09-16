import streamlit as st
from clients.google_client import GoogleGeminiClient
import pandas as pd
import json

google_client = GoogleGeminiClient()

st.title("Hot Deal Package Extractor")

st.write("Upload a hotel rates contract as a PDF file and automatically extract relevant data using AI.")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    uploaded_file = google_client.upload_pdf(uploaded_file.read())
    st.write("File uploaded successfully")
    st.write(uploaded_file)
    with st.spinner("Extracting hot deal packages..."):
      # Extract hot deals as JSON string
      hot_deals_data = google_client.extract_hot_deal_packages(uploaded_file)

      if hot_deals_data:
          st.subheader("Extracted Hot Deals (Editable)")
          # convert the hot_deals_data to a pandas dataframe
          # hot_deals_data is already a JSON object (dict), so just extract the hot_deals list and convert to DataFrame
          hot_deals_list = hot_deals_data.get("hot_deals", [])
          hot_deals_data = pd.DataFrame(hot_deals_list)
          edited_hot_deals = st.data_editor(
              hot_deals_data,
              num_rows="dynamic",
              use_container_width=True,
              width="stretch",  # Ensure the editor takes the full width of the container
              key="hot_deals_editor"
          )

          # Download button for JSON
          st.download_button(
              label="Download as JSON",
              data=edited_hot_deals.to_json(orient="records", indent=2),
              file_name="hot_deals.json",
              mime="application/json",
              type="primary",  # This makes the button red in Streamlit
          )