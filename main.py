import streamlit as st
import requests
from bs4 import BeautifulSoup
import html2text
from io import StringIO

# Function to extract and convert content
def extract_and_convert(url, selector):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        selected_content = soup.select_one(selector)
        title = soup.find('title').get_text() if soup.find('title') else 'No Title'

        if selected_content:
            converter = html2text.HTML2Text()
            converter.ignore_links = False
            markdown = converter.handle(str(selected_content))
            return title, markdown
        else:
            return title, 'No content found for the provided CSS selector.'
    except Exception as e:
        return 'No Title', str(e)

# Streamlit interface
st.title('URL Content Extractor')

# File uploader
uploaded_file = st.file_uploader("Upload a file containing URLs (one per line)", type="txt")

# CSS Selector input
css_selector = st.text_input("Enter the CSS selector")

# Process button
if st.button("Extract Content"):
    if uploaded_file and css_selector:
        content = ""
        for url in uploaded_file.getvalue().decode("utf-8").splitlines():
            title, markdown_content = extract_and_convert(url, css_selector)
            content += f"原文網址：{url}\n標題：{title}\n{markdown_content}\n====================\n"
        
        # Download link
        st.download_button(
            label="Download Content as TXT",
            data=StringIO(content),
            file_name="extracted_content.txt",
            mime="text/plain"
        )
