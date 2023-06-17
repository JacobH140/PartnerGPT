import openai
from apikey import api_key
import os
import ast
import time



def get_initial_message(vocab_word, aux_words, system_prompt=None, user_prompt=None):
    if system_prompt is None:
        print("system_prompt is None")
        system_prompt = f"""You are a Chinese language professor tutoring me, an English speaking student, in learning Chinese. Give a mini-lesson introducing the word {vocab_word}. Be concise, as there are many words to get through after. Quiz me as you go in order to move the lesson forward. When I make mistakes, you should correct and remember those mistakes. When I ask questions, you should answer in mostly English and remember those questions. Only include pinyin for new words."""
    if user_prompt is None:
        print("user_prompt is None")
        user_prompt = f"Guide me through the word {vocab_word}. During the lesson (e.g., when providing example sentences using {vocab_word}), incorporate usage of {aux_words[:]}. You should provide an example sentence before asking me to provide one."

    messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    return messages

def get_chatgpt_response(messages, temperature, model="gpt-3.5-turbo-16k", verbose=True, max_tries = 10):
    #print("model: ", model)
    sleep_seconds = 2
    try:
        if messages[-2]['role'] == 'system' and verbose:
            print("system: ", messages[-2]['content'])
    except IndexError:
        pass
    if verbose:
        print("user: ", messages[-1]['content'])

    tries = 0
    success = False
    while success == False:
        try:

            response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            stream=False,
            temperature=temperature,
            )
            if verbose:
                print("response: ", response['choices'][0]['message']['content'])
            success = True

        except openai.error.RateLimitError as r:
            if tries > max_tries:
                print("tried sleeping for up to ", sleep_seconds, "seconds, but still got rate limit error. Giving up")
                raise r
            else:
                tries += 1
                print("Encountered Rate Limit error: \n----\n", r, "\n----\n", "...will sleep for", sleep_seconds, "seconds")
                print("messags that are going over are: ", messages)
                time.sleep(sleep_seconds)
                sleep_seconds *= 2
                
        
    
    time.sleep(2) # to avoid overloading with requests
    return response['choices'][0]['message']['content']

def get_chatgpt_response_enforce_python_formatting(messages, response_on_fail, formatting_restriction="valid Python", extra_prompt=None, start_temperature=0, end_temperature=1, step=0.1, model="gpt-3.5-turbo-16k"):
    # returns whatever response_on_fail is if chatgpt is not working
    # extra_prompt gives a chance for the user to remind the bot how the output formatting should be organized
    # formatting_restriction is either "valid Python" or a user-provided bool-returning function
    temperature = start_temperature
    success = False
    response = "none yet"
    while not success:
        try:
            response = get_chatgpt_response(messages, temperature=temperature, model=model)
            #print("User: <placeholder>")
            #print("Response: ", response)
            if formatting_restriction == "valid Python":
                ast.literal_eval(response) # just testing to see if formatting works
            else:
                assert formatting_restriction(response) == True
            success = True
        except Exception as e:
            print("Encountered exception; response was:", response)
            print("EXCEPTION:", e)
            print("Trying again, cGPT gave incorrectly formatted output")
            temperature += step
            if extra_prompt:
                messages.append({"role": "user", "content": extra_prompt})
            if temperature > end_temperature:
                print("cGPT is not working, giving up")
                return str(response_on_fail)
    return response

def get_chatgpt_response_stream_chunk(messages, model="gpt-3.5-turbo-16k"):
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    stream=True,
    )
    # create variables to collect the stream of chunks
    collected_chunks = []
    collected_messages = []
    # iterate through the stream of events
    for chunk in response:
        collected_chunks.append(chunk)  # save the event response
        chunk_message = chunk['choices'][0]['delta']  # extract the message
        collected_messages.append(chunk_message)  # save the message

def update_chat(messages, role, content):
    print("chat updated, messages are now: ", messages)
    messages.append({"role": role, "content": content})
    return messages

def stream_chat_completion(messages, model, temperature=0):
    return openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        stream=True  # again, we set stream=True
    )

