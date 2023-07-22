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
    text = """陳 敏 萱 : 你 怎 麼 了 ? 怎麼那麼 沒精神 ?
l 高 橋健太 : 唉 ! 氣死 了 ! 昨 天 我上綱 買 五 月 天演唱 會 的
i 票 。 沒想 到 綱 路塞車 , 我試 了 兩 、 三個鐘頭 ,
等 我上線成 功 , 票 已經 賣 完 了 。 真倒楣 !
陳 敏 萱 : 你 別 生 氣 了 。 買 不 到 就算 了 。 為 什麼 非聽不

可 ?

蘿 瑨 蒂 : 五 月 天 是誰 ? 什麼 演 唱 會啊 ?
高 橋健太 : ( 拿 出 手機 ) 妳聽 。 這就是他們 的 歌 。 五 月
天 是 華 人世界最 受歡迎的 樂 團 。 下個 月 他們
的 演 唱 會 , 我當然不能錯過 。陳 敏 萱 : 我朋 友去聽 了 他們 的 跨年 演 唱 會 。 她說 , 那
天體育館擠 滿 了 人 , 大 家都 玷在椅 子上 又唱
又叫 , 興奮極 了 。

羅瑨蒂 : 他們很帥 嗎 ? 為 什麼 這麼 多 人迷他們 ?
高 橋健太 : 大 家 喜歡他們是因 為 他們 的 歌詞不但都 寫 得
很 美 , 而 且能 說 出 年輕人心裡的話 。 高興的
時候 , 要聽 ; 難過的 時候 , 更要聽 。

陳 敏 萱 : 演 唱 會 人那 麼 多 , 票 又不 好 買 , 不 如在 家上

綱看舒服 。

高 橋健太 : 聽演唱 會噹然 要去現場 , 大 家一 超唱 , 一 超
跳 , 整個 體 育館都在震動 。 這樣的 威 覺 沒去
過 的 人是不 能 了 解的 。

陳 敏 萱 : 罄音那 麼 大,吵 死 了 。 還 是在 家好 。
高 橋健太 : 妳整天在 家不 會太無聊嗎 ?
陳 敏 萱 : 怎 麼 會呢 ? 有 那 麼 多 有趣的 漫 畫 , 怎麼 會覺

得無聊 呢 ?

羅 瑒 蒂 : 我媽媽說租書 店 的 漫畫內容都 太 色 情 , 不 適

合我們看 。

高 橋健太 : 現在誰去 租書 店 啊 ? 大 家都 用 平板 電腦跟智

慧 型 手機上綱看 了 。

羅瑒蒂 : 我媽也說他朋 友的孩子 因 為 迷漫 畫 , 花了太
多 時 間 , 影 零 了 功課 , 所 以她不 讓我們 看 。
高 橋健太 : 不 會啊 , 好的漫畫 也很 多 啊 。 看 漫畫 除 了 可
以 放鬆心 情 , 還可以學到很 多歷史 、 文化和
傳統 。

陳 敏 萱 : 沒錯 。 我也是看 了 漫畫 才知道壽司是 怎麼做的 。
儸 瑁 蒂 : 看漫畫就是為 了 殺時 間 。 你 們想太多 啦 。
陳 敏 萱 : 幾 點 了 ? 這麼 晚啪 ? 我跟朋 友 約 了 去看漫畫
展 , 他們在捷運玷 等 我 , 再 不 走就來不 及 了 。
改天再聊吧 。"""
    make_writing_flash_cards(text, "CC3-Chapter 5-對話", deck_name="CC3-Chapter 5-對話")