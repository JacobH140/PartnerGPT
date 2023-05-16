import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS

from streamlit_bokeh_events import streamlit_bokeh_events

from gtts import gTTS
from io import BytesIO
import openai

from apikey import api_key

openai.api_key = api_key

if 'prompts' not in st.session_state:
    st.session_state['prompts'] = [{"role": "system", "content": "You are a helpful assistant. Answer as concisely as possible with a little humor expression."}]

def generate_response(prompt):

    st.session_state['prompts'].append({"role": "user", "content":prompt})
    completion=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = st.session_state['prompts']
    )
    
    message=completion.choices[0].message.content
    return message

sound = BytesIO()

placeholder = st.container()

placeholder.title("Yeyu's Voice ChatBot")
mic, user, next_button = st.columns([2,30,4])
with mic:
    stt_button = Button(label='🎙️', button_type='success')

with user:
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

    tr.text_area("**Your input**", value=st.session_state['input']['text'])

    if result:
        if "GET_TEXT" in result:
            print("GET_TEXT in result")
            if result.get("GET_TEXT")["t"] != '' and result.get("GET_TEXT")["s"] != st.session_state['input']['session'] : # "s" for "session", "t" for "text"
                print(f"""result.get("GET_TEXT")["t"] = {result.get("GET_TEXT")["t"]} and result.get("GET_TEXT")["s"] = {result.get("GET_TEXT")["s"]} != st.session_state['input']['session'] (which is {st.session_state['input']['session']})""")
                st.session_state['input']['text'] = result.get("GET_TEXT")["t"]
                tr.text_area("**Your input**", value=st.session_state['input']['text'])
                st.session_state['input']['session'] = result.get("GET_TEXT")["s"]

        if "GET_INTRM" in result:
            print("GET_INTRM in result")
            if result.get("GET_INTRM") != '':
                print("""result.get("GET_INTRM") = """ + result.get("GET_INTRM"))
                tr.text_area("**Your input**", value=st.session_state['input']['text']+' '+result.get("GET_INTRM"))

        if "GET_ONREC" in result:
            print("GET_ONREC in result")
            if result.get("GET_ONREC") == 'start':
                print("result.get('GET_ONREC') == 'start'")
                #placeholder.image("recon.gif")
                st.session_state['input']['text'] = ''
            elif result.get("GET_ONREC") == 'running':
                print("result.get('GET_ONREC') == 'running'")
                #placeholder.image("recon.gif")
            elif result.get("GET_ONREC") == 'stop':
                print("result.get('GET_ONREC') == 'stop'")
                #placeholder.image("recon.jpg")

with next_button:
    st.button("Next", key="next_button", disabled=True) 
