import streamlit as st
from streamlit_chat import message
from utils import get_initial_message, get_chatgpt_response, get_chatgpt_response_stream_chunk, update_chat
import os
from dotenv import load_dotenv
import openai
from apikey import api_key
import anki_utils
from collections import defaultdict
from bokeh.models.widgets import Button
from bokeh.models import CustomJS

from streamlit_bokeh_events import streamlit_bokeh_events

from gtts import gTTS
from io import BytesIO
import openai
os.environ['OPENAI_API_KEY'] = api_key 
load_dotenv()

class SessionNonUIState:
    def __init__(self):
        self.chatting_has_begun = False
        self.model = None
        self.messages = []

        self.generated = []
        self.past = []
        self.reviewed = []

        self.submitted_ratings = defaultdict(lambda: None)
        self.administer_rating_form = False

    def generate_bot_response_placeholder(self, query):
        with st.spinner("generating..."):
            messages = self.messages
            messages = update_chat(messages, "user", query)
            response = "generated response placeholder for query " + query # this is where the model would be called etc
            messages = update_chat(messages, "assistant", response)
            self.generated.append(response)
            self.past.append(query)
            self.reviewed.append("")


        return messages
    
    def review_notif(self, str):
        self.generated.append("")
        self.past.append("")
        self.reviewed.append(str)

    def reset_submitted_ratings(self):
        self.submitted_ratings = defaultdict(lambda: None)
        assert(len(self.submitted_ratings) == 0)

def get_initial_message_placeholder():
    messages=[
            {"role": "system", "content": "system initial message placeholder"},
            {"role": "user", "content": "user initial message placeholder"},
            {"role": "assistant", "content": "assistant initial message placeholder"},
        ]
    return messages


    
 
def update_UI_messages(state_object):
    for i in range(len(state_object.generated)): # reverse iterate through list
        #st.info(state_object.past[i]) if state_object.past[i] else None # user messages
        #st.success(state_object.generated[i]) if state_object.generated[i] else None # bot responses
        #st.warning(state_object.reviewed[i]) if state_object.reviewed[i] else None # review notification for when the 'next' form is submitted

        # rewrite above using regular if statements, not as comment
        if state_object.past[i]:
            st.info(state_object.past[i])
        if state_object.generated[i]:
            st.success(state_object.generated[i])
        if state_object.reviewed[i]:
            st.warning(state_object.reviewed[i])



def initialize_app(heading, subheading):
    #st.title(heading)
    #st.subheader(subheading)
    if 'state' not in st.session_state:
        st.session_state.state = SessionNonUIState()

    if not st.session_state.state.chatting_has_begun:
        model = st.selectbox("Select a model", ("gpt-3.5-turbo", "gpt-4"))
        st.session_state.state.model = model
    
    return st.session_state.state

def expander_messages_widget(state_object):
    with st.sidebar.expander("Show Current Messages"):
        st.write(state_object.messages)
        

def rating_form(nonUI_state):
    def on_submit():
        nonUI_state.administer_rating_form = False
        st.balloons()

    with st.form('Rating Form', clear_on_submit=False):
        #for word in [state_object.main_words[-2]] + state_object.current_aux_words:
        for word in ["word1", "word2", "word3", "word4"]:
            r = st.radio(word, ("Again", "Hard", "Good", "Easy", "N/A"), horizontal=True)
            nonUI_state.submitted_ratings[word] = r
        return st.form_submit_button('Submit', on_click=on_submit)

def chat(nonUI_state):

    def clear_text():
        st.session_state["queried"] = st.session_state["query"]
        st.session_state["query"] = ""

    def on_proceed_button_click():
        nonUI_state.messages = get_initial_message_placeholder()
        if nonUI_state.chatting_has_begun:
            nonUI_state.administer_rating_form = True
            clear_text()
        
        if 'query' in st.session_state and not nonUI_state.administer_rating_form:
            st.session_state.queried = '**next !**'
            nonUI_state.messages = nonUI_state.generate_bot_response_placeholder(query=st.session_state.queried)
            clear_text()
        elif not nonUI_state.administer_rating_form:
            nonUI_state.messages = nonUI_state.generate_bot_response_placeholder(query='**begin !**')
            #st.markdown("<details> <summary>Details</summary> Something small enough to escape casual notice. </details>", unsafe_allow_html=True)
        
        nonUI_state.chatting_has_begun = True
        



    if "queried" not in st.session_state:
        st.session_state["queried"] = ""
    
    #st.button("Begin" if not nonUI_state.chatting_has_begun else "Next", key="proceed_button", on_click=on_proceed_button_click)
    if not nonUI_state.chatting_has_begun:
        st.button("Begin", key="begin_button", on_click=on_proceed_button_click)


    if 'query' in st.session_state and st.session_state.queried:
        nonUI_state.messages = nonUI_state.generate_bot_response_placeholder(st.session_state.queried)

    if nonUI_state.generated:
        if nonUI_state.submitted_ratings:
            nonUI_state.review_notif("**Submitted ratings for <num_items> items: <items>**")
            print(nonUI_state.submitted_ratings)
            nonUI_state.reset_submitted_ratings()
        update_UI_messages(nonUI_state)
        


    if nonUI_state.administer_rating_form:
        rating_form(nonUI_state)
        #nonUI_state.reviewed.append("**Submitted reviews for <num_items> items: <items> !**")

    
    if nonUI_state.chatting_has_begun:
        st.divider()
        mic, user, next_button = st.columns([2,30,4])
        with mic:
            st.button("🎙️", key="mic_button", disabled=nonUI_state.administer_rating_form)
        with user:
            st.text_input("You: ", placeholder='speak or type', key="query", label_visibility="collapsed", on_change=clear_text, disabled=nonUI_state.administer_rating_form)
        with next_button:
            st.button("Next", key="next_button", on_click=on_proceed_button_click, disabled=nonUI_state.administer_rating_form)

    
    if nonUI_state.generated:
        expander_messages_widget(nonUI_state)


if __name__ == '__main__':
    nonUI_state = initialize_app("header", "subheader")
    chat(nonUI_state)


#https://stackoverflow.com/questions/52718897/minimal-shortest-html-for-clickable-show-hide-text-or-spoiler
