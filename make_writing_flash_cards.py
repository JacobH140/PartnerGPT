import anki_utils
import make_cards as mc
from collections import defaultdict
import jieba
import utils
from hanziconv import HanziConv
import chinese_nlp_utils as cnlp

def make_writing_flash_cards(simplified_text, source_tag, deck_name):
    """Given a text, make flash cards for writing practice."""
    url_stem = "https://translate.google.com/translate_tts?ie=UTF-8&tl=zh-CN&client=tw-ob&q="
    segments = jieba.cut(simplified_text, cut_all=False)       
    for segment in segments:
        if anki_utils.is_duplicate_in_deck("简体字simplified", segment, deck_name):
            print("note for ", segment, " already exists, so not invoking chatgpt and moving on...")
            continue
        # card setup
        fields_dict = defaultdict(str) 
        fields_dict["简体字simplified"] = segment
        fields_dict["繁体字traditional"] = HanziConv.toTraditional(segment)
        fields_dict["英文english"] = cnlp.chatgpt_translate_to_english(segment) 

        # example sentence generation using ChatGPT
        sentence_prompt = "Create a sentence in simplified chinese containing the following text segment: " + segment + "."
        msgs = [{"role":"system", "content":sentence_prompt}]
        fields_dict["例句example sentence simplified"] = utils.get_chatgpt_response(msgs, temperature=0.7, model="gpt-4")
        fields_dict["例句example sentence traditional"] = HanziConv.toTraditional(fields_dict["例句example sentence simplified"])
        fields_dict["例句example sentence translation"] = cnlp.chatgpt_translate_to_english(fields_dict["例句example sentence simplified"])
        fields_dict["例句example sentence pinyin"] = " ".join(cnlp.chatgpt_get_pinyin(fields_dict["例句example sentence simplified"]))
        

        # audio generation using Google Translate
        fields_dict["量词/量詞classifier sound"] = "N/A"
        fields_dict["同义词/同義詞synonyms sound"] =  "N/A"
        fields_dict["反义词/反義詞antonyms sound"] =  "N/A"
        fields_dict["related words sound"] =  "N/A"   
        fields_dict["usages sound"] =  "N/A"
        mc.add_all_chinese_audio_to_note(fields_dict, url_stem, audio_loc="/Users/jacobhume/PycharmProjects/ChineseAnki/translation-audio")

        # add the source tag for easy studying later
        tags = [f"Writing::{source_tag}"]

        # get pinyin
        fields_dict["vocab pinyin"] = " ".join(cnlp.chatgpt_get_pinyin(segment))

        # get radicals and other word decomposition info
        fields_dict = mc.decomposition_info_helper(fields_dict)

        # get mnemonics
        fields_dict = mc.mnemonic_helper(fields_dict, "gpt-4")

        # add a usage notes blank field for tips added while studying'
        fields_dict["usage notes"] = ""

        # get image
        #fields_dict["图片/圖片image"] = mc.get_image(search_query=fields_dict["简体字simplified"])

        # add the note
        anki_utils.add_note(fields_dict, deck_name, "书法",  tags=tags, dupe_check=False)
        

if __name__ == "__main__":
    test_text = "我在图书馆发现了一本有趣的书。"
    make_writing_flash_cards(test_text, "test_tag", deck_name="CC3-Chapter 5-對話")