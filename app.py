import os
from apikey import api_key
import streamlit as st 
import anki_utils
import requests
import json
import urllib.request
import time
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from utils import get_initial_message, get_chatgpt_response, update_chat
from dotenv import load_dotenv
from streamlit_chat import message

os.environ['OPENAI_API_KEY'] = api_key

template = """Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to tutor native English speakers in learning the Chinese language. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

{history}
Human: {human_input}
Assistant:"""


if __name__ == '__main__':
    #st.title('LangChain Test') 
    st.set_page_config(page_title='LangChain Test', page_icon='🤖', layout='wide')
    #prompt = st.text_input('Enter a prompt:')

    # llms
    llm = OpenAI()

    # anki
    deck_name = "Chinese::Vocabulary::Vocabulary"
    due_card_ids = anki_utils.get_due_ids(deck_name=deck_name, limit=1)

    

    due_note_info, due_card_info = anki_utils.get_note_and_card_info(due_card_ids)

    #print(due_card_info)
    
    first_key, first_value = next(iter(due_note_info.items()))
    vocab_word = due_note_info[first_key]['fields']['Vocab']['value']

    # Open the deck for review
    #anki_utils.open_deck_review(deck_name)

    # Wait for a few seconds to ensure the review window is open and the card is displayed
    #time.sleep(2)
    #anki_utils.gui_answer_current_card(ease=1)

    # Make a request to get the information for the due cards
    #payload = {"action": "cardsInfo", "params": {"cards": card_ids}}
    #card_info = anki_utils.invoke(payload)

    #prompt = "Create a Chinese sentence using the word " + vocab_word + " using traditional characters. Disclude pinyin."
    prompt = "Translate " + vocab_word + " into English and write an English sentence using the translated word. Then request from the user the Chinese translation."

    #prompt = PromptTemplate(
    #input_variables=["history", "human_input"], 
    #template=template
    #)
#
#
    #chatgpt_chain = LLMChain(
    #llm=OpenAI(), 
    #prompt=prompt, 
    #verbose=True, 
    #memory=ConversationBufferWindowMemory(k=2),
    #)

    #output = chatgpt_chain.predict(human_input=f"You are tutoring me, an English speaking student, to learn chinese. Give a mini-lesson introducing the word {vocab_word}. Be concise, as there are many words to get through after. Ask me questions as you go to guide the lesson and to track my comprehension.")
    #print(output)
    
    #print(due_note_info)

    #print((due_note_info[1661739501383]))
    #print(due_card_info)

    # Print the card information
    #for card in due_card_info:
    #    print(card["vocab"])
    #    print(card["pinyin"])



    # show stuff to the screen if there's a prompt
    #if prompt:
    #    response = llm(prompt)
    #    st.write(response)

    os.environ['OPENAI_API_KEY'] = api_key
    load_dotenv()
    st.title("Chatbot : ChatGPT and Streamlit Chat")
    #st.subheader("AI Tutor:")

    model = st.selectbox(
        "Select a model",
        ("gpt-3.5-turbo", "gpt-4")
    )

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []

    query = st.text_input("Query: ", key="input")

    if 'messages' not in st.session_state:
        st.session_state['messages'] = get_initial_message()

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
            st.write(messages)


