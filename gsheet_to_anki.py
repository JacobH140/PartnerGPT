import os
import make_cards as mkc
import anki_utils
import gsheet_utils as gs
import jieba
import pandas as pd
import re

def make_cards_from_translation_gsheet():
    df, wks = gs.access_gsheet_by_url(url="https://docs.google.com/spreadsheets/d/1MfIh7x2sIwnLYFUpunpTb_x77woirfPOSGEQhqJ0Qto/edit?usp=sharing", sheet_name='Texts')
    if not df.empty:
        gs.log_df(df, 'learning-data/gsheet_df.csv')
        for row in df.itertuples():
          mkc.make_anki_notes_from_text(text=row[1], source=row[2], context_messages=row[3]) # Text (in either language, simpl or trad), Source, context_messages data, respectively
        gs.clear_sheet(wks, keep_headers=True)
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
    



