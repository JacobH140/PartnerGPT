import os
import make_cards as mkc
import anki_utils
import gsheet_utils as gs
import jieba
import pandas as pd
import re
import time
from datetime import datetime

def make_cards_from_translation_gsheet(persistent=False):
    url = 'https://docs.google.com/spreadsheets/d/1MfIh7x2sIwnLYFUpunpTb_x77woirfPOSGEQhqJ0Qto/edit?usp=sharing'
    df, wks = gs.access_gsheet_by_url(url=url, sheet_name='To Create')
    if not df.empty:
        gs.log_df(df, 'learning-data/gsheet_df.csv')
        for i, row in df.iterrows():
          entry = list(row)
          num_tries = 0
          success = False
          seconds_to_sleep = 10
          while not success:
            if not row[0]: # disregard any empty text entries
                wks.delete_rows(2, 2)
                continue
            try:
                #mkc.make_anki_notes_from_text(text=row[0], source=row[1], context_messages=row[2]) # Text (in either language, simpl or trad), Source, context_messages data, respectively
                success = True
                entry[3] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # log with the current time
                _, log_wks = gs.access_gsheet_by_url(url=url, sheet_name='Created')
                log_wks.append_row(entry)
                wks.delete_rows(2, 2) # delete the first non-header spreadsheet row, this should be the one we just processed
                print(f"Created note for text {row[0]}, assuming one does not already exist.")
            except Exception as e:
                if not persistent:
                    raise Exception(f"Error on gsheet:\n---\n {e} \n---\n Text was '{row[0]}'. Only tried once, set persistent=True to have me re-try up to 5 times.")
                else:
                    print(f'Error on row of gsheet:\n---\n {e} \n---\n, text was {row[0]}. Sleeping for {seconds_to_sleep} seconds then trying again.')
                    num_tries += 1
                    time.sleep(seconds_to_sleep)
                    seconds_to_sleep *= 2
                    if num_tries > 5:
                        raise Exception(f'Error on row of gsheet, tried and failed {num_tries} times:\n---\n {e} \n---\n, text was {row[0]}. Slept for up to {seconds_to_sleep} seconds each time.')
        
        #gs.clear_sheet(wks, keep_headers=True)
        print(df)

        # upload any terms which are unknown to the unknown sheet
        # v_df, v_wks = gs.access_gsheet(auth_json='anki-359920-d78c1a86928f.json', file_name='Async Translate', sheet_name='Vocab')


def find_unknown_vocabs(simplifieds, known_vocab_csv='learning-data/known-vocab.csv'):
    return [find_unknown_vocab(s, known_vocab_csv) for s in simplifieds]

def find_unknown_vocab(simplified, known_vocab_csv='learning-data/known-vocab.csv'):
    output = []
    jieba.enable_paddle()
    seg_list = jieba.cut(simplified, use_paddle=True)
    kv_df = pd.read_csv(known_vocab_csv, sep='\t')
    for word in seg_list:
        word = remove_nonalnum(word)  # chinese characters are alnum; this is to prevent spaces, punctuation, etc from being added
        if word and word not in kv_df['vocab'].tolist():
            output.append(word)

    output = [o for o in output if re.search(u'[\u4e00-\u9fff]', o)]  # only keep non chinese entries
    return output

def remove_nonalnum(_str):
    return ''.join(_char for _char in _str.lower() if _char.isalnum())

if __name__ == "__main__":
    # always run vocab first on a small df to generate known-vocab.csv if it doesn't exist for some reason!
    make_cards_from_translation_gsheet()
    


