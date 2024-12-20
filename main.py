import google.generativeai as genai

import gizlidosya

genai.configure(api_key=gizlidosya.api_key)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model= genai.GenerativeModel('gemini-pro')
response = model.generate_content("3 kere 4")
print(response.text)