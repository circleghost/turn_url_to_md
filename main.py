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
st.title('網址批量內容抓取器')

# File uploader
uploaded_file = st.file_uploader("請上傳一個包含網址的 txt 檔案（每行一個）", type="txt")

# CSS Selector input
css_selector = st.text_input("請輸入 CSS 選擇器")

# Submit button
if st.button("Submit"):
    if uploaded_file and css_selector:
        with st.spinner("知識庫產生中... 請稍候"):
            valid_content = ""
            invalid_content = ""
            urls = uploaded_file.getvalue().decode("utf-8").splitlines()
            progress_bar = st.progress(0)
            for i, url in enumerate(urls):
                title, markdown_content, is_valid = extract_and_convert(url, css_selector)
                if is_valid:
                    valid_content += f"標題：{title}\n{markdown_content}\n====================\n"
                else:
                    invalid_content += f"無效頁面：{url}\n"
                progress_bar.progress((i + 1) / len(urls))

            # Display valid data download button
            st.download_button(
                label="下載你的知識庫吧！",
                data=valid_content.encode('utf-8'),
                file_name="valid_data.txt",
                mime="text/plain"
            )

            # Display invalid data
            st.subheader("以下可能是網址錯誤，或是網頁內容未有 CSS 選擇器")
            st.text(invalid_content)
