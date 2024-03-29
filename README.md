# ChatGPT-Infused Spaced Repetition System for Chinese Study

A Chinese learning toolkit for Mac/iOS based on what I call the **ARID Principles** of vocabulary acquisition: How can we simultaneously optimize the vocabulary acquisition process for:
- **A**ccessibility;
- **R**etention;
- **I**mmersion; and
- **D**ata?


![anki_mobile_gif](https://github.com/JacobH140/PartnerGPT/assets/71049464/baef3d49-f5de-4cd2-aba7-1b61ed85bf2a)![iPhone_text_translation](https://github.com/JacobH140/PartnerGPT/assets/71049464/c1b3d721-9268-4125-b149-defe837059bb)



![taxi_example_1](https://github.com/JacobH140/PartnerGPT/assets/71049464/b9d9ca9d-c0ce-4470-ac73-8bd217dbb678)


https://github.com/JacobH140/PartnerGPT/assets/71049464/c67589dc-5b56-49fc-b2a9-27a973bf8c95




https://github.com/JacobH140/PartnerGPT/assets/71049464/2cec976f-5545-4167-b9af-9fe7c968fb7c







# Introduction
In reference to the [ARID Principles](#chatgpt-infused-spaced-repetition-system-for-chinese-study), this program approaches Chinese vocabulary acquisition with the following priorities.

## Accessibility
Regardless of location and medium of interaction, learners should be able to access the card creation process without sacrificing any present immersion. 

This is accomplished via Alfred (Mac) and Siri (iOS) translation workflows which parse text, screenshot, audio, and photo input into flash cards. See [Creating Flashcards](#creating-flashcards).


## Retention
Learners should be algorithmically guided through the process of applying [Piotr Wozniak's 20 Rules of Knowledge Formulation](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge) to acquire vocabulary. 

[Anki](https://apps.ankiweb.net/)'s spaced repetition system is used to review cards created with these ideas in mind. See [Reviewing Flashcards](#reviewing-flashcards-in-Anki).


## Immersion
A learner should be able to practice in an immersive environment— if desired, they should be able to learn and review in conversational settings.

To this end, a ChatGPT interface is provided which provides in-depth translations, micro-lessons for new words, dynamic translation and cloze deletion drills for review words, and freeform conversation concerning on a topic chosen by the learner. The latter three mediums incorporate 'batch reviews' of aging cards naturally incorporated into conversation, and 'keep track' of new words and questions the learner asks throughout the conversation to be automatically made into flashcards after. See [Conversationally Reviewing Flashcards](#conversationally-revewing-flashcards).


## Data
A learner should have reach toward extensive resources regarding the learning contents, allowing them to eventually settle on a practice routine that is personal and flexible.

Numerous special tags and fields exist from which cards may be organized. See [Flashcard Fields](#flashcard-fields) and [Flashcard Tags](#flashcard-tags).

# Usage

## Creating Flashcards
(Ensure the Anki add-on is installed first.)

**On iOS.** The [iOS Shortcut](https://support.apple.com/guide/shortcuts/welcome/ios) provides translations and pinyin for Chinese or English input. These translations are just meant to be heuristics; they do not actually make it into the end card. Instead, the _input_ is uploaded to the learner's PartnerGPT Google Sheet along with source of upload. After a small amount of time, the Anki add-on will create a flashcard for each word (and sometimes phrase) in the input for which it has not made a flashcard before. If the input is sufficiently long, it will use that sentence as the flashcard's example sentence.

Accepted input methods are
- Typed text (See below)
- Clipboard
- Most recent screenshot
- Take screenshot
- Camera
- Camera roll
- Speak English
- Speak Chinese (CN)
- Speak Chinese (TW) (See below)
- Talk with PartnerGPT (See below)



![iPhone_text_translation](https://github.com/JacobH140/PartnerGPT/assets/71049464/4565e172-24e8-4849-9bb2-32e8032fcaba)


![mobile_audio_input_demo](https://github.com/JacobH140/PartnerGPT/assets/71049464/8d05ee91-d74a-4ca5-a650-6d562b1155b7)![mobile_conversation](https://github.com/JacobH140/PartnerGPT/assets/71049464/3522a9fa-0fbb-414b-bfa0-83d03165aad2)


**On Mac.** The [Alfred Workflow](https://www.alfredapp.com/) provides real-time translation heuristics of typed input. Upon pressing of the return key, the input is sent to the PartnerGPT Google Sheet. From there it works the same as **iOS.**


https://github.com/JacobH140/PartnerGPT/assets/71049464/e2f77e19-cda1-4557-945f-2e59a2788b9c


Additionally, a second Alfred Workflow exists (triggered as 'te' rather than 'tr') for parsing screenshots.


https://github.com/JacobH140/PartnerGPT/assets/71049464/f5cf4219-4a84-4552-a2b7-d42ba1182dd1



**From PartnerGPT Conversations.**
In any conversation with PartnerGPT, pressing the _Next_ button will prompt the AI to review the conversation since the last time _Next_ was pressed and find text which it thinks 'should be flashcarded'. A common example of text that 'gets flashcarded' in this manner would be when a learner doesn't recognize a character in one of ChatGPT's sentences and asks about it.




https://github.com/JacobH140/PartnerGPT/assets/71049464/335646cc-0d57-4eed-a038-97ca10aa5af6



**From Google Sheets (Batch Creation)**
It is also common to manually fill in PartnerGPT Google Sheet entries. This is especially useful when inputting vocabulary for a new textbook chapter. TIP: take advantage of the 'source' column! For example, if inputting textbook vocabulary, fill in the source column with the textbook chapter— that way, you can customize to study *just those words* later.
![CleanShot 2023-08-04 at 13 58 41@2x](https://github.com/JacobH140/PartnerGPT/assets/71049464/dd030dd3-5a02-4425-a1a2-1793e976dba2)



## Reviewing Flashcards in Anki
The Anki flashcard template seen below is designed with [Piotr Wozniak's 20 Rules of Knowledge Formulation](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge) in mind. Take a look:


https://github.com/JacobH140/PartnerGPT/assets/71049464/04eb67e4-40c9-49d8-80a7-c11c1c605930



1. **Do not learn if you do not understand.** Stroke animations, example sentences, images, and audio are all immediately viewable upon flipping a card. What _isn't_ immediately avaiable is pinyin or English versions of the auxillary data— those require an extra click. This challenges learners to understand new words 'in context', from both a textual and auditory perspective. [Conversing with PartnerGPT](#immersion) is a great way to understand new words as well, as a learner may ask questions to check comprehension. Finally, some example sentences are often determined based on the sentence a user originally asked PartnerGPT to translate; thus upon seeing a new card of this type they often immediately understand how to fit it into their overall picture of learned knowledge.

2. **Learn before you memorize.** Two on-flashcard tools are provided for this. The first is etymological: a small blurb detailing how the constituent characters relate (e.g., 眼鏡='eye'+'mirror' in the video). The second is orthographical: an analysis of the constituent components used in writing the characters and how they might convey its meaning. Probably the best way to learn brand new words is via the micro-lessons that [PartnerGPT conversations](#immersion) provide. 

3. **Build upon the basics.** When prompted with input, PartnerGPT creates flashcards out of _all_ different words found within, excluding any cards that already exist. This makes the learning process appear slow at first (in fact, I recommend using Anki rather than PartnerGPT for most practicing early on to most efficiently 'Easy' one's way through information they already know), but naturally calibrates the learner with a solid foundation upon which to build new knowledge. As [Dr. Wozniak](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge) says, "Basics may also appear volatile and the cost of memorizing easy things is little... However, each memory lapse on basics can cost you dearly!".

4. **Stick to the minimum information principle.** This is the whole point of studying vocabulary! (As opposed to memorizing example sentences, grammar patterns, etc... those are better accomplished via other mediums of study.)

5. **Cloze deletion is easy and effective.** Chatting with PartnerGPT on **Review** mode allows a learner to answer cards based on filling-in-the-blanks of context sentences provided by the AI.

6. **Use imagery – a picture is worth a thousand words**. Done! 

7. **Use mnemonic techniques.** Clicking on the image in a card yields a mnemonic from ChatGPT which attempts to connect characters' meanings to the components of which they're comprised. This is extremely useful for practicing writing as well as reading! Mnemonic quality varies from clever to outlandish, but usually is at the least a good starting place to make one's own mnemonic.

8. **Graphic deletion is as good as cloze deletion.** I am not sure how to make this point relevant for language learning— ideas welcome!

9. **Avoid sets.** Done!

10. **Avoid enumeration.** Done!

11. **Combat interference.** As [Dr. Wozniak](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge) notes, there is nothing algorithmically that can be done here... interference strikes unpredictably and distinctly for every person. Thus, cards have a 'Usage Notes' field which can be filled in with extra examples, context cues, anecdotes, etc. to make them unique. (Of course, all other fields — image, example sentences, mnemonic, etymology — can be edited as well.)

12. **Optimize wording.** N/A.

13. **Refer to other memories.** Points (3) and Anki's spaced repetition algorithm in general are intended to help here, but — similar to point (11) — the onus of execution falls on the learner. _Use_ the '*Usa*ge Notes' field!

14. **Personalize and provide examples.** Same as (13).

15. **Rely on emotional states.** Some of ChatGPT's fever dream mnemonics work great here, but for the most part the situation matches (13).

16. **Context cues simplify wording.** N/A.

17. **Redundancy does not contradict minimum information principle.** Learners can choose to include cards with English-front, Simplified-front, or Traditional-front. My preference is to maximize redundancy and include all 3 when studying.

18. **Provide sources.** See [data](#data).

19. **Provide date stamping.** Done!

20. **Prioritize.** Referencing [data](#data), the Anki component of PartnerGPT allows learners to prioritize what they study based on semantic, syntactic, orthographic, source, frequency, custom and more types of tags. The conversation component allows learners to decide what cards to review via deciding what the conversation topic should be. Finally, the translation-conversation component allows learners to get translations tailored to their specific situation quickly so that they can get back to immersion — PartnerGPT will remember to make flashcards based on the discussion had. 






### Flashcard Fields
As a reference, the fields filled in by the algorithm for each card are 
| VOCABULARY WORD | Simplified | Traditional | English | Pinyin | Audio | Image | Etymology | Radical/Phonetic Decomposition | Mnemonic | Simplification Process |
| -------------- | ---------- | ----------- | ------- | ------ | ----- | ----- | --------- | ------------------------------ | -------- | --------------------- |

| EXAMPLE SENTENCE | Simplified | Traditional | English | Pinyin | Audio |
| ---------------------- | ---------- | ----------- | ------- | ------ | ----- |

| SYNONYMS         | Simplified | Traditional | English | Pinyin | Audio |
| ---------------------- | ---------- | ----------- | ------- | ------ | ----- |

| ANTONYMS | Simplified | Traditional | English | Pinyin | Audio |
| ---------------------- | ---------- | ----------- | ------- | ------ | ----- |

| RELATED WORDS | Simplified | Traditional | English | Pinyin | Audio |
| ---------------------- | ---------- | ----------- | ------- | ------ | ----- |

| CLASSIFIERS | Simplified | Traditional | English | Pinyin | Audio |
| ---------------------- | ---------- | ----------- | ------- | ------ | ----- |

| USAGES | Simplified | Traditional | English | Pinyin | Audio |
| ---------------------- | ---------- | ----------- | ------- | ------ | ----- |

| RADICALS | Simplified | Traditional | English | 
| ---------------------- | ---------- | ----------- | ------- |

| PHONETIC REGULARITIES | Simplified | Traditional | English | Pinyin | 
| ---------------------- | ---------- | ----------- | ------- | ------- |



### Flashcard Tags
For each card, tags corresponding to the categories below are offered. These can be used to arrange custom study sessions (e.g., 'study all verbs in HSK 7-9 with the radical 言'), steer PartnerGPT conversations ('let's review cards through a conversation about `art_and_literature` ), etc.

| `Category` | Examples | 
| ---------------------- | ---------- | 
| `Source` | 'Integrated Chinese Textbook 4, Chapter 7', 'added from iPhone' |
| `Level` | 'HSKv2 level 4', 'HSKv3 level 6'， ‘not in HSKv3’ |
| `Frequency` | 'in top 40% of most frequentlty used words' |
| `Semantic` | 'geography and landmarks', 'Chinese mythology and folklore', 'etiquette and social norms' |
| `Classifier` | '个'， ‘台’， ’辆‘, ‘座' |
| `Orthographic` | 'simplified contains radical 乚', 'traditional contains radical 車'|
| `Syntactic` | 'adjective', 'is a grammar point', 'idiom', 'is a measure word' |
| `Custom` | (User-defined) |




## Conversationally Reviewing Flashcards
The PartnerGPT conversation interface has four pages: **translate**, **learn**, **review**, and **converse**.
### Translate with ChatGPT
Quickly provide ChatGPT with translation prompts. These can be more detailed than those for Google translate, e.g., 'how should I say 'excuse me' when I bump into someone?', and followups can be asked, e.g., 'is this expression common in Taiwan?'. Pressing _Next_ allows PartnerGPT to create flashcards based on the conversation.


https://github.com/JacobH140/PartnerGPT/assets/71049464/a3483590-1d7d-48c4-b105-fe95bd4cc99c




### Learn New Cards with ChatGPT
This is where the learner is **introduced to new words** for the first time. The conversation takes the form of a mini tutoring lesson structured as:
1. ChatGPT introduces the new word, its etymology, and perhaps some tricks for remembering it.
2. The user asks questions and practices usage.

Throughout, ChatGPT will incorporate long-term review cards into the dialogue as 'batch review'.

Once the user feels as though they have _understood and learned_ the new word [(recall Wozniak's first and second points !)](#reviewing-flashcards-in-anki), they click the _Next_ button. They are prompted to Anki-rate the difficulty of the new card as well as the infused long-term review cards, and to multiselect from a provided list any incidentally new words involved in the conversation for which that they would like PartnerGPT to make flashcards.



https://github.com/JacobH140/PartnerGPT/assets/71049464/9b1c8c91-a937-4353-898e-5933c47233dd





### Review Cards with ChatGPT
This is where the learner **drills recently learned words** and **batch-reviews long-term words**. Drills may include dynamic translation exercises or cloze deletions. Laced throughout these exercises are uses of long-term words. The _Next_ button functions identically to the **learn** page.



https://github.com/JacobH140/PartnerGPT/assets/71049464/38c8a6ab-736d-4583-8e15-7070810909aa



### Converse with ChatGPT
This is where the learner can engage in free-form conversation on a topic of their choice while simultaneously batch-reviewing long-term cards. The _Next_ button functions as it does for the **review** and **learn** pages.
