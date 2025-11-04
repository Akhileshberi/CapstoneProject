import streamlit as st
import pandas as pd
import PyPDF2
from gtts import gTTS
import io
import time


st.title("Web Application to convert text to speech and download the audio file")
status = st.radio("Select an option:", ("Enter Text", "Upload a file"))
text_content = ""
if status == "Enter Text":
    text_content_user = st.text_area("Enter your text here:", height=200)
    
else:
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "csv", "xlsx", "pdf"])
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            text_content = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            text_content = df.to_string() # Convert DataFrame to string
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(uploaded_file)
            text_content = df.to_string()
            st.text_area("Extracted Text", text_content, height=200)
                    

        # ... inside the file upload logic ...
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text_content = ""
            for page_num in range(len(pdf_reader.pages)):
                text_content += pdf_reader.pages[page_num].extract_text()
            st.text_area("Extracted Text", text_content, height=200)

        

def text_to_audio(text):
    tts = gTTS(text=text, lang='en')
    audio_bytes_io = io.BytesIO()
    tts.write_to_fp(audio_bytes_io)
    audio_bytes_io.seek(0)
    return audio_bytes_io
# ... later, after extracting/getting text_content or user_input_text ...
if st.button("Convert to Audio"):
     if text_content or text_content_user:
        text_to_convert = text_content if text_content else text_content_user
        audio_io = text_to_audio(text_to_convert)
        st.audio(audio_io.read(), format='audio/mp3')
        time.sleep(2) # Introduce a 2-second delay
     else:
        st.warning("Please upload a file or enter some text.")
        