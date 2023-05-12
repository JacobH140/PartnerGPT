from collections import defaultdict
from tqdm import tqdm
import json
import urllib.request
import requests
import os
from urllib.parse import urlencode
from urllib.parse import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup


def request(action, **params):
    # kinda ankiconnect boilerplate
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    # kinda ankiconnect boilerplate
    request_json = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', request_json)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def create_audio_dict(audio):
    audio_dict = {
            "url": '',
            "filename": audio,
            "skipHash": "7e2c2f954ef6051373ba916f000168dc",
            "fields": [
                "Back"
            ]
        }
    return audio_dict


def add_note(fields_dict, deck_name, model_name, audio_dict=None, tags=""):
    return invoke('addNote',
        note = {
            "deckName": deck_name,
            "modelName": model_name,
            "fields": fields_dict,
            "options": {
                "allowDuplicate": False,  # revert to F when not debugging
            "duplicateScope": "deck",
            "duplicateScopeOptions": { "deckName": "Export", "checkChildren": False}
            },
            "tags": [tags],
            #"audio": [audio_dict],
        }
    )

def get_due_ids(deck_name, limit=None):
    ids = invoke('findCards', query=f"deck:{deck_name} is:due")
    if limit is not None:
        return ids[:limit]
    return ids



def get_note_and_card_info(card_ids):
    note_info = {}
    card_info = {}
    for card_id in card_ids:
        card_data = invoke("cardsInfo", cards=[card_id])
        note_id = card_data[0]["note"]
        note_data = invoke("notesInfo", notes=[note_id])
        note_info[note_id] = note_data[0]
        card_info[card_id] = card_data[0]

    return note_info, card_info

def gui_answer_current_card(ease):
    invoke("guiAnswerCard", ease=ease)

def open_deck_review(deck_name):
    invoke("guiDeckReview", name=deck_name)


def permute_and_add(filtered_df, deck_name, model_name, fields_to_ignore=None, front_field='vocab'):
    """takes deck in dataFrame form (already filtered as required) and creates notes*fields cards
    for that deck, where for each note a distinct card is created whose front is a different field of that note
    (and back is all the others). Unfortunately only works for this specific use case due to time crunch with class starting soon"""
    if fields_to_ignore is None:
        fields_to_ignore = []
    for row_index, row in tqdm(filtered_df.iterrows()):
        for col_index, col in filtered_df.iteritems():
            if col_index in fields_to_ignore:
                continue
            field_names = filtered_df.columns
            front = filtered_df[col_index][row_index]
            other_fields_dict = defaultdict(list)
            for col_name in field_names:
                other_fields_dict[col_name] = filtered_df[col_name][row_index]
            hijacked_field = col_index  # weird semantics
            swapped = filtered_df[field_names[1]][row_index]  # swaps the "vocab" field contents into here, so that other fields can remain the same
            other_fields_dict[field_names[1]] = front
            other_fields_dict[hijacked_field] = swapped
            audio = filtered_df["audio"][row_index]
            audio_dict = create_audio_dict(audio)  # filtered_df.columns[0] is bc we just need a filename; is overall irrelevant
            tags = filtered_df["tag"][row_index]
            if other_fields_dict[front_field]:
                add_note(other_fields_dict, deck_name, model_name, audio_dict, tags)
