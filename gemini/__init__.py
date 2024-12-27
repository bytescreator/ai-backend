import logging

import google.generativeai as genai
import markdown
from bs4 import BeautifulSoup
from electron.messaging import json_dump
from speech.piper.process import WrappedSynth

genai.configure(api_key="AIzaSyBjcp4nPRf-AZ_E_y5psFuV4Emzxar6Gn8")
model = genai.GenerativeModel("gemini-1.5-flash", safety_settings={}, system_instruction="""\
Sen sesli konuşabilen bir bilgisayar asistanısın.\
Kesinlikle ve kesinlikle yalnızca Türkçe cevap vermelisin çünkü konuşmaların \
sesli olarak kullanıcıya iletilecektir ve ses çeviricisi yalnızca Türkçe \
konuşabilmekte bunun yanında çok uzatmadan açık bir şekilde cevap vermelisin.\
Amacın hızlı bir şekilde kullanıcın isteklerini tamamlayarak kullanıcıya yardımcı olmaktır.\
""")


def send_text(text: str):
    txt = model.generate_content(text).text
    json_dump({"action": "on-llm-response", "text": txt})
    # WrappedSynth.synth(_sanitize_output(txt))


def _sanitize_output(text: str) -> str:
    return "".join(BeautifulSoup(markdown.markdown(text), features="html.parser").findAll(text=True))
