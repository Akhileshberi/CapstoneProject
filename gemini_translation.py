import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import PyPDF2
import tempfile
import pandas as pd
#import basicStreamlitapp

import getpass
#APIKEY = getpass.getpass()
APIKEY = st.secrets["OPENAI_API_KEY"]
genai.configure(api_key=APIKEY)

#Configure LLL Model

model=genai.GenerativeModel("gemini-flash-latest")
#print(genai.list_models())
#Funtion to translate text using Gemini
def translate_text_gemini(text, target_language):   
    try:
        prompt = f"Translate the following text to {target_language}:\n\n{text},provide only the translated text without any additional commentary."
        response = model.generate_content(prompt)
        translated_text = response.text.strip()
        return translated_text
    except Exception as e:
        st.error(f"An error occurred during translation: {e}")
        return None

#Function to convert text to speech
def text_to_speech(text,language_code):
    try:
        tts = gTTS(text=text, lang=language_code)
        #temp_file=tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        audio_file = "output.mp3"
        tts.save(audio_file)
        #tts.save(temp_file.name)
        return audio_file
    except Exception as e:
        st.error(f"An error occurred during text-to-speech conversion: {e}")
        return None
    
#Stremalit App
st.title("Multilingual Text-to-Speech Converter using Gemini and gTTS")

status = st.radio("Select an option:", ("Enter Text", "Upload a file"))
if status == "Enter Text":
    input_text = st.text_area("Enter text to translate and convert to speech:", height=200)
else:
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "csv", "xlsx", "pdf"])
    input_text = ""
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            input_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            input_text = df.to_string() # Convert DataFrame to string
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(uploaded_file)
            input_text = df.to_string()
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page_num in range(len(pdf_reader.pages)):
                input_text += pdf_reader.pages[page_num].extract_text()
        st.text_area("Extracted Text", input_text, height=200)

language_code_map = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Arabic": "ar",
    "Chinese": "zh",
    "Hindi": "hi"
}
target_language = st.selectbox("Select target language for translation:", list(language_code_map.keys()))

if st.button("Translate and Convert to Speech"):
    if input_text.strip() == "":
        st.warning("Please enter some text to translate and convert.")
    else:
        translated_text = translate_text_gemini(input_text, target_language)
        if translated_text:
            st.subheader("Translated Text:")
            st.write(translated_text)
            language_code = language_code_map[target_language]
            st.write(language_code)
            audio_file_path = text_to_speech(translated_text, language_code)
            st.write("Generated Audio:",audio_file_path)
            if audio_file_path:
                st.audio(audio_file_path, format='audio/mp3')
                with open(audio_file_path, "rb") as f:
                    st.download_button(
                        label="Download Audio",
                        data=f,
                        file_name="translated_speech.mp3",
                        mime="audio/mp3"
                    )
                os.remove(audio_file_path)  # Clean up temporary file

hide_github_icon = """
        <style>
        #GithubIcon {
            visibility: hidden;
        }
        </style>
        """
        st.markdown(hide_github_icon, unsafe_allow_html=True)
