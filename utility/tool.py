from ngram import NGram


def nearlySameText(text_1, text_2):
    return NGram.compare(text_1.strip(), text_2.strip()) >= 0.9

def prepcessCitingSentence(sentence):
    removed_non_ascii = ''.join([i if ord(i) < 128 else '' for i in sentence])
    removed_non_ascii = removed_non_ascii.strip('.')
    while '  ' in removed_non_ascii:
        removed_non_ascii = removed_non_ascii.replace('  ', ' ')
    removed_non_ascii = removed_non_ascii.replace('[ ', '[')
    removed_non_ascii = removed_non_ascii.replace(' ]', ']')

    removed_non_ascii = removed_non_ascii.replace('( ', '(')
    removed_non_ascii = removed_non_ascii.replace(' )', ')')

    return removed_non_ascii.strip()