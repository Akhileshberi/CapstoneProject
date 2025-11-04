import google.generativeai as genai

# Configure your API key
YOUR_API_KEY ="AIzaSyCBlOZoLEQQtDUDN9_cjqp3C_qQCQwMQuc"
genai.configure(api_key=YOUR_API_KEY)

# Example for Gemini 1.5 Pro
#model_pro = genai.GenerativeModel('gemini-1.5-pro')
#response_pro = model_pro.generate_content("Translate the following text to French: 'Hello, how are you?'")
#print(f"Gemini 1.5 Pro response: {response_pro.text}")

# Example for Gemini 1.5 Flash
#model_flash = genai.GenerativeModel('gemini-1.5-flash')
#response_flash = model_flash.generate_content("Translate the following text to French: 'Hello, how are you?'")
#print(f"Gemini 1.5 Flash response: {response_flash.text}")


for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(model.name)