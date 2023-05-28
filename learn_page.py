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
import gsheet_utils as gs

# READ: ----------------------------------------------------------------




from streamlit_bokeh_events import streamlit_bokeh_events

from gtts import gTTS
from io import BytesIO
import openai
openai.api_key = api_key

import chat_template

###def get_due_vocab_word(state_object): SUBSUMED BY get_chinese_anki_cards
###    if state_object.simpl_or_trad == "Simplified":
###        field_name = "简体字simplified"
###    else:
###        field_name = "繁体字traditional"
###    deck_name = "中文"
###    due_card_ids = anki_utils.get_due_ids(deck_name=deck_name, limit=1)
###    due_note_info, due_card_info = anki_utils.get_note_and_card_info(due_card_ids)
###    first_key, first_value = next(iter(due_note_info.items()))
###    voc_word = due_note_info[first_key]['fields'][field_name]['value']
###
###    return voc_word

#def get_chinese_anki_cards(state_object, status, limit=None):
#    if state_object.simpl_or_trad == "Simplified":
#        field_name = "简体字simplified"
#    else:
#        field_name = "繁体字traditional"
#    deck_name = "中文"
#
#    if status == "due":
#        card_ids = anki_utils.get_due_ids(deck_name=deck_name, limit=limit)
#    elif status == "new":
#        card_ids = anki_utils.get_new_ids(deck_name=deck_name, limit=limit)
#    elif status == "review":
#        card_ids = anki_utils.get_review_ids(deck_name=deck_name, limit=limit)
#    else:
#        raise ValueError("status must be 'due', 'new', or 'review'")
#    note_info, card_info = anki_utils.get_note_and_card_info(card_ids)
#
#    voc_words = [note_info[key]['fields'][field_name]['value'] for key in note_info.keys()] 
#
#    return voc_words

def learn_get_initial_message(learn_state):
    aux_words = ["小狗", '女朋友', '是吗'] # temp for now
    vocab_word = learn_state.custom['cards_new'].pop()[learn_state.simpl_or_trad]


    initial_system = f"""You are a Chinese language professor tutoring me, an English speaking student, in learning Chinese. Give a mini-lesson introducing the word {vocab_word}. Be concise, as there are many words to get through after. Quiz me as you go in order to move the lesson forward. When I make mistakes, you should correct and remember those mistakes. When I ask questions, you should answer in mostly English and remember those questions. Only include pinyin for new words."""
    initial_user = f"Guide me through the word {vocab_word}. During the lesson (e.g., when providing example sentences using {vocab_word}), incorporate usage of {aux_words[:]}. You should provide an example sentence before asking me to provide one. Use {st.session_state.learn_state.simpl_or_trad} Chinese characters."

    learn_state.to_review = [vocab_word] + aux_words
    messages=[
            {"role": "system", "content": initial_system},
            {"role": "user", "content": initial_user},
        ]
    return messages

def update_databases(learn_state):
    from_gsheet_new_cards, wks_new_cards = gs.access_gsheet_by_url_no_df(sheet_name="New")
    from_gsheet_reviewed_cache, wks_reviewed_cache_cards = gs.access_gsheet_by_url_no_df(sheet_name="Reviewed Cards Cache")
    excluded = {entry["id"] for entry in from_gsheet_reviewed_cache}
    learn_state.custom['cards_new'] = [entry for entry in from_gsheet_new_cards if entry["id"] not in excluded] # essentially a set minus


def next(learn_state):
    update_databases(learn_state)


if 'learn_state' not in st.session_state:
    st.session_state.learn_state = chat_template.SessionNonUIState()


st.session_state.next_func_args = (st.session_state.learn_state,)
    
if not st.session_state.learn_state.chatting_has_begun:
    model = st.selectbox("Select a model", ("gpt-3.5-turbo", "gpt-4"))
    st.session_state.learn_state.simpl_or_trad = st.selectbox("Simplified or Traditional", ("简体字simplified", "繁体字traditional"))
    st.session_state.learn_state.model = model

if 'cards_new' not in st.session_state.learn_state.custom:
    print("updating databases")
    update_databases(st.session_state.learn_state)

else:
    st.title("Learn")
    if not st.session_state.learn_state.custom['cards_new']:
        st.exception("There are no new words to learn right now! Head over to review to review some words, or converse to put things into practice...")
    




st.session_state.learn_state.to_create_prompt = "Repeat back: ['this', 'is', 'create', 'prompt']"
st.session_state.learn_state.initial_message_func = learn_get_initial_message
st.session_state.learn_state.initial_message_func_args = (st.session_state.learn_state,)

chat_template.chat(st.session_state.learn_state)

if st.session_state.learn_state.on_automatic_rerun:
    st.session_state.learn_state.on_automatic_rerun = False

