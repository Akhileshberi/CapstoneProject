import streamlit as st
from gtts import gTTS
import os
import PyPDF2
import tempfile
from PyPDF2 import PdfReader
import pandas as pd
import csv

st.title("Web Application to convert text to speech and download the audio file")
status = st.radio("Select an option:", ("Enter Text", "Upload a file"))
if status == "Enter Text":
    text = st.text_area("Enter the text you want to convert to speech:")
    if st.button("Convert to Speech"):
        if text.strip() == "":
            st.error("Please enter some text to convert.")
        else:
            tts = gTTS(text=text, lang='en')
            audio_file = "output.mp3"
            tts.save(audio_file)
            st.success("Text has been converted to speech!")
            with open(audio_file, "rb") as file:
                st.download_button(label="Download Audio", data=file, file_name=audio_file, mime="audio/mpeg")
            os.remove(audio_file)
elif status == "Upload a file":
    
    uploaded_file = st.file_uploader("Upload a file to translate", type=["pdf", "txt", "csv","xlsx"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name   
            st.success(f"File '{uploaded_file.name}' saved temporarily at: {tmp_file_path}")
            try:
                if uploaded_file.name.endswith(".pdf"):
                    with open(tmp_file_path, "rb") as file:
                        reader = PdfReader(file)
                        for page in reader.pages:
                            text = ""
                            text += page.extract_text() or ""
                    st.success("PDF file read successfully!")
                elif uploaded_file.name.endswith(".txt"):
                    with open(tmp_file_path, "r", encoding="utf-8") as file:
                        text = ""
                        text = file.read()
                        st.success("Text file read successfully!")
                        st.text_area("Extracted Text:", text, height=100)
                elif uploaded_file.name.endswith(".csv"):
                    delimiter_char = ';'
                    text = pd.read_csv(tmp_file_path, sep=delimiter_char)
                    text = text.to_string() 
                # Additional file types can be handled here
            except Exception as e:
                st.error(f"An error occurred while processing the file: {e}")
        if st.button("Convert to Speech"):
            tts = gTTS(text=text, lang='en')
            audio_file = "output.mp3"
            tts.save(audio_file)
            st.success("Text has been converted to speech!")
            with open(audio_file, "rb") as file:
                st.download_button(label="Download Audio", data=file, file_name=audio_file, mime="audio/mpeg")
                os.remove(audio_file)