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

if 'vocab_words' not in st.session_state:
    st.session_state['vocab_words'] = ["滑冰", "大象", "默契", "矛盾"]


#def form_callback():


def get_next_vocab_word():
    deck_name = "Chinese::Vocabulary::Vocabulary"
    due_card_ids = anki_utils.get_due_ids(deck_name=deck_name, limit=1)
    due_note_info, due_card_info = anki_utils.get_note_and_card_info(due_card_ids)
    first_key, first_value = next(iter(due_note_info.items()))
    voc_word = due_note_info[first_key]['fields']['Vocab']['value']
    return st.session_state['vocab_words'].pop() # temp

if __name__ == '__main__':


    st.title("heading")
    st.subheader("subheading")
    

    model = st.selectbox("Select a model", ("gpt-3.5-turbo", "gpt-4"))

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
   
    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if 'proceed_button_clicked' not in st.session_state:
        st.session_state['proceed_button_clicked'] = False
    
    if 'current_ratings' not in st.session_state:
        st.session_state['current_ratings'] = defaultdict(lambda: None)

    if 'form_submitted' not in st.session_state:
        st.session_state['form_submitted'] = False

    if 'main_words' not in st.session_state:
        st.session_state['main_words'] = []

    query = st.text_input("You: ", key="input", disabled=False)

    if st.button("Begin" if not st.session_state['proceed_button_clicked'] else "Next", key="proceed_button"):
        print("next")
        #if 'messages' not in st.session_state:
        vocab_word = get_next_vocab_word()
        aux_words= ["熊猫", "首都机场", "常常"]
        st.session_state['main_words'].append(vocab_word)
        st.session_state['messages'] = get_initial_message(vocab_word=vocab_word, aux_words=aux_words)

        if not st.session_state['proceed_button_clicked']:
            query = "Let's begin!"
        else:
            query = "Next!"
        print("If region query: ", query)
    

        if st.session_state['proceed_button_clicked']:
            # Create a form
            with st.form('Rating Form'):
                ratings = []
                for word in [st.session_state['main_words'][-2]] + aux_words:
                    st.session_state.current_ratings[word] = st.radio(word, ("Again", "Hard", "Good", "Easy"), horizontal=True)
                    #ratings.append(st.radio(word, ("Again", "Hard", "Good", "Easy"), horizontal=True))

                # Add a submit button to the form
                submitted = st.form_submit_button('Submit')

                st.session_state['form_submitted'] = submitted

            
        st.session_state['proceed_button_clicked'] = True
        if query:
            with st.spinner("generating..."):
                messages = st.session_state['messages']
                messages = update_chat(messages, "user", query)
                response = get_chatgpt_response(messages, model)
                messages = update_chat(messages, "assistant", response)
                st.session_state.past.append(query)
                st.session_state.generated.append(response)
        if st.session_state['generated']:
        
            for i in range(len(st.session_state['generated'])-1, -1, -1):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))

            with st.expander("Show Messages"):
                try:
                    st.write(messages)
                except NameError:
                    pass
            

    elif st.session_state['form_submitted']:
        print("form submitted")
        query = "" # no query here
        st.write("ratings: ", st.session_state.current_ratings)
        print("ratings: ", st.session_state.current_ratings)
        st.session_state['form_submitted'] = False

    else:
        print("ratings: ", st.session_state.current_ratings)
        print("Else region query: ", query)
        if query:
            with st.spinner("generating..."):
                messages = st.session_state['messages']
                messages = update_chat(messages, "user", query)
                response = get_chatgpt_response(messages, model)
                messages = update_chat(messages, "assistant", response)
                st.session_state.past.append(query)
                st.session_state.generated.append(response)

        if st.session_state['generated']:

            for i in range(len(st.session_state['generated'])-1, -1, -1):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))

            with st.expander("Show Messages"):
                try:
                    st.write(messages)
                except NameError:
                    pass

    
            

            



        
        


            
