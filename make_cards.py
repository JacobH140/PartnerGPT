import pandas as pd
import json
import urllib.request
from urllib.parse import urlencode
from urllib.parse import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict
import ImageScraper
import anki_utils
#import pinyin
#import chinese_converter
import requests
import os
#import jieba
#import gsheet_utils as gs
import numpy as np
import re
import utils
from apikey import api_key
import openai
import ast
# import dictionary
from hanzipy.decomposer import HanziDecomposer
decomposer = HanziDecomposer()
# import decomposer
from hanzipy.dictionary import HanziDictionary
dictionary = HanziDictionary()
import chinese_nlp_utils as cnlp
openai.api_key = api_key

def add_images(filtered_df, query_col="vocab", tries_before_giving_up=3):
    # query_col gives us the searches from which images are scraped
    urls = []
    for voc in filtered_df.loc[:, query_col].tolist():
        approved_exts = [".jpg", ".png", ".jpeg"]
        number_of_images = 1
        try:
            image_options = ImageScraper.scrape_images([voc], number_of_images=number_of_images)[0] # res is still a list since I.S. outputs list of lists
        except IndexError:
            image_options = ["(NO IMAGE AVAILABLE)"]
        image_options = [url for url in image_options if url[-4:] in approved_exts]
        tries_before_giving_up = tries_before_giving_up - 1
        while not image_options and tries_before_giving_up:
            number_of_images = number_of_images + 1
            try:
                image_options = ImageScraper.scrape_images([voc], number_of_images=number_of_images)[0]  # res is still a list since I.S. outputs list of lists
            except IndexError:
                image_options = ["(NO IMAGE AVAILABLE)"]
            image_options = [url for url in image_options if url[-4:] in approved_exts]  # only permit image links with valid file extensions
            #if image_options and image_options[0][-4:] not in approved_exts:  # we only care abt first valid img; check its file ext
            #    image_options = ''
            tries_before_giving_up = tries_before_giving_up - 1
        try:
            image_options = f'<img src={image_options[0]}>'  # use the first valid image
            urls.append(image_options)
        except IndexError:
            urls.append("")  # (gave up trying to find a valid img)
    filtered_df["image"] = urls
    return filtered_df


def generate_audio(audio_url, title, audio_loc):
    title = title.replace('/', '')  # prevents issues with bad filenames breaking stuff
    doc = requests.get(audio_url)
    filename = os.path.join(audio_loc, title + '.mp3')
    if len(filename) > 255:
        filename = filename[:252] + '.mp3'
    anki_media_fp = "/Users/jacobhume/Library/Application Support/Anki2/User 1/collection.media"
    with open(filename, 'wb') as f:
        f.write(doc.content)

    anki_media_filename = os.path.join(anki_media_fp, title + '.mp3')
    if len(anki_media_filename) > 255:
        anki_media_filename = anki_media_filename[:252] + '.mp3'
    with open(anki_media_filename, 'wb') as f:  # also add to anki media
        f.write(doc.content)

    return anki_media_filename


def make_hsk_tag(simplified_word):
    new_hsk_v3 = pd.read_csv("new_hsk_v3.csv")
    hsk_v3_level = new_hsk_v3.columns[new_hsk_v3.isin([simplified_word]).any()][0]
    if hsk_v3_level == []: # above didn't find anything
        hsk_v3_level = "not_in_hsk_v3"

    return hsk_v3_level
    



    
    
def make_cards_from_text(text, source):
    """Inputs:
        text_in_english_or_simplified_or_traditional (3 categories): a string of text in English, simplified Chinese, or traditional Chinese, such as one of...
        1- English word ("shirt")              
        1- Simplified Chinese word ("衬衫")
        1- Traditional Chinese word ("襯衫")
        2- English text ("I can't take it right now...")
        2- Simplified Chinese text ("我现在受不了了...")
        2- Traditional Chinese text ("我現在受不了了...")
        3- An English natural-language translation inquiry ("In english, when i am verifying if some functionality works (while coding, etc), i use the word 'test'. what is the counterpart in chinese?")
        3- A simplified Chinese natural-language translation inquiry (在英语中，当我想要查看某些功能（如编码）是否有效时，我会使用'测试'这个词。那么，中文中的对应词是什么？")
        3- A traditional Chinese natural-language translation inquiry ("在英語中，當我想要查看某些功能（如編碼）是否有效時，我會使用'測試'這個詞。那麼，中文中的對應詞是什麼？")
        The behavior is DIFFERENT, however, in each case. 
        In case 1, the user is asking merely for the translation of a word. A single Anki note will be created accordingly if one does not already exist.
        In case 2, the user is asking for the translation of some multi-word, multi-phrase, or multi-sentence entity. It will be broken down into rather more 'atomic'
        components (e.g., words, small phrases, idioms), and a single Anki note will be created for each of these component. The trick is that the a text will be ADDED as an 'example sentence' for a 
        note created out of one of its 'atoms', and will hence appear as a cloze card and perhaps be factored into PracticeGPT conversations down the line. 
        So, although there won't be a full note dedicated to a large chunk of text, that specific text will still be factored into the learning process.
        Case 3 is actually probably not going to be implemented; PracticeGPT will just be able to make it part of case 2 conceptually... but leaving it here for now.
    Source: where this function is being called from. Examples include 'integrated_chinese_chapter_x', 'practice_gpt_review_session', 'practice_gpt_conversation', etc.
            this will be the 'source tag' for the resulting note(s) in Anki.
    """
    card_seeds = cnlp.chatgpt_smartish_segmentize(text) # the bits of text that will be used to create Anki notes

def decomposition_info_helper(fields_dict):
    # get decomposition information — simplified
    simpl_radicals_and_phonetics_dict_list = cnlp.text_decomposition_info(fields_dict["简体字Simplified"])

    # get decomposition information — traditional
    trad_radicals_and_phonetics_dict_list = cnlp.text_decomposition_info(fields_dict["繁体字Traditional"])

    for dict in simpl_radicals_and_phonetics_dict_list:
        for key in dict:
            fields_dict['Radicals (Simplified)'].append((dict[key], dict[key]['radicals']))
            fields_dict['Component Decomposition and Phonetic Regularity (Simplified)'].append((dict[key], dict[key]['phonetic_regularities']))

    for dict in trad_radicals_and_phonetics_dict_list:
        for key in dict:
            fields_dict['Radicals (Traditional)'].append(dict[key], dict[key]['radicals']) 
            fields_dict['Component Decomposition and Phonetic Regularity (Traditional)'].append((dict[key], dict[key]['phonetic_regularities']))

    return fields_dict

def mnemonic_helper(fields_dict, context_messages, gpt_model):
    decomposition_mnemonic_prompt = f"""Write a memnonic for the each of the characters {fields_dict["简体字simplified"]} by using the meanings of their constituent radicals: {fields_dict["'Radicals (Simplified)'"]}. Then insert a paragraph break. Then do the same thing but for traditional: Write a memnonic for the each of the characters {fields_dict["繁体字traditional"]} by using the meanings of their constituent radicals: {fields_dict["'Radicals (Traditional)'"]}"""
    context_messages.append({"role": "user", "content": f"{decomposition_mnemonic_prompt}"})
    second_response = utils.get_chatgpt_response(context_messages, temperature=0.7, model=gpt_model)
    context_messages = utils.update_chat(context_messages, "assistant", second_response)
    print("User: ", decomposition_mnemonic_prompt)
    print("Response: ", second_response)

    fields_dict["Radicals Mnemonic"] = second_response

    return fields_dict, context_messages

def chatgpt_semantic_tags_helper(fields_dict, context_messages, gpt_model, semantic_tags_info_prompt):
    success = False
    while not success:
        context_messages.append([{"role":"system", "content":semantic_tags_info_prompt}, {"role":"user", "content":f"""The text is {fields_dict["简体字Simplified"]} Remember to format your answer as a Python list of strings."""}])
        try:
            response = utils.get_chatgpt_response(context_messages, temperature=0, model=gpt_model)
            context_messages = utils.update_chat(context_messages, "assistant", response)
            print("User: ", semantic_tags_info_prompt)
            print("Response: ", response)
            semantic_tags = ast.literal_eval(response)
            success = True
        except Exception as e:
            print(e)
            print("Trying again, cGPT gave incorrectly formatted output")
    # replace spaces of each entry in semantic_tags with underscores
    for i in range(len(semantic_tags)):
        semantic_tags[i] = semantic_tags[i].replace(" ", "_")
    return semantic_tags, context_messages

def chatgpt_check_if_grammar_point_tag(text, context_messages):
    prompt = f"is {text} a grammar point in Chinese? Answer ONLY with 'True' or 'False'"
    while True:
        context_messages.append({"role":"user", "content":prompt})
        try: 
            response = ast.literal_eval(utils.get_chatgpt_response(context_messages, temperature=0))
            utils.update_chat(context_messages, "assistant", response)
            return response, context_messages
        except Exception as e:
            print(e)
            print("Trying again, cGPT gave incorrectly formatted output")
          

def make_frequency_percentile_tags(text):
    # e.g., if a character has the tag "top_20_percent", that means it is in the top 10% of most frequently used characters in the language
    freq_percentile = max([dictionary.get_character_frequency(character) for character in text]["percentage"])
    percents = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    categories = ["top_10_percent", "top_20_percent", "top_30_percent", "top_40_percent", "top_50_percent", "top_60_percent", "top_70_percent", "top_80_percent", "top_90_percent", "top_100_percent"]
    tags = []
    for i in range(len(categories)):
        if freq_percentile <= percents[i]:
            tags.append(categories[i])
    return tags

def chatgpt_pos_and_phrase_type_helper(text, context_messages):
    pos_system_prompt = """Your job is now to identify all parts-of-speech throughout the following text. Keep in mind that some words in Chinese can be multiple parts-of-speech at once, though you should not include duplicates in your response. Please format your answer as a Python list of strings, all lowercase and with no duplicate entries."""
    context_messages.append([{"role":"system", "content":pos_system_prompt}, {"role":"user", "content":f"The text is {text}. Remember to format your answer as a Python list of strings."}])
    pos_response = utils.get_chatgpt_response(context_messages, temperature=0)
    context_messages = utils.update_chat(context_messages, "assistant", pos_response)
    phrase_system_prompt = "Your job is now to identify the what type of syntactic phrase the following text is. The options are CP, TP, VP, NP, PP, AdjP, AdvP, XP, X. Respond ONLY with your answer. If you think the text is not a phrase, respond with 'not_a_phrase'."
    context_messages.append([{"role":"system", "content":phrase_system_prompt}, {"role":"user", "content":f"The text is {text}"}])
    phrase_response = utils.get_chatgpt_response(context_messages, temperature=0)
    context_messages = utils.update_chat(context_messages, "assistant", phrase_response)
    return pos_response, phrase_response, context_messages

def radical_tags(fields_dict, simplified=True):
    if simplified:
        key = "Radicals (Simplified)"
    else:
        key = "Radicals (Traditional)"
    rad_tags = []
    for i in range(len(fields_dict[key])):
        for pair in fields_dict[key][i]:
            if simplified:
                rad_tags.append(f"simpl_rad_{pair[0]}")
            else:
                rad_tags.append(f"trad_rad_{pair[0]}")
    return rad_tags # returns a list of strings


def generate_fields_and_tags(text_in_english_or_simplified_or_traditional, gpt_model, context_messages=[], example_sentence_given=None, source_tag=None, audio=None, audio_loc=None, add_image=False):
    # context messages are included when the function is invoked from within a conversation (e.g., during a PracticeGPT session)


    # creates a df  with fields as specified
    fields_dict = defaultdict()

    

    arbitrary_note_prompt = """
   You are a helpful AI Chinese language teacher, helping a student create Anki flashcards. I will give you a word in one of english, simplfied, or traditional Chinese. Please respond with the following information, formatted as a python dictionary (quoted strings are the dictionary keys).

- "简体字Simplified" : the simplified Chinese word.
- "繁体字Traditional" : the traditional Chinese word.
- "英文English" : the English translation. Can be as long as you want for nuanced words, but be concise and clear.
- "Simplification Process (GPT Estimate)" : the process of simplifying the traditional Chinese word to the simplified Chinese word, say "None" if the word is already simplified.
- "Vocab pinyin" : the pinyin of the Chinese word.
- "Etymology — GPT Conjecture" : etymology of the whole word... how do the individual characters' meaning contribute to the whole word's meaning? You may choose to analyze one or both of the simplified and traditional versions. 
- "Categories of Characters — GPT Conjecture" : The type of each character involved, perhaps one of 象形字,  形声字, 指事字,  会意字,  转注字, 假借字. Explain your answer. If you claim a character is a 形声字, you should check that the phonetic component matches the pinyin you provided before. If not, it is not 形声字 and you should think again about this!
- "例句Example sentence simplified" : An example sentence at the HSK3 level, in simplified Chinese. Disclude translation/pinyin.
- "例句Example sentence traditional" : The same sentence as above in traditional Chinese.
- "例句Example sentence pinyin" : The same sentence as above in pinyin.
- "例句Example sentence translation" : The same sentence as above in English.
- "Related words" : Words commonly used alongside the word, and description or example of the relation.
- "同义词/同義詞Synonyms" : Synonyms. Include pinyin and translation.
- "反义词/反義詞Antonyms" : Antonyms. Include pinyin and translation.
- 量词/量詞Classifier(s) : Measure words, if relevant. Include pinyin. Say "None" if not relevant.
- "Usages" : Any words, common phrases, idioms, etc. that use this word. Include pinyin and translation. For example, for 的 the response could be 有的时候, 别的, 是她做的，什么的. This is NOT just a place to add example sentences!

Thanks!"""

    

    semantic_tags_info_prompt = """Now your job is to, given user's text, classify it into any number (including zero) of the following properties. Please format your answer as a Python list of strings.
    Semantic categories:
    - food and drink
    - travel
    - shopping
    - work and employment
    - family and relationships
    - daily routines
    - entertainment
    - health and wellness
    - environment and sustainability
    - technology
    - culture and customs
    - politics and current events
    - education
    - weather and climate
    - sports and fitness
    - art and literature
    - history and traditions
    - holidays and celebrations
    - travel and tourism
    - movies and television
    - music and audio
    - philosophy and religion
    - cars and transportation
    - animals and wildlife
    - business and finance
    - geography and landmarks
    - fashion and style
    - science and technology
    - math, science and innovation
    - language and linguistics
    - learning chinese
    - Social Media and Internet Culture
    - Hobbies and Interests
    - Career and Professional Development
    - Astronomy and Space
    - Home and Lifestyle
    - Celebrity and Pop Culture
    - Cooking and Cuisine
    - Gardening and Plants
    - Chinese Mythology and Folklore
    - Personal Growth and Self-Improvement
    - Human Rights and Social Issues
    - Public Transport and Infrastructure
    - Outdoor Activities and Adventures
    - Photography and Visual Arts
    - Military and Defense
    - Etiquette and Social Norms
    - Pets and Pet Care
    - Volunteering and Community Service
    - Real Estate and Housing
    - Parenting and Childcare
    - Mental Health and Wellness
    - Elderly Care and Retirement
    - Dating and Relationships
    - Marriage and Weddings
"""

    # get chatgpt's response for relevant CARD FIELDS
    success = False
    while not success:
        try:
            first_user_prompt = f"""The word is {text_in_english_or_simplified_or_traditional}. Format your response as a python dictionary (where quoted strings are the dictionary's keys)."""
            context_messages.append([{"role": "system", "content": f"{arbitrary_note_prompt}"},{"role": "user", "content": f"{first_user_prompt}"}])
            first_response = utils.get_chatgpt_response(context_messages, temperature=0.7, model=gpt_model)
            context_messages = utils.update_chat(context_messages, "assistant", first_response)
            print("System: ", arbitrary_note_prompt)
            print("User: ", first_user_prompt)
            print("Response: ", first_response)
            fields_dict = ast.literal_eval(first_response)
            success = True
        except Exception as e:
            print(e)
            print("Trying again, cGPT gave incorrectly formatted output")


    # get decomposition information (simplified and traditional)
    fields_dict = decomposition_info_helper(fields_dict)
    
    # continue getting chatgpt response for relevant CARD FIELDS using the information from the decomposition
    fields_dict, context_messages = mnemonic_helper(fields_dict, context_messages, gpt_model)



    # begin making tags
    tags = defaultdict(list)
    # hsk tags
    tags["Level"].append(make_hsk_tag(fields_dict["简体字Simplified"]))

    # freq tags
    tags["Level"].append(make_frequency_percentile_tags(fields_dict["简体字Simplified"]))

    # get chatgpts response for card (semantic) TAGS
    tags["Semantic"], context_messages = chatgpt_semantic_tags_helper(fields_dict, context_messages, gpt_model) # returns a list of strings

    # time for syntactic tags
    is_grammar_point, context_messages = chatgpt_check_if_grammar_point_tag(fields_dict["简体字Simplified"], context_messages)
    if is_grammar_point:
        tags["Syntactic"].append["grammar_point"]
    
    pos, phrase_type, context_messages = chatgpt_pos_and_phrase_type_helper(fields_dict["简体字Simplified"], context_messages)
    tags["Syntactic"].append(pos); tags["Syntactic"].flatten() # since pos is a list
    if phrase_type != "not_a_phrase":
        assert(type(phrase_type)==str)
        tags["Syntactic"].append(phrase_type) 
    
    if fields_dict["量词/量詞Classifier(s)"] != "None":
        tags["Syntactic"].append("measure_word")

    if fields_dict["简体字Simplified"] != fields_dict["繁体字Traditional"]:
        tags["Orthographic"].append("simplified_differs_traditional")

    tags["Orthographic"].append(radical_tags(fields_dict, simplified=True))
    tags["Orthographic"].append(radical_tags(fields_dict, simplified=False))
    tags["Orthographic"].flatten() # since radical_tags returns a list

    






    

    

    if source_tag is not None:
        #if type(tag) is not list:  # then user wants the same tag for every entry
        #    tag = [tag] * len(translation)
        fields_dict["tags"] = source_tag


    if add_pinyin:
        fields_dict["pinyin"] = [generate_pinyin(s) for s in simplified]


    if add_traditional:
        fields_dict["traditional"] = [chinese_converter.to_traditional(s) for s in simplified]

    if audio == 'url':
        url_stem = "https://translate.google.com/translate_tts?ie=UTF-8&tl=zh-CN&client=tw-ob&q="
        audio_url = [url_stem + quote(s) for s in simplified]
        anki_audio = [f"[sound:{os.path.basename(generate_audio(a_url, a_url.split('=')[-1], audio_loc))}]" for a_url in audio_url]
        fields_dict["audio"] = anki_audio

    # construct df
    df = pd.DataFrame(fields_dict)

    # add image column to df if requested
    if add_image:
        df = add_images(df, query_col=simplified_col_name)

    return df