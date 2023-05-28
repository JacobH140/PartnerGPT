import streamlit as st
from streamlit_chat import message
from utils import get_initial_message, get_chatgpt_response, get_chatgpt_response_stream_chunk, update_chat, stream_chat_completion
import os
from dotenv import load_dotenv
import openai
from apikey import api_key
import anki_utils
from collections import defaultdict
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from random import randrange
import stt
import string
from playsound import playsound
import base64






from streamlit_bokeh_events import streamlit_bokeh_events

from gtts import gTTS
from io import BytesIO
import openai
openai.api_key = api_key

import chat_template

def translate_get_initial_message(system_prompt, user_prompt):
    messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    return messages





if 'translate_state' not in st.session_state:
    st.session_state.translate_state = chat_template.SessionNonUIState()
    
if not st.session_state.translate_state.chatting_has_begun:
    model = st.selectbox("Select a model", ("gpt-3.5-turbo", "gpt-4"))
    st.session_state.translate_state.simpl_or_trad = st.selectbox("Simplified or Traditional", ("Simplified", "Traditional"))
    st.session_state.translate_state.model = model
else:
    st.title("Translate")



initial_system = """Your job is to help me translate between English and Chinese. Reply to my first message with 'What would you like to translate?'."""
initial_user = f"Please use {st.session_state.translate_state.simpl_or_trad} Chinese characters."

st.session_state.translate_state.initial_message_func = translate_get_initial_message
st.session_state.translate_state.initial_message_func_args = (initial_system, initial_user)

chat_template.chat(st.session_state.translate_state)

if st.session_state.translate_state.on_automatic_rerun:
    st.session_state.translate_state.on_automatic_rerun = False

