#!/usr/bin/env python

import sys

orig_word = ''.join(sys.argv[1:])
orig_letters = set(orig_word)
corpus = [word.strip() for word in open('slowa.txt').readlines() if all((letter in orig_letters) for letter in word.strip())]
print corpus
