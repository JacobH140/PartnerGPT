import streamlit as st
from streamlit_chat import message
from utils import get_initial_message, get_chatgpt_response, get_chatgpt_response_stream_chunk, update_chat
import os
from dotenv import load_dotenv
import openai
from apikey import api_key
import anki_utils
from collections import defaultdict
import time
from io import BytesIO
from gtts import gTTS
from urllib.parse import quote
import base64
from bokeh.models.widgets import Button
from bokeh.models import CustomJS


os.environ['OPENAI_API_KEY'] = api_key 
load_dotenv()

def stream_chat_completion(model, query, temperature=0):
    return openai.ChatCompletion.create(
        model=model,
        messages=[
            {'role': 'user', 'content': query},
        ],
        temperature=temperature,
        stream=True  # again, we set stream=True
    )

if __name__ == '__main__':
    model = "gpt-3.5-turbo"
    query = "write a story in 10 words or less"



    tts_url_stem = "https://translate.google.com/translate_tts?ie=UTF-8&tl=zh-CN&client=tw-ob&q="

    with st.empty():
    # create variables to collect the stream of chunks
       collected_chunks = []
       collected_messages = []
       # iterate through the stream of events
       for chunk in stream_chat_completion(model, query):
           collected_chunks.append(chunk)  # save the event response
           chunk_message = chunk['choices'][0]['delta']  # extract the message
           collected_messages.append(chunk_message)  # save the message
           #message(''.join([m.get('content', '') for m in collected_messages]), key=str(len(collected_chunks)), avatar_style='shapes')
           st.success(''.join([m.get('content', '') for m in collected_messages]))
           #sound_file = BytesIO()
           #tts = gTTS('我们在首都机场跟熊猫打球PPT, where are you?', lang='zh-cn')
           #tts.write_to_fp(sound_file)
           #st.audio(sound_file)

    
    sound_file = BytesIO()
    tts = gTTS('我们在首都机场跟熊猫打球PPT, where are you?', lang='zh-cn')
    tts.write_to_fp(sound_file)
    audio_base64 = base64.b64encode(sound_file.read()).decode('utf-8')
    print("audio_base64", audio_base64)
    audio_tag = f'<audio control autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    print("src:", f"data:audio/mp3;base64,{audio_base64}")
    st.markdown(audio_tag, unsafe_allow_html=True)
    #st.audio(sound_file)
    
   
    audio_url = tts_url_stem + quote('他们在首都机场跟熊猫打球')
    test_url = "https://www.orangefreesounds.com/wp-content/uploads/2022/04/Small-bell-ringing-short-sound-effect.mp3" # remember to enable autoplay in browser settings
    test_url_2 = quote("https://translate.google.com/translate_tts?ie=UTF-8&tl=zh-CN&client=tw-ob&q=%E4%BB%96%E4%BB%AC%E5%9C%A8%E9%A6%96%E9%83%BD%E6%9C%BA%E5%9C%BA%E8%B7%9F%E7%86%8A%E7%8C%AB%E6%89%93%E7%90%83")
    html_string = f"""
            <audio autoplay="true">
              <source src={test_url} type="audio/mp3">
            </audio>
            """
    print(html_string)
    print(audio_url)
    sound = st.empty()
    sound.markdown(html_string, unsafe_allow_html=True)  # will display a st.audio with the sound you specified in the "src" of the html_string and autoplay it
    #time.sleep(10)  # wait for 2 seconds to finish the playing of the audio
    #sound.empty()  # op

    