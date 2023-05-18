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
import string
from playsound import playsound
import re

openai.api_key = api_key



def autoplay_audio(file_path, key=None):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        if key is None:
            st.markdown(
                md,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                md,
                unsafe_allow_html=True,
                key=key
            )
            


def has_punctuation(s):
    punctuation = r"""!?.,;:。。，()[]？""" 
    return any([c in punctuation for c in s])


def remove_spaces_punctuation(input_string):
    # Remove spaces
    input_string = input_string.replace(" ", "")
    
    # Remove punctuation
    input_string = input_string.translate(str.maketrans("", "", string.punctuation))
    
    return input_string

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
    query = "write a question in chinese that uses using 受不了了. then immediately after write a sentence in english about cats. no paragraph break."



    tts_url_stem = "https://translate.google.com/translate_tts?ie=UTF-8&tl=zh-CN&client=tw-ob&q="

    if 'response_so_far' not in st.session_state:
        st.session_state['response_so_far'] = ""

    if 'currently_sonifying' not in st.session_state:
        st.session_state['currently_sonifying'] = ""

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
           #st.success(''.join([m.get('content', '') for m in collected_messages]))
           #sound_file = BytesIO()
           #tts = gTTS('我们在首都机场跟熊猫打球PPT, where are you?', lang='zh-cn')
           #tts.write_to_fp(sound_file)
           #st.audio(sound_file)
           #print(collected_messages[-1].get('content ', ''))
           #print(chunk_message.get('content', ''))
           response_so_far = ''.join([m.get('content', '') for m in collected_messages])
           #st.success(response_so_far)

           prev_response_so_far = st.session_state['response_so_far']
           if len(response_so_far) > len(prev_response_so_far):
                st.success(response_so_far)
                print("new response_so_far", response_so_far)
                print("old response_so_far", prev_response_so_far)
                to_sonify = response_so_far[len(prev_response_so_far):len(response_so_far)]
                #print("to_sonify", to_sonify)
                

                
                #print(response_so_far[-1])
                #to_sonify = response_so_far[-1]
                #print("next part", to_sonify)
                #test = "你受不了了什么?"
                #print("TEST", has_punctuation(test))

                if has_punctuation(to_sonify): # only sonify clause-like structures
                    tts = gTTS(to_sonify, lang='zh-cn')
                    tts.save(to_sonify + '.mp3')
                    #autoplay_audio(to_sonify + '.mp3')
                    playsound(to_sonify + '.mp3')
                    print("sonifying: ", to_sonify)
                    #st.audio(to_sonify + '.mp3')
                    st.session_state['response_so_far'] = response_so_far
                    #st.audio(to_sonify + '.mp3')
                    st.session_state['currently_sonifying'] = to_sonify
                    st.success(response_so_far)
                    #autoplay_audio(st.session_state['currently_sonifying'] + '.mp3')
                    #time.sleep(3) 
                    
                    
          # if st.session_state['currently_sonifying']:
            

            #time.sleep(2)
            #st.audio(st.session_state['currently_sonifying'] + '.mp3') 
            #playsound(st.session_state['currently_sonifying'] + '.mp3')
            #pass
           
    #tts = gTTS(st.session_state.response_so_far, lang='zh-cn')
    #tts.save("test" + '.mp3')
    #autoplay_audio("test" + '.mp3')

    
    #sound_file = BytesIO()
    #tts = gTTS('我们在首都机场跟熊猫打球PPT, where are you?', lang='zh-cn')
    #tts.write_to_fp(sound_file)
    #audio_base64 = base64.b64encode(sound_file.read()).decode('utf-8')
    #print("audio_base64", audio_base64)
    #audio_tag = f'<audio control autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    #print("src:", f"data:audio/mp3;base64,{audio_base64}")
    #st.markdown(audio_tag, unsafe_allow_html=True)
    #st.audio(sound_file)

    #tts = gTTS('我们在首都机场跟熊猫打球PPT, where are you?', lang='zh-cn')
    #tts.save("test.mp3")
    #st.write("# Auto-playing Audio!")
    #autoplay_audio("test.mp3")    
    
   
    #audio_url = tts_url_stem + quote('他们在首都机场跟熊猫打球')
    #test_url = "https://www.orangefreesounds.com/wp-content/uploads/2022/04/Small-bell-ringing-short-sound-effect.mp3" # remember to enable autoplay in browser settings
    #test_url_2 = quote("https://translate.google.com/translate_tts?ie=UTF-8&tl=zh-CN&client=tw-ob&q=%E4%BB%96%E4%BB%AC%E5%9C%A8%E9%A6%96%E9%83%BD%E6%9C%BA%E5%9C%BA%E8%B7%9F%E7%86%8A%E7%8C%AB%E6%89%93%E7%90%83")
    #html_string = f"""
    #        <audio autoplay="true">
    #          <source src={test_url} type="audio/mp3">
    #        </audio>
    #        """
    #print(html_string)
    #print(audio_url)
    #sound = st.empty()
    #sound.markdown(html_string, unsafe_allow_html=True)  # will display a st.audio with the sound you specified in the "src" of the html_string and autoplay it
    #time.sleep(10)  # wait for 2 seconds to finish the playing of the audio
    #sound.empty()  # op

    