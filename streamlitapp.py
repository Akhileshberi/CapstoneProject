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
    