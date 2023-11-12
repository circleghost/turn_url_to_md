import streamlit as st
import requests
from bs4 import BeautifulSoup
import html2text

# Function to extract and convert content
def extract_and_convert(url, selector):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        selected_content = soup.select_one(selector)

        if selected_content:
            converter = html2text.HTML2Text()
            converter.ignore_links = False
            markdown = converter.handle(str(selected_content))
            return markdown
        else:
            return None
    except Exception as e:
        return str(e)

# Streamlit interface
st.title('URL Content Extractor')

# File uploader
uploaded_file = st.file_uploader("Upload a file containing URLs (one per line)", type="txt")

# CSS Selector input
css_selector = st.text_input("Enter the CSS selector")

if uploaded_file and css_selector:
    content = ""
    for url in uploaded_file.getvalue().decode("utf-8").splitlines():
        markdown_content = extract_and_convert(url, css_selector)
        if markdown_content:
            content += f"原文網址：{url}\n標題：{url}\n# md格式的內容\n{markdown_content}\n====================\n"

    st.text_area("Extracted Content", content, height=300)
