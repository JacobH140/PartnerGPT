import streamlit as st
from streamlit_chat import message
from utils import get_initial_message, get_chatgpt_response, update_chat
import os
from dotenv import load_dotenv
import openai
from apikey import api_key
import anki_utils
from collections import defaultdict
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

    def generate_bot_response(self, query):
        with st.spinner("generating..."):
            messages = self.messages
            messages = update_chat(messages, "user", query)
            response = get_chatgpt_response(messages, self.model)
            messages = update_chat(messages, "assistant", response)
            state.past.append(query)
            state.generated.append(response)
        return messages

def initialize_app(heading, subheading):
    st.title(heading)
    st.subheader(subheading)
    
    model = st.selectbox("Select a model", ("gpt-3.5-turbo", "gpt-4", "ada"))
    if 'state' not in st.session_state:
        st.session_state.state = SessionState()
        st.session_state.state.model = model
    return st.session_state.state

def update_UI_messages(state_object):
    for i in range(len(state_object.generated)-1, -1, -1):
        message(state_object.past[i], is_user=True, key=str(i) + '_user')
        message(state_object.generated[i], key=str(i))

def expander_messages_widget(state_object):
    with st.expander("Show Messages"):
        try:
            st.write(state_object.messages)
        except NameError:
            pass



def rating_form(state_object):
    # Create a form
    def on_click():
        state_object.form_submitted=True
        for word in [state_object.current_vocab_word] + state_object.current_aux_words:
            state.current_ratings[word] = r

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
    query = st.text_input("You: ", key="input")
    ratings = []
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
        state.messages = get_initial_message(vocab_word=state.current_vocab_word, aux_words=state.current_aux_words)

        if not state.begin_button_has_been_clicked:
            query = "Let's begin!"
        else:
            query = "Next!"
        print("If region query: ", query)
    


            
        state.begin_button_has_been_clicked = True
        if query:
            state.messages = state.generate_bot_response(query)

        if state.generated:
            update_UI_messages(state)
            expander_messages_widget(state)
            

    elif state.form_submitted:
        print("form submitted")
        query = "" # no query here
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
        print("Else region query: ", query)
        if query:
            state.generate_bot_response(query)

        if state.generated:
            update_UI_messages(state)
            expander_messages_widget(state)
    
            

            



        
        


            
