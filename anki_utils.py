from collections import defaultdict
import json
import urllib.request
import requests
import os
from urllib.parse import urlencode
from urllib.parse import quote
from urllib.request import urlopen


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


def is_duplicate(field_name, field_value):
    response = requests.post('http://localhost:8765', json={
        'action': 'findNotes',
        'version': 6,
        'params': {
            'query': f'{field_name}:"{field_value}"'
        }
    })
    return len(response.json()['result']) > 0

def add_note(fields_dict, deck_name, model_name, audio_dict=None, tags=[], dupe_check="简体字simplified"):
    if is_duplicate(dupe_check, fields_dict[dupe_check]):
        print("duplicate detected, not making card for ", fields_dict["简体字simplified"])
        return
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
            "tags": tags,
            #"audio": [audio_dict],
        }
    )

def get_due_ids(deck_name, limit=None):
    ids = invoke('findCards', query=f"deck:{deck_name} is:due")
    if limit is not None:
        return ids[:limit]
    return ids

def get_new_ids(deck_name, limit=None):
    ids = invoke('findCards', query=f"deck:{deck_name} is:new")
    if limit is not None:
        return ids[:limit]
    return ids

def get_review_ids(deck_name, limit=None):
    ids = invoke('findCards', query=f"deck:{deck_name} is:review")
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

def get_field_data_with_status(deck_name, status, field_names, limit=None):
    if status == "due":
        card_ids = get_due_ids(deck_name=deck_name, limit=limit)
    elif status == "new":
        card_ids = get_new_ids(deck_name=deck_name, limit=limit)
    elif status == "review":
        card_ids = get_review_ids(deck_name=deck_name, limit=limit)
    else:
        raise ValueError("status must be 'due', 'new', or 'review'")
    note_info, card_info = get_note_and_card_info(card_ids)

    note_field_data = defaultdict(list)
    card_field_data = defaultdict(list)

    for field_name in field_names:
        note_field_data[field_name] = [note_info[key]['fields'][field_name]['value'] for key in note_info.keys()]
        card_field_data[field_name] = [card_info[key]['fields'][field_name]['value'] for key in card_info.keys()]


    return note_field_data, card_field_data


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
    for row_index, row in filtered_df.iterrows():
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

if __name__ == '__main__':
    #def format_to_plaintext(data):
    #    plaintext_list = ""
    #    for character, components in data:
    #        plaintext_list += f'{character}\\n'
    #        for component, meaning in components:
    #            plaintext_list += f' - {component}: {meaning}\\n'
    #    return plaintext_list
#
    #data = [('做', [('亻', 'human'), ('十', 'ten'), ('口', 'mouth'), ('⺙', 'knock')]), 
    #        ('米', [('米', 'rice')]), 
    #        ('饭', [('饣', 'eat/food'), ('⺁', 'cliff'), ('又', 'right hand')])]
#
    #anki_plaintext_list = format_to_plaintext(data)
    #print(anki_plaintext_list)
    new_card_data = get_field_data_with_status('中文', 'new', field_names=["简体字simplified", "繁体字traditional", "id"])
    print(new_card_data)
    
