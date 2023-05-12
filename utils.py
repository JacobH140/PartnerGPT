import openai
from apikey import api_key
import os

def get_initial_message(vocab_word, aux_words):
    messages=[
            {"role": "system", "content": f"You are a Chinese language professor tutoring me, an English speaking student, in learning Chinese. Give a mini-lesson introducing the word {vocab_word}. Be concise, as there are many words to get through after. Quiz me as you go in order to move the lesson forward. When I make mistakes, you should correct and remember those mistakes. When I ask questions, you should answer in mostly English and remember those questions. Only include pinyin for new words."},
            {"role": "user", "content": f"Guide me through the word {vocab_word}. During the lesson (e.g., when providing example sentences using {vocab_word}), incorporate usage of {aux_words[:]}. You should provide an example sentence before asking me to provide one."},
            {"role": "assistant", "content": f"Let's start with the etymology of {vocab_word}..., then we'll move on to discuss some example senntences..."},
        ]
    return messages

def get_chatgpt_response(messages, model="gpt-3.5-turbo"):
    print("model: ", model)
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
    )
    return  response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages