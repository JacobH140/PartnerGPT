# ChatGPT-Infused Spaced Repetition System for Chinese Study

A Chinese learning toolkit for Mac/iOS based on what I call the **ARID Principles** of vocabulary acquisition: How can we simltaneously optimize the vocabulary acquisition process for:
- **A**ccessibility;
- **R**etention;
- **I**mmersion; and
- **D**ata?

![anki_mobile_gif](https://github.com/JacobH140/PartnerGPT/assets/71049464/0cd2e530-9a60-43c2-8e31-ab44dac51a87)

![mobile_conversation](https://github.com/JacobH140/PartnerGPT/assets/71049464/06004b14-0704-4d85-983d-cab39729d9e4)



![mobile_audio_input_demo](https://github.com/JacobH140/PartnerGPT/assets/71049464/70ee38c4-84d5-4028-b0b6-882299a61f2a)




https://github.com/JacobH140/PartnerGPT/assets/71049464/920a0a67-8d75-4b74-ad64-adf851ff3e38

# Introduction
In reference to the [ARID Principles](#chatgpt-infused-spaced-repetition-system-for-chinese-study), this program approaches Chinese vocabulary acquisition with the following priorities.

## Accessibility
### Of Input
Regardless of location and medium of interaction, learners should be able to access the card creation process without sacrificing any present immersion. 

This is accomplished via Alfred (Mac) and Siri (iOS) translation workflows which parse text, screenshot, audio, and photo input into flash cards. See [Creating Flashcards](#creating-flashcards).


## Retention
Learners should be algorithmically guided through the process of applying [Piotr Wozniak's 20 Rules of Knowledge Formulation](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge) to acquire vocabulary. 

[Anki](https://apps.ankiweb.net/)'s spaced repetition repetition is used to review cards created with these ideas in mind. See [Reviewing Flashcards](#reviewing-flashcards-in-Anki).


## Immersion
A learner should be able to practice in an immersive environment— if desired, they should be able to learn and review in conversational settings.

To this end, a [ChatGPT](https://chat.openai.com/) interface is provided which provides in-depth translations, micro-lessons for new words, dynamic translation and cloze deletion drills for review words, and freeform conversation concerning on a topic chosen by the learner. The latter three mediums incorporate 'batch reviews' of aging cards naturally incorporated into conversation, and 'keep track' of new words and questions the learner asks throughout the conversation to be automatically made into flashcards after.


## Data
A learner should have reach toward extensive resources regarding the learning contents, allowing them to eventually settle on a practice routine that is personal and flexible.

Numerous special tags and fields exist from which cards may be organized. See [flashcard fields](flashcard-fields) and [flashcard tags](flashcard-tags).

# Usage

## Creating Flashcards
(Ensure the Anki add-on is installed first.)

**On iOS.** The [iOS Shortcut](https://support.apple.com/guide/shortcuts/welcome/ios) provides translations and pinyin for Chinese or English input. These translations are just meant to be heuristics; they do not actually make it into the end card. Instead, the _input_ is uploaded to the learners PartnerGPT Google Sheet along with source and time of upload. After a small amount of time, the Anki add-on will make a flashcard for each word (and sometimes phrase) in the input for which it has not made a flashcard before. If the input is sufficiently long, it will use that sentence as the flashcard's example sentence.

Accepted input methods are
- Typed text
- Clipboard
- Most recent screenshot
- Take screenshot
- Camera
- Camera roll
- Speak English
- Speak Chinese (CN)
- Speak Chinese (TW)
- Conversation with PartnerGPT.

**On Mac.**

**From PartnerGPT Conversations.**

**From Google Sheets (Batch Creation)**


## Reviewing Flashcards in Anki
The Anki flashcard template seen below is designed with [Piotr Wozniak's 20 Rules of Knowledge Formulation](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge) in mind. Take a look:



https://github.com/JacobH140/PartnerGPT/assets/71049464/9f19113a-0e4e-484b-8d35-f0a49dec6313


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
The fields available for each card are

### Flashcard Tags
The tags available for each card are

### Card Templates


## Conversationally Revewing Flashcards
### Translate with ChatGPT

### Learn New Cards with ChatGPT

### Review Cards with ChatGPT

### Converse with ChatGPT
