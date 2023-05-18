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


def get_next_vocab_word():
    deck_name = "Chinese::Vocabulary::Vocabulary"
    due_card_ids = anki_utils.get_due_ids(deck_name=deck_name, limit=1)
    due_note_info, due_card_info = anki_utils.get_note_and_card_info(due_card_ids)
    first_key, first_value = next(iter(due_note_info.items()))
    voc_word = due_note_info[first_key]['fields']['Vocab']['value']

    #vocab_words_testing_temp = ["滑冰", "大象", "默契", "矛盾"] # temp, just for testing purposes currently
    return state.vocab_words_testing_temp.pop() # temp

def get_next_aux_words():
    return ["熊猫", "首都机场", "常常"] # temporary for testing

class SessionState:
    def __init__(self):
        self.vocab_words_testing_temp = ["滑冰", "大象", "默契", "矛盾"]
        self.generated = []
        self.past = []
        self.begin_button_has_been_clicked = False
        self.current_ratings = defaultdict(lambda: None)
        self.form_submitted = False
        self.current_vocab_word = None
        self.current_aux_words = None
        self.messages = []
        self.model = None
        #self.main_words = []
    
    def stream_chat_completion(self, messages, temperature=0):
        return openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            stream=True  # again, we set stream=True
        )

    def generate_bot_response(self, query, stream=False):
        with st.spinner("generating..."):
            messages = self.messages
            messages = update_chat(messages, "user", query)
            if not stream:
                response = get_chatgpt_response(messages, self.model)
                
                
            else:
                with st.empty():
                # create variables to collect the stream of chunks
                   collected_chunks = []
                   collected_messages = []
                   # iterate through the stream of events
                   for chunk in self.stream_chat_completion(messages):
                       collected_chunks.append(chunk)  # save the event response
                       chunk_message = chunk['choices'][0]['delta']  # extract the message
                       collected_messages.append(chunk_message)  # save the message
                       st.success(''.join([m.get('content', '') for m in collected_messages]))
                response = ''.join([m.get('content', '') for m in collected_messages])
                
            messages = update_chat(messages, "assistant", response)
            state.generated.append(response)
            state.past.append(query)
            #state.generated.append(response)
        return messages
    
    

def initialize_app(heading, subheading):
    st.title(heading)
    st.subheader(subheading)
    
    model = st.selectbox("Select a model", ("gpt-3.5-turbo", "gpt-4"))
    if 'state' not in st.session_state:
        st.session_state.state = SessionState()
        st.session_state.state.model = model
    return st.session_state.state

def update_UI_messages(state_object):
    for i in range(len(state_object.generated)-1, -1, -1): # reverse iterate through list
        #message(state_object.past[i], is_user=True, key=str(i) + '_user')
        st.info(state_object.past[i])
        #message(state_object.generated[i], key=str(i))
        st.success(state_object.generated[i])

def expander_messages_widget(state_object):
    with st.expander("Show Messages"):
        try:
            st.write(state_object.messages)
        except NameError:
            pass

def user_stt():
    placeholder = st.container()

    stt_button = Button(label='🎙️', button_type='success')


    stt_button.js_on_event("button_click", CustomJS(code="""
        var value = "";
        var rand = 0;
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'zh-CN';

        document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'start'}));

        recognition.onspeechstart = function () {
            document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'running'}));
        }
        recognition.onsoundend = function () {
            document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'stop'}));
        }
        recognition.onresult = function (e) {
            var value2 = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                    rand = Math.random();

                } else {
                    value2 += e.results[i][0].transcript;
                }
            }
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: {t:value, s:rand}}));
            document.dispatchEvent(new CustomEvent("GET_INTRM", {detail: value2}));

        }
        recognition.onerror = function(e) {
            document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'stop'}));
        }
        recognition.start();
        """))

    result = streamlit_bokeh_events(
        bokeh_plot = stt_button,
        events="GET_TEXT,GET_ONREC,GET_INTRM",
        key="listen",
        refresh_on_update=False,
        override_height=75,
        debounce_time=0)

    tr = st.empty()

    if 'input' not in st.session_state:
        st.session_state['input'] = dict(text='', session=0)
        print("init session state input", st.session_state['input'])
        print(type(st.session_state['input']))

    print("session state input: ", st.session_state.input)
    tr.text_area("**Your input**", value=st.session_state['input']['text'])
    

    if result:
        if "GET_TEXT" in result:
            if result.get("GET_TEXT")["t"] != '' and result.get("GET_TEXT")["s"] != st.session_state['input']['session'] :
                st.session_state['input']['text'] = result.get("GET_TEXT")["t"]
                tr.text_area("**Your input**", value=st.session_state['input']['text'])
                st.session_state['input']['session'] = result.get("GET_TEXT")["s"]

        if "GET_INTRM" in result:
            if result.get("GET_INTRM") != '':
                tr.text_area("**Your input**", value=st.session_state['input']['text']+' '+result.get("GET_INTRM"))

        if "GET_ONREC" in result:
            if result.get("GET_ONREC") == 'start':
                placeholder.image("recon.gif")
                st.session_state['input']['text'] = ''
            elif result.get("GET_ONREC") == 'running':
                placeholder.image("recon.gif")
            elif result.get("GET_ONREC") == 'stop':
                placeholder.image("recon.jpg")
                if st.session_state['input']['text'] != '':
                    input = st.session_state['input']['text']

                    return input
    return False



def rating_form(state_object):
    # Create a form
    def on_click():
        #state_object.form_submitted=True
        for word in [state_object.current_vocab_word] + state_object.current_aux_words:
            state.current_ratings[word] = r
            st.balloons()

    with st.form('Rating Form'):
        ratings = []
        #for word in [state_object.main_words[-2]] + state_object.current_aux_words:
        for word in [state_object.current_vocab_word] + state_object.current_aux_words:
            r = st.radio(word, ("Again", "Hard", "Good", "Easy", "N/A"), horizontal=True)
            print("r: ", r)
            state.current_ratings[word] = r
            ratings.append(r)
            #ratings.append(st.radio(word, ("Again", "Hard", "Good", "Easy"), horizontal=True)
        return st.form_submit_button('Submit', on_click=on_click), state.current_ratings


if __name__ == '__main__':
    state = initialize_app("heading", "subheading")

    st.text_input("You: ", placeholder='speak or type', key="query", label_visibility="collapsed")
    ratings = []
    #user_stt()
    if st.button("Begin" if not state.begin_button_has_been_clicked else "Next"):
        print("next")
        if state.begin_button_has_been_clicked:
            state.form_submitted, ratings = rating_form(state)
            print("form submitted: ", state.form_submitted)
            #for index, word in enumerate(state.current_ratings.keys()):
            #    state.current_ratings[word] = ratings[index]
            print("other ratings: ", state.current_ratings)
        #if 'messages' not in st.session_state:
        state.current_vocab_word = get_next_vocab_word()
        state.current_aux_words = get_next_aux_words()
        #state.main_words.append(state.current_vocab_word)
        if state.form_submitted:
            state.messages = get_initial_message(vocab_word=state.current_vocab_word, aux_words=state.current_aux_words)
            state.form_submitted = False
        #if not state.begin_button_has_been_clicked:
        #    st.session_state.query = "Let's begin!"
        #else:
        #    st.session_state.query = "Next!"
        #print("If region query: ", st.session_state.query)
        state.begin_button_has_been_clicked = True
        if st.session_state.query:
            state.messages = state.generate_bot_response(st.session_state.query, stream=True)
            #st.session_state.query = ""
        if state.generated:
            update_UI_messages(state)
            expander_messages_widget(state)
    elif state.form_submitted:
        print("form submitted")
        #query = "" # no query here
        #st.write("ratings: ", state.current_ratings)
        #for i, word in enumerate([state.current_vocab_word] + state.current_aux_words):
            #print(i)
            #state.current_ratings[word] = ratings[i]
        print("ratings: ", state.current_ratings)
        state.form_submitted = False
        if state.generated:
            update_UI_messages(state)
            expander_messages_widget(state)
    else:
        print("ratings: ", state.current_ratings)
        print("Else region query: ", st.session_state.query)
        if st.session_state.query:
            state.generate_bot_response(st.session_state.query, stream=True)
            #st.session_state.query = ""
        if state.generated:
            update_UI_messages(state)
            expander_messages_widget(state)
    
            

            



        
        


            
