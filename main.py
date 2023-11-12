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
        title_text = soup.find('title').get_text() if soup.find('title') else 'No Title'
        title = f"[{title_text}]({url})"  # Markdown format for title with URL

        if selected_content:
            converter = html2text.HTML2Text()
            converter.ignore_links = False
            markdown = converter.handle(str(selected_content))
            return title, markdown, True
        else:
            return title, 'No content found for the provided CSS selector.', False
    except Exception as e:
        return 'No Title', str(e), False

# Streamlit interface
st.title('URL Content Extractor')

# File uploader
uploaded_file = st.file_uploader("Upload a file containing URLs (one per line)", type="txt")

# CSS Selector input
css_selector = st.text_input("Enter the CSS selector")

# Submit button
if st.button("Submit"):
    if uploaded_file and css_selector:
        valid_content = ""
        invalid_content = ""
        urls = uploaded_file.getvalue().decode("utf-8").splitlines()
        progress_bar = st.progress(0)
        for i, url in enumerate(urls):
            title, markdown_content, is_valid = extract_and_convert(url, css_selector)
            if is_valid:
                valid_content += f"標題：{title}\n{markdown_content}\n====================\n"
            else:
                invalid_content += f"{url}\n"
            progress_bar.progress((i + 1) / len(urls))

        # Display download buttons
        st.download_button(
            label="Download Valid Data as TXT",
            data=valid_content.encode('utf-8'),
            file_name="valid_data.txt",
            mime="text/plain"
        )

        st.download_button(
            label="Download Invalid Pages as TXT",
            data=invalid_content.encode('utf-8'),
            file_name="invalid_pages.txt",
            mime="text/plain"
        )
