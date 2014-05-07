from ngram import NGram
import random
import time

def nearlySameText(text_1, text_2):
    return NGram.compare(text_1.strip(), text_2.strip()) >= 0.9

def prepcessCitingSentence(sentence):
    res = ''.join([i if ord(i) < 128 else '' for i in sentence])
    res = res.strip('.')
    while '  ' in res:
        res = res.replace('  ', ' ')
    res = res.replace('[ ', '[')
    res = res.replace(' ]', ']')

    res = res.replace('( ', '(')
    res = res.replace(' )', ')')

    res = res.replace(' ,', ',')

    return res.strip()

def randomSleep():
    sec = random.randint(0, 100) % 2 + 1
    time.sleep(sec)