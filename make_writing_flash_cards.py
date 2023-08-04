import anki_utils
import make_cards as mc
from collections import defaultdict
import jieba
import utils
from hanziconv import HanziConv
import chinese_nlp_utils as cnlp

def make_writing_flash_cards(text, source_tag, deck_name):
    """Given a text, make flash cards for writing practice."""
    simplified_text = cnlp.remove_spaces_punctuation(text)
    url_stem = "https://translate.google.com/translate_tts?ie=UTF-8&tl=zh-CN&client=tw-ob&q="
    segments = jieba.cut(simplified_text, cut_all=False)       
    for text_segment in segments:
        # skip if the segment is empty after removing punctuation
        if not cnlp.remove_spaces_punctuation(text_segment):
            continue
        

        segment = HanziConv.toSimplified(text_segment)
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
        try:
            fields_dict["vocab pinyin"] = " ".join(cnlp.chatgpt_get_pinyin(segment))
        except:
            fields_dict["vocab pinyin"] = "N/A (error)"

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
    text = """现代小农
星期天一大早，何雅婷就陪着妈妈到农夫市集去买菜。最近食品安全
出了好几次问题，何雅婷的妈妈为了家人的健康，开始注意食材的产地，也尽量到有机商店和农夫市集买菜。虽然这些地方卖的东西种类没有市场那么多，价钱也比较高，可是妈妈常跟农夫聊天，了解小农用友善的方式
对待上地和环境，很信任他们，所以宁可每个星期跑一趟，多花一点钱，也要支持小农。
像何雅婷妈妈这样关心小农的人越来越多。有人写文章介绍小农种的蔬菜水果，有人到处帮小农推销，其中最有名的是一位面包师傅。他从小在农村长大，了解农夫的辛苦。为了帮助小农，也为了帮自己的产品找更好的食材，他常常拜访小农，用他们出产的食材做出受欢迎的面包。
由于报纸、网路的介绍，许多住在城市里的人开始美慕小农的生活。
他们利用放假的时候，带着孩子到农村去，一方面可以让孩子在田里跑跑跳跳，接近自然，一方面自己也可以放松心情。到乡下住一晚变成了现在
热门的休闲活动。
随着小农越来越受重视，到农村来观光的人也慢慢地多起来了，连便利商店都来了。以前当地人习惯自己做饭，或是到传统的小商店和小吃店消费，现在便利商店更方便也更吸引他们。传统的小店生意受到了影响，原来安静的农村有了很大的变化。现在农人担心的是传统的生活方式会不会消失。"""
    make_writing_flash_cards(text, "CC3-Chapter 6-短文", deck_name="CC3-Chapter 6-短文")