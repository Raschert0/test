from itertools import cycle
from mglobals import sec_level
import random

sec_levels = ['green', 'yellow', 'red']

sec_phrases = ('HALT! HALT! HALT! HALT!',
               'Stop in the name of the Law.',
               'Compliance is in your best interest.',
               'Prepare for justice!',
               'Running will only increase your sentence.',
               'Don\'t move, Creep!',
               'Down on the floor, Creep!',
               'Dead or alive you\'re coming with me.',
               'God made today for the crooks we could not catch yesterday.',
               'Freeze, Scum Bag!',
               'Stop right there, criminal scum!'
)

pool = cycle(sec_levels)

def nextSec():
    global sec_level
    global pool
    sec_level = next(pool)

