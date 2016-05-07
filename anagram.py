#!/usr/bin/env python

import codecs, sys
from bisect import bisect_left
from collections import Counter

max_word_count = 3
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    max_word_count = int(sys.argv[1])
    sys.argv = sys.argv[1:]
orig_word = ''.join(sys.argv[1:]).decode('utf-8').lower()
orig_letters = set(orig_word)

print 'Preparing corpus...',
corpus = [
    word.strip() for word in codecs.open('slowa.txt', 'r', encoding='utf8').readlines() \
        if all((letter in orig_letters) for letter in word.strip())
]
print len(corpus), 'words.'


# level == x  <=>  x letters are already placed when entering the call
def search(available_letters, complete_words, uncomplete_word, level):
    if level == len(orig_word) and not uncomplete_word:
        yield complete_words
    elif len(complete_words) < max_word_count:
        for letter, count in sorted(available_letters.items()):
            if count == 0: continue
            new_word = uncomplete_word + letter
            if complete_words and new_word < complete_words[-1]: continue
            updated_letters = available_letters.copy()
            updated_letters[letter] -= 1
            new_word_index = bisect_left(corpus, new_word)
            if new_word_index == len(corpus): continue
            if not corpus[new_word_index].startswith(new_word): continue
            if corpus[new_word_index] == new_word:
                for i in search(updated_letters, complete_words + [new_word], '', level + 1):
                    yield i
            for i in search(updated_letters, complete_words, new_word, level + 1):
                yield i

print 'Looking for anagrams, up to', max_word_count, 'words long...'
for seq in search(Counter(orig_word), [], '', 0):
    print ' '.join(seq)

