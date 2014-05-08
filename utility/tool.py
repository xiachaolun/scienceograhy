from pyquery import PyQuery as pq
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


def hasNextPage(url):
    html = pq(url)
    text = html('a').filter('.nextprev').filter(lambda i: 'Go to Next Page' in str(pq(this).attr('title'))).text()
    return text == 'Next'
    #<a id="ctl00_MainContent_ObjectList_Next" title="Go to Next Page" class="nextprev"
    # href="/Detail?entitytype=2&amp;searchtype=2&amp;id=1790648&amp;start=101&amp;end=200">Next</a>