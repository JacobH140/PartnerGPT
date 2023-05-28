#from anki import Collection
# import the main window object (mw) from aqt
import anki
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *

if __name__ == '__main__':


    # The path to your Anki sqlite database - likely to be in your Anki User folder
    # If you are unsure where this is, from Anki's main window,
    # go to Tools -> Add-ons -> Open Add-ons Folder and navigate one level up
    db_path = "/Users/jacobhume/Library/Application Support/Anki2/User 1/collection.anki2" 

    # Load the Collection
    col = Collection(db_path)

    card = col.sched.getCard()
    print(card) 
    if not card:
        print("current deck is finished")
    else:
        #Answer the card:
        ease = 1 # 1=Again, 2=Hard, 3=Good, 4=Easy
        col.sched.answerCard(card, ease)
