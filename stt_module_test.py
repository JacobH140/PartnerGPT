import stt
import UI
import streamlit as st

if __name__ == "__main__":
    if 'fish' not in st.session_statea:
        st.session_state['fish'] = UI.SessionNonUIState()
    nonUI_state = st.session_state.fish
    mic, user, next_button = st.columns([2,30,4])
    with mic:
        if 'query' not in st.session_state:
            st.session_state['stt_session'] = 0 # init
        button = stt.mic_button(st.session_state)
    with user:
        stt.mic_button_monitor(nonUI_state, button, st.session_state)
        
    with next_button:
        st.button("Next", key="next_button", disabled=True) 