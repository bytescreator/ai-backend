import logging

import google.generativeai as genai
import markdown
from bs4 import BeautifulSoup
from electron.messaging import json_dump
from speech.piper.process import WrappedSynth

from . import actions


def extract_functions():
    return [getattr(getattr(actions, elem), name) for elem in dir(actions) for name in dir(getattr(
        actions, elem)) if name.startswith("invokable_")]


genai.configure(api_key="AIzaSyBjcp4nPRf-AZ_E_y5psFuV4Emzxar6Gn8")
model = genai.GenerativeModel("gemini-2.0-flash-exp", safety_settings={}, system_instruction="""\
Sen sesli konuşabilen bir bilgisayar asistanısın. Adın A.S.T.R.A .\
Kullanıcının girdisi sonucu genellikle bir ya da birden fazla fonksiyon çağrısı yaparak veri toplayacaksın \
ki kullanıcıya sistemi ile alakalı konularda yardımcı olabilesin. Fonksiyon çağırısı yapmaktan çekinme. \
Kesinlikle ve kesinlikle yalnızca Türkçe cevap vermelisin çünkü konuşmaların \
sesli olarak kullanıcıya iletilecektir ve ses çeviricisi yalnızca Türkçe \
konuşabilmekte bunun yanında çok uzatmadan açık bir şekilde cevap vermelisin.\
Amacın hızlı bir şekilde kullanıcın isteklerini tamamlayarak kullanıcıya yardımcı olmaktır.\
""", tools=extract_functions(), tool_config={"function_calling_config": {"mode": "AUTO"}})
session = model.start_chat(enable_automatic_function_calling=True)


def new_session():
    global session
    session = model.start_chat(enable_automatic_function_calling=True)


def rewind_session():
    session.rewind()


def send_text(text: str, voice_activated: bool):
    try:
        resp = session.send_message(text)
    except Exception as e:
        logging.error(f"send_message raised an exception: {e}")
        raise e
    logging.info(f"llm returned {resp}")
    txt = resp.text
    json_dump({"action": "on-llm-response", "text": txt})

    if voice_activated:
        WrappedSynth.synth(_sanitize_output(txt))


def _sanitize_output(text: str) -> str:
    return "".join(BeautifulSoup(markdown.markdown(text), features="html.parser").findAll(text=True))
